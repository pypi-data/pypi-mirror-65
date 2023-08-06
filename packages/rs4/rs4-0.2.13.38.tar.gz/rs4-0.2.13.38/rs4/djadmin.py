from django.contrib import admin
from django.utils.safestring import mark_safe
from django.forms import Widget
import mimetypes

def set_title (title):
    admin.site.site_title = title
    admin.site.site_header = "{}".format (title)
    admin.site.index_title = "{} Management Console".format (title)

def get_type (path):
    return mimetypes.guess_type (os.path.basename (path))[0]

def ImageWidget (width = 360):
    class _ImageWidget(Widget):
        def render(self, name, value, **noneed):
            return value and mark_safe ('<img src="{}" width="{}">'.format (value, width)) or 'No Image'
    return _ImageWidget

class LinkWidget(Widget):
    def render(self, name, value, **noneed):
        return value and mark_safe ('<a href="{}">{}</a> [<a href="{}" target="_blank">새창</a>]'.format (value, value, value)) or 'No Image'

def VideoWidget (video_width = 320, video_height = 240):
    class _VideoWidget(Widget):
        def render(self, name, value, **noneed):
            return value and mark_safe (
                '<video width="{}" height="{}" controls><source src="{}" type="{}"></video>'.format (
                    video_width, video_height, value, get_type (value)
                )
            ) or 'No Video'
    return _VideoWidget

class AudioWidget(Widget):
    def render(self, name, value, **noneed):
        return value and mark_safe ('<audio controls><source src="{}" type="{}"></audio>'.format (
            value, get_type (value)
            )
        ) or 'No Audio'


class ModelAdmin (admin.ModelAdmin):
    image_width = 320
    video_width = 320
    enable_add = True
    enable_delete = True
    enable_change = True
    def has_add_permission(self, request, obj=None):
        return self.enable_add

    def has_delete_permission(self, request, obj=None):
        return self.enable_delete

    def has_change_permission(self, request, obj=None):
        return self.enable_change

    def formfield_for_dbfield (self, db_field, request, **kwargs):
        if 'widget' not in kwargs:
            if db_field.name.endswith ('image'):
                kwargs ['widget'] = ImageWidget (self.image_width)
                return db_field.formfield(**kwargs)
            elif db_field.name.endswith ('video'):
                kwargs ['widget'] = VideoWidget (self.video_width)
                return db_field.formfield(**kwargs)
            elif db_field.name.endswith ('audio'):
                kwargs ['widget'] = AudioWidget
                return db_field.formfield(**kwargs)
            elif db_field.name.endswith ('url'):
                kwargs ['widget'] = LinkWidget
                return db_field.formfield(**kwargs)
        return super ().formfield_for_dbfield (db_field, request, **kwargs)