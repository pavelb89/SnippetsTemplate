from django.contrib import admin

from MainApp.models import Snippet, Comment


# Register your models here.

# 1 variant
# admin.site.register(Snippet)
# admin.site.register(Comment)

# 2 variant
@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ['name', 'lang', 'code', 'public']
    list_filter = ['lang', 'creation_date']
    
    search_fields = ['name', 'code']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['snippet', 'text', 'creation_date', 'author']
     
    ordering = ['creation_date', 'author'] 
    
    search_fields = ['text']