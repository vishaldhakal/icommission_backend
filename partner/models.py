from django.db import models

class Partner(models.Model):
    partner_name = models.CharField(max_length=100)
    partner_email = models.EmailField(blank=True)
    partner_phone = models.CharField(max_length=15)
    partner_address = models.CharField(blank=True,max_length=400)
    website = models.URLField(blank=True)
    partner_logo = models.FileField(upload_to='partner_logos/', blank=True)
    partner_detail = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.partner_name