from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from decimal import Decimal
import datetime
import json

User = get_user_model()

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)

class Application(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Contracted', 'Contracted'),
        ('Funded', 'Funded'),
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Overdue', 'Overdue'),
    ]

    TRANSACTION_TYPES = [
        ('Resale', 'Resale'),
        ('Commercial', 'Commercial'),
        ('Pre-construction', 'Pre-construction'),
        ('Line of Credit', 'Line of Credit'),
        ('Lease', 'Lease'),
        ('Royalty Loan', 'Royalty Loan'),
        ('Term Loan', 'Term Loan'),
    ]

    TRANSACTIONS= [
        ('Single', 'Single'),
        ('Multiple', 'Multiple'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, default='Purchase')
    transaction_address = models.CharField(max_length=255, null=True, blank=True)
    deal_commission_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    purchase_commission_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    advance_payout_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    commission_amount_requested = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_fee_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    advance_date = models.DateField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)
    transaction_count = models.CharField(max_length=20, choices=TRANSACTIONS, default='Single')

    approved_version = models.ForeignKey('ChangeRequest', null=True, blank=True, on_delete=models.SET_NULL, related_name='current_application')

    def __str__(self):
        return f"Application for {self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        else:
            changes = self.get_changes()
            if changes:
                # Get the user from the current request
                from django.contrib.admin.sites import site
                from django.contrib.auth import get_user_model
                from threading import current_thread
                
                request = None
                thread = current_thread()
                if hasattr(thread, 'request'):
                    request = thread.request
                else:
                    for thread_local in site._registry.values():
                        if hasattr(thread_local, 'request'):
                            request = thread_local.request
                            break

                User = get_user_model()
                user = None
                if request and hasattr(request, 'user'):
                    user = request.user
                else:
                    user = User.objects.filter(is_superuser=True).first()

                if user and changes:
                    ChangeRequest.objects.create(
                        content_type=ContentType.objects.get_for_model(self),
                        object_id=self.pk,
                        changes=changes,
                        created_by=user,
                        status='Applied'
                    )
            super().save(*args, **kwargs)

    def get_changes(self):
        if not self.pk:
            return {}
        
        old_instance = Application.objects.get(pk=self.pk)
        changes = {}
        tracked_fields = [
            'transaction_type', 'transaction_address', 'deal_commission_amount',
            'purchase_commission_amount', 'advance_payout_amount', 'discount_fee_amount',
            'advance_date', 'closing_date', 'status', 'transaction_count'
        ]
        
        # Define choice fields
        choice_fields = ['transaction_type', 'status', 'transaction_count']
        
        for field in tracked_fields:
            old_value = getattr(old_instance, field)
            new_value = getattr(self, field)
            
            # Skip if values are the same
            if old_value == new_value:
                continue
            
            # Handle different types of values
            if field in choice_fields:
                # Handle choice fields directly as strings
                changes[field] = str(new_value) if new_value else None
            elif isinstance(new_value, (int, float, str, bool)) or new_value is None:
                changes[field] = new_value
            elif isinstance(new_value, Decimal):
                changes[field] = str(new_value)
            elif isinstance(new_value, datetime.date):
                changes[field] = new_value.isoformat() if new_value else None
                old_value = old_value.isoformat() if old_value else None
                # Only add to changes if the formatted values are different
                if old_value != changes[field]:
                    changes[field] = changes[field]
                else:
                    del changes[field]
            else:
                # For any other types, convert to string
                changes[field] = str(new_value) if new_value is not None else None
            
        return changes

    class Meta:
        ordering = ['-submitted_at']

class ApplicationComment(models.Model):
    COMMENT_TYPES = [
        ('Internal', 'Internal'),
        ('External', 'External'),
    ]
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(default='')
    comment_type = models.CharField(max_length=20, choices=COMMENT_TYPES, default='Internal')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_comment_type_display()} comment for {self.application}"

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('Valid ID', 'Valid ID'),
        ('Purchase and Sale Agreement', 'Purchase and Sale Agreement'),
        ('SOLD MLS Listing', 'SOLD MLS Listing'),
        ('Annual Commission Statement', 'Annual Commission Statement'),
        ('T4A', 'T4A'),
        ('VOID Cheque', 'VOID Cheque'),
        ('Direct Deposit Form', 'Direct Deposit Form'),
        ('Waivers of Conditions', 'Waivers of Conditions'),
        ('Trade Record Sheet', 'Trade Record Sheet'),
        ('Deposit Cheque/Receipt', 'Deposit Cheque/Receipt'),
        ('Exclusive Listing Agreement or Confirmation of Cooperation', 'Exclusive Listing Agreement or Confirmation of Cooperation'),
        ("Signed Broker Referral with Payment Schedule", "Signed Broker Referral with Payment Schedule"),
        ("Receiving/Referral Agreement (if applicable)", "Receiving/Referral Agreement (if applicable)"),
        ("Signed Buyer Rep/RECO Info Guide (if direct deal)", "Signed Buyer Rep/RECO Info Guide (if direct deal)"),
        ("Signed Trade Record Sheet & Pending Trade Report", "Signed Trade Record Sheet & Pending Trade Report"),
        ("Mortgage Pre-approval", "Mortgage Pre-approval"),
        ("Developer's Email Confirmation", "Developer's Email Confirmation"),
        ('Other', 'Other'),
    ]

    DOCUMENT_STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=500, choices=DOCUMENT_TYPES)
    status = models.CharField(max_length=20, choices=DOCUMENT_STATUS, default='Pending')
    file = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} for {self.application}"

    class Meta:
        ordering = ['-uploaded_at']

class Note(models.Model):
    NOTE_TYPES = [
        ('Internal', 'Internal'),
        ('External', 'External'),
    ]

    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='notes')
    note_type = models.CharField(max_length=10, choices=NOTE_TYPES)
    content = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_note_type_display()} note for {self.document}"

    class Meta:
        ordering = ['-created_at']

class ChangeRequest(models.Model):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),  # Simplified status - only tracking changes
    ]

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    changes = models.JSONField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='change_requests_created')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Applied')

    def __str__(self):
        return f"Change history for {self.content_object} at {self.created_at}"

    class Meta:
        ordering = ['-created_at']
