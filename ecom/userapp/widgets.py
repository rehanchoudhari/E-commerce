from django.forms import widgets
from django.utils.safestring import mark_safe


class CustomeImagesForProfile(widgets.FileInput):

    def render(self, name, value, attrs=None, **kwargs):
        defualt_html = super().render(name, value, attrs, **kwargs)
        image_html = mark_safe(f'<img src="{value.url}" width="200" />')
        return f'{image_html}{defualt_html}'