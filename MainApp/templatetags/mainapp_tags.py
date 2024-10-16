from django import template
from MainApp.models import Snippet


register = template.Library()


@register.simple_tag(name='delete_snippet_tag')
def delete_snippet_tag(snippet_id):
    Snippet.objects.get(id=snippet_id).delete()
    return