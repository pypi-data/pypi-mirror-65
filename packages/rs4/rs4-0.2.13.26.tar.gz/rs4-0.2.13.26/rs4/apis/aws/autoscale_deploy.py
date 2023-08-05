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
        self.VPC_ID = None
        self.LAUNCH_TEMPLATE_VERSION = "1"

    def ssh (self, inst, key_file, user = 'ubuntu'):
        if isinstance (inst, str):
            inst = ec2.Instance (inst)
        if inst.state ['Name'] != 'running':
            raise SystemError ('instance not running')
        return fabric.Connection (inst.public_dns_name, user, connect_kwargs = dict (key_filename = key_file))

    def ssh_with_password (self, host, user, password, port = 22):
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

    def link_elb_to_domain (self, hosted_zone, domain, alias_zone_id):
        if not self.NEW_ELB:
            return
        self.set_route (hosted_zone, 'A', domain, self.ELB_DNS_NAME, alias_zone_id)

    def create_load_balancer_if_not_exists (self):
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
        self.VPC_ID = elbs [0] ['VpcId']

    def add_listener_if_not_exists (self, cert, target_group_arns = None):
        listensers = elb2.describe_listeners (LoadBalancerArn = self.ELB_ARN) ['Listeners']
        protocols = [ lsn ['Protocol'] for lsn in listensers ]
        target_group_arns = target_group_arns or [(self.ELB_GROUP_ARN, 1)]
        target_groups = [{'TargetGroupArn': target_arn, 'Weight': weight} for target_arn, weight in target_group_arns]
        if 'HTTPS' not in protocols:
            elb2.create_listener (
                LoadBalancerArn = self.ELB_ARN, Protocol = 'HTTPS', Port = 443,
                DefaultActions = [{'ForwardConfig': {'TargetGroups': target_groups}, 'Type': 'forward'}],
                Certificates = [ {'CertificateArn': cert} ],
                SslPolicy='ELBSecurityPolicy-2016-08'
            )

        if 'HTTP' not in protocols:
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

    def create_launch_template_if_not_exists (self, instance_type, instance_role_arn):
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

    def create_target_group_if_not_exists (self, target_group_name = None):
        print ('checking target group...')
        is_default_target_group = target_group_name is None
        target_group_name = target_group_name or self.ELB_TARGET
        tgs = [e for e in elb2.describe_target_groups () ["TargetGroups"] if e ['TargetGroupName'] == target_group_name]
        if not tgs:
            tgs = elb2.create_target_group (
                Name = target_group_name,
                VpcId = self.VPC_ID,
                Protocol = 'HTTP',
                Port = 80
            ) ['TargetGroups']

        if is_default_target_group:
            # default
            self.ELB_GROUP_ARN = tgs [0]['TargetGroupArn']
        return tgs [0]['TargetGroupArn']

    def create_auto_scaling_group_if_not_exist (self, min_, max_, auto_scaling_group_name = None, target_group_arn = None):
        print ('checking auto scaling group...')
        auto_scaling_group_name = auto_scaling_group_name or self.AUTO_SCALING_GROUP
        asg = [e for e in autoscaling.describe_auto_scaling_groups () ["AutoScalingGroups"] if e ['AutoScalingGroupName'] == auto_scaling_group_name]
        if not asg:
            autoscaling.create_auto_scaling_group (
                AutoScalingGroupName = auto_scaling_group_name,
                MinSize = min_,
                MaxSize = max_,
                VPCZoneIdentifier = ','.join (self.SUBNETS),
                LaunchTemplate = {'LaunchTemplateName': self.LAUNCH_TEMPLATE, 'Version': '$Latest'},
                TargetGroupARNs = [target_group_arn or self.ELB_GROUP_ARN],
                TerminationPolicies = ['OldestLaunchTemplate', 'OldestInstance'],
                Tags = [{'Key': 'system',
                    'PropagateAtLaunch': True,
                    'ResourceId': auto_scaling_group_name,
                    'ResourceType': 'auto-scaling-group',
                    'Value': self.system
                }]
            )

    def add_scaling_policy (self, name, metric_type = 'ASGAverageCPUUtilization', value = 75.0, auto_scaling_group_name = None):
        auto_scaling_group_name = auto_scaling_group_name or self.AUTO_SCALING_GROUP
        autoscaling.put_scaling_policy (
            AutoScalingGroupName = auto_scaling_group_name,
            PolicyName = name,
            PolicyType = 'TargetTrackingScaling',
            TargetTrackingConfiguration = {'DisableScaleIn': False,
                                            'PredefinedMetricSpecification': {'PredefinedMetricType': metric_type},
                                            'TargetValue': value}
        )

    def get_elb_targets (self, target_group_arn = None):
        return elb2.describe_target_health (TargetGroupArn = target_group_arn or self.ELB_GROUP_ARN) ['TargetHealthDescriptions']

    def set_auto_scaling_group_range (self, min_ = None, max_ = None):
        return autoscaling.update_auto_scaling_group (
            AutoScalingGroupName = self.AUTO_SCALING_GROUP, MinSize = min_, MaxSize = max_
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
            time.sleep (30)
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

    def register_target (self, inst, target_group_arn = None):
        print ('registering new elb2 member: {}'.format (inst.id))
        elb2.register_targets (
            TargetGroupArn = target_group_arn or self.ELB_GROUP_ARN,
            Targets = [{'Id': inst.id, 'Port': port}]
        )

    def get_instances_by_image (self, image):
        return list (ec2.instances.filter(Filters=[{'Name': 'image-id', 'Values': [image.id]}]))

    def get_old_instances_by_image (self, new_image):
        news = [inst.id for inst in self.get_instances_by_image (new_image) if inst.state ['Name'] == 'running']
        valids = [ t ['Target']['Id'] for t in self.get_elb_targets () if t ['TargetHealth']['State'] != 'draining' ]
        return [ inst for inst in ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': [self.EC2_NAME]}]) if inst.id not in news and inst.id in valids and inst.state ['Name'] == 'running']

    def rescale (self, image, current_count, desired_count):
        def runnings ():
            return [ deployed.id for deployed in self.get_instances_by_image (image) if deployed.state ['Name'] == 'running' ]

        new_instances = runnings ()
        valids = [ t ['Target']['Id'] for t in self.get_elb_targets () if t ['Target']['Id'] in new_instances and t ['TargetHealth']['State'] != 'draining' ]
        exists_new_instances = len (valids)

        self.set_auto_scaling_group_range (current_count + desired_count, current_count + desired_count)
        print ('desired new isntance count: {}'.format (desired_count))
        for i in range (20):
            new_instances = runnings ()
            print ('- found {} new versioned instances, target is {}'.format (len (new_instances), exists_new_instances + desired_count))
            if len (new_instances) >= (exists_new_instances + desired_count) * 0.75:
                print ('{} new running instances fulfill minimum requirements'.format (len (new_instances)))
                break
            time.sleep (30)

        for i in range (20):
            new_instances = runnings ()
            valids = [ t ['Target']['Id'] for t in self.get_elb_targets () if t ['Target']['Id'] in new_instances and t ['TargetHealth']['State'] in ('healthy', 'draining') ]
            print ('- healthy / new instances: {} / {}'.format (len (valids), len (new_instances)))
            if len (valids) > len (new_instances) * 0.75:
                print ('{} healthy instances fulfill minimum requirements'.format (len (valids)))
                break
            time.sleep (30)

        self.set_auto_scaling_group_range (current_count, current_count)
        return new_instances

    def cleanup (self):
        print ('cleanup load balancer...')
        elbs = [e for e in elb2.describe_load_balancers () ["LoadBalancers"] if e ['LoadBalancerName'] == self.ELB]
        if elbs:
            elb2.delete_load_balancer (LoadBalancerArn=elbs [0]['LoadBalancerArn'])

        print ('cleanup auto scaler...')
        if autoscaling.describe_auto_scaling_groups () ["AutoScalingGroups"]:
            autoscaling.delete_auto_scaling_group (AutoScalingGroupName = self.AUTO_SCALING_GROUP, ForceDelete = True)
            time.sleep (10.)

        print ('cleanup target group...')
        tgs = [e for e in elb2.describe_target_groups () ["TargetGroups"] if e ['TargetGroupName'] == self.ELB_TARGET]
        if tgs:
            elb2.delete_target_group (TargetGroupArn = tgs [0]['TargetGroupArn'])

        print ('cleanup instances...')
        for inst in ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': [self.EC2_NAME]}]):
            if inst.state ['Name'] == 'running':
                print ('- terminating instance: {}'.format (inst.id))
                inst.terminate ()

