import time
import sys, os
import fabric
from rs4.apis.aws import ec2, elb2, ec2cli, rt53, autoscaling
import threading
import requests
from pprint import pprint
import botocore

class AutoScaleDeploy:
    def __init__ (self, system, initial_image, key_name, subnets, security_groups):
        self.system = system

        self.KEY_NAME = key_name
        self.INITIAL_AMI_ID = initial_image
        self.AMI_ID = initial_image
        self.SUBNETS = subnets
        self.SECURITY_GROUPS = security_groups

        requisits = self.get_images ()
        if requisits:
            self.AMI_ID = requisits [0]['ImageId']
        self.LAUNCH_TEMPLATE = '{}-launch-template'.format (self.system)
        self.AUTO_SCALING_GROUP = '{}-as-group'.format (self.system)
        self.EC2_NAME = '{}-elb-member'.format (self.system)
        self.ELB = '{}-elb'.format (self.system)
        self.ELB_TARGET = '{}-elb-target'.format (self.system)

        self.ELB_GROUP_ARN = None
        self.ELB_ARN = None
        self.NEW_ELB = False

    def ssh (self, inst, KEY_FILE, user = 'ubuntu'):
        if isinstance (inst, str):
            inst = ec2.Instance (inst)
        if inst.state ['Name'] != 'running':
            raise SystemError ('instance not running')
        return fabric.Connection (inst.public_dns_name, user, connect_kwargs = dict (key_filename = KEY_FILE))

    def sshcli_by_passwd (self, host, user, password, port = 22):
        return fabric.Connection (host, user, port = port, connect_kwargs = dict (password = password))

    def get_images (self):
        images = ec2cli.describe_images (Owners=['self'])['Images']
        images = [img for img in images if img ['Name'].startswith ('{}-'.format (self.system))]
        if not images:
            return []
        images.sort (key = lambda x: x ['Name'], reverse = True)
        return images

    def set_route (self, hosted_zone, type, domain, value, alias_zone_id = None):
        ChangeBatch={
            'Comment': 'Create/Update ELB dns entry',
            'Changes': [{
                'Action': 'UPSERT',
                'ResourceRecordSet': {'Name': '{}.'.format (domain), 'Type': type}
            }]
        }
        if alias_zone_id:
            ChangeBatch ['Changes'][0]['ResourceRecordSet']['AliasTarget'] = { 'HostedZoneId': alias_zone_id, 'DNSName': value, 'EvaluateTargetHealth': False}
        else:
            ChangeBatch ['Changes'][0]['ResourceRecordSet']['ResourceRecords'] = [{'Value': value}]
            ChangeBatch ['Changes'][0]['ResourceRecordSet']['TTL'] = 300
        rt53.change_resource_record_sets(
            HostedZoneId='Z05482662UQBG0NKWZHCJ',
            ChangeBatch=ChangeBatch
        )

    def link_elb_to_domain (self, hosted_zone, type, domain, alias_zone_id):
        if not self.NEW_ELB:
            return
        self.set_route (hosted_zone, type, domain, self.ELB_DNS_NAME, alias_zone_id)

    def create_resources_if_not_exists (self, instance_type, instance_role_arn, cert):
        print ('checking elastic load balancer...')
        elbs = [e for e in elb2.describe_load_balancers () ["LoadBalancers"] if e ['LoadBalancerName'] == self.ELB]
        if not elbs:
            self.NEW_ELB = True
            elbs = elb2.create_load_balancer (
                Name = self.ELB,
                Subnets = ['subnet-94c348d8', 'subnet-b76d8ecc'],
                SecurityGroups = self.SECURITY_GROUPS,
                Tags=[{'Key': 'system', 'Value': self.system }],
                Type='application',
                Scheme='internet-facing',
                IpAddressType='ipv4'
            ) ['LoadBalancers']
        self.ELB_ARN = elbs [0]['LoadBalancerArn']
        self.ELB_DNS_NAME = elbs [0]['DNSName']

        print ('checking target group...')
        tgs = [e for e in elb2.describe_target_groups () ["TargetGroups"] if e ['TargetGroupName'] == self.ELB_TARGET]
        if not tgs:
            tgs = elb2.create_target_group (
                Name = self.ELB_TARGET,
                VpcId = elbs [0] ['VpcId'],
                Protocol = 'HTTP',
                Port = 80
            ) ['TargetGroups']
        self.ELB_GROUP_ARN = tgs [0]['TargetGroupArn']

        if self.NEW_ELB:
            elb2.create_listener (
                LoadBalancerArn = self.ELB_ARN, Protocol = 'HTTP', Port = 80,
                DefaultActions = [{
                    'Type': 'redirect',
                    "RedirectConfig": {
                        "Protocol": "HTTPS",
                        "Port": "443",
                        "StatusCode": "HTTP_301",
                    }
                }]
            )
            elb2.create_listener (
                LoadBalancerArn = self.ELB_ARN, Protocol = 'HTTPS', Port = 443,
                DefaultActions = [{'Type': 'forward', 'TargetGroupArn': self.ELB_GROUP_ARN}],
                Certificates = [ {'CertificateArn': cert} ],
                SslPolicy='ELBSecurityPolicy-2016-08'
            )

        print ('checking launch template...')
        tps = [e for e in ec2cli.describe_launch_templates () ["LaunchTemplates"] if e ['LaunchTemplateName'] == self.LAUNCH_TEMPLATE]
        if not tps:
            ec2cli.create_launch_template (
                LaunchTemplateName = self.LAUNCH_TEMPLATE,
                LaunchTemplateData = {
                    'CreditSpecification': {'CpuCredits': 'standard'},
                    'DisableApiTermination': False,
                    'IamInstanceProfile': {'Arn': instance_role_arn},
                    'ImageId': self.AMI_ID,
                    'InstanceType': instance_type,
                    'KeyName': self.KEY_NAME,
                    'Monitoring': {'Enabled': False},
                    'SecurityGroupIds': self.SECURITY_GROUPS,
                    'TagSpecifications': [{'ResourceType': 'instance',
                                            'Tags': [
                                                {'Key': 'system', 'Value': self.system},
                                                {'Key': 'Name', 'Value': self.EC2_NAME}
                                            ]
                                        }]
                    }
            )

    def create_auto_scaling_group (self):
        asg = [e for e in autoscaling.describe_auto_scaling_groups () ["AutoScalingGroups"] if e ['AutoScalingGroupName'] == self.AUTO_SCALING_GROUP]
        if not asg:
            autoscaling.create_auto_scaling_group (
                AutoScalingGroupName = self.AUTO_SCALING_GROUP,
                MinSize = 1,
                MaxSize = 10,
                VPCZoneIdentifier = ','.join (self.SUBNETS),
                LaunchTemplate = {'LaunchTemplateName': self.LAUNCH_TEMPLATE, 'Version': '$Latest'},
                TargetGroupARNs = [self.ELB_GROUP_ARN],
                Tags = [{'Key': 'system',
                    'PropagateAtLaunch': True,
                    'ResourceId': self.AUTO_SCALING_GROUP,
                    'ResourceType': 'auto-scaling-group',
                    'Value': self.system
                }]
            )

    def launch_instance (self, instance_type, user_data = None, dryrun = False):
        instances = ec2.create_instances (
            ImageId = self.INITIAL_AMI_ID,
            MinCount = 1,
            MaxCount = 1,
            InstanceType = instance_type,
            Monitoring = {'Enabled': False},
            SecurityGroupIds = self.SECURITY_GROUPS,
            DryRun = dryrun,
            KeyName = self.KEY_NAME,
            UserData = isinstance (user_data, str) and user_data or '\n'.join (user_data),
            InstanceInitiatedShutdownBehavior = 'terminate',
            TagSpecifications = [{
                    'ResourceType': 'instance',
                    'Tags': [
                            {'Key': 'Name', 'Value': '{}-elb-member'.format (self.system)},
                            {'Key': 'system', 'Value': self.system},
                    ]
                },
            ])

        inst = instances [0]
        print ('creating instance...: {} {}'.format (inst.id, inst.public_dns_name))
        for i in range (20):
            inst.reload()
            state = inst.state ['Name']
            if state == 'running':
                print ('instance created')
                return inst
            print ('- instance state: {}'.format (state))
            time.sleep (6)
        inst.terminate ()
        raise SystemError ('instance creation timeout')

    def remove_old_images (self, keep = 3):
        images = self.get_images ()
        print ('unregistering images...')
        for img in images [keep:]:
            id = img ['ImageId']
            ec2cli.deregister_image(ImageId = id)
            print ('- image unregistered: {}'.format (id))

    def create_image (self, inst, testfunc):
        image = None
        print ('waiting for app...')
        time.sleep (200)
        for i in range (60):
            if testfunc (self, inst):
                image = inst.create_image (Name = '{}-{}'.format (self.system, time.strftime ('%y%m%d%H%M', time.localtime (time.time ()))))
                break
            print ('- waiting...')
            time.sleep (10)

        if not image:
            raise SystemError ('instance activation failed')

        print ('creating image...')
        time.sleep (60)
        for i in range (30):
            image.reload ()
            if image.state == 'available':
                break
            print ('- image state: {}'.format (image.state))
            time.sleep (20)
        print ('image created: {}'.format (image.id))
        self.remove_old_images (3)
        assert testfunc (self, inst)
        return image

    def get_latest_template_version (self):
        templates = ec2cli.describe_launch_template_versions (LaunchTemplateName = self.LAUNCH_TEMPLATE, MaxResults = 1)
        return templates ['LaunchTemplateVersions'][0]

    def update_template (self, image):
        print ('applying {} to template...'.format (image.id))
        latest = self.get_latest_template_version ()
        ec2cli.create_launch_template_version (
            LaunchTemplateName = self.LAUNCH_TEMPLATE,
            SourceVersion = str (latest ['VersionNumber']),
            LaunchTemplateData = {'ImageId': image.id}
        )
        latest = self.get_latest_template_version ()
        print ('new launch template version created: {}'.format (latest ['VersionNumber']))

    def restruct_elb_target (self, inst):
        members = elb2.describe_target_health (TargetGroupArn = self.ELB_GROUP_ARN) ['TargetHealthDescriptions']
        deregisterables = [{'Id': m ['Target']['Id'], 'Port': m ['Target']['Port']} for m in members if m ['Target']['Id'] != inst.id]

        print ('registering new elb2 member: {}'.format (inst.id))
        elb2.register_targets (
            TargetGroupArn = self.ELB_GROUP_ARN,
            Targets = [{'Id': inst.id, 'Port': 80}]
        )

        if deregisterables:
            print ('deregistering {} elb2 members...'.format (len (deregisterables)))
            for each in deregisterables:
                print ('- deregistering: {}'.format (each ['Id']))
            elb2.deregister_targets (
                TargetGroupArn = self.ELB_GROUP_ARN,
                Targets = deregisterables
            )

        for i in range (30):
            members = elb2.describe_target_health (TargetGroupArn = self.ELB_GROUP_ARN) ['TargetHealthDescriptions']
            if [1 for m in members if m ['Target']['Id'] == inst.id and m ['TargetHealth']['State'] == 'healthy' ]:
                print ('instance registered successfully: {}'.format (inst.id))
                break
            time.sleep (10)

    def cleanup_instances (self, inst):
        deletables = [depre.id for depre in ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': [self.EC2_NAME]}]) if depre.id != inst.id and depre.state ['Name'] == 'running']
        print ('clean up old/unused instances...')
        # wait for finidhing draining, otherwise scaler launch one forcely
        for i in range (20):
            members = elb2.describe_target_health (TargetGroupArn = self.ELB_GROUP_ARN) ['TargetHealthDescriptions']
            actives = { m ['Target']['Id']: m ['TargetHealth']['State'] for m in members }
            _deletables = []
            for id in deletables:
                if id not in actives or actives [id] not in ('draining', 'healthy', 'initial'):
                    print ('- terminating: {}'.format (id))
                    ec2.Instance (id).terminate ()
                else:
                    print ('- {}: {}'.format (id, actives [id]))
                    _deletables.append (id)
            if not _deletables:
                break
            deletables = _deletables
            time.sleep (30)
