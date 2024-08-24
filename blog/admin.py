from django.contrib import admin
from .models import Category,Post,Tag
from unfold.admin import ModelAdmin
from tinymce.widgets import TinyMCE
from django.db import models

admin.site.register(Category, ModelAdmin)
admin.site.register(Tag, ModelAdmin)

""" 
class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=500)
    blog_duration_to_read = models.CharField(max_length=100,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumbnail_image = models.FileField()
    blog_content = models.TextField(default='')
    tags = models.ManyToManyField(Tag)
    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title """


class PostAdmin(ModelAdmin):
   fieldsets = (
         (None, {
              'fields': (('title', 'category', 'thumbnail_image'), 'blog_content', 'tags',('meta_title', 'meta_description'))
         }),
    )
   def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'blog_content':
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, **kwargs)
   
admin.site.register(Post,PostAdmin)