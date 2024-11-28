from django.db import models
from django.utils.text import slugify
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, blank=True)
    blog_duration_to_read = models.CharField(max_length=100,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumbnail_image = models.FileField()
    blog_content = models.TextField(default='')
    tags = models.ManyToManyField(Tag)
    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Check if slug exists and generate a unique one
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
