from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model

User = get_user_model()
class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('contracted', 'Contracted'),
        ('funded', 'Funded'),
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('overdue', 'Overdue'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=255)
    broker_of_record = models.CharField(max_length=255)
    deal_admin_email = models.EmailField()
    emergency_phone = models.CharField(max_length=20)
    upload_id = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf'])],
        help_text="Upload your Valid ID"
    )
    
    purchase_sale_agreement = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Upload Purchase and Sales Agreement (PDF only)"
    )
    
    mls_listing = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Upload SOLD MLS Listing (PDF only)"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application for {self.name} (ID: {self.upload_id})"

    class Meta:
        ordering = ['-submitted_at']