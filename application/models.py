from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from decimal import Decimal
from datetime import datetime

User = get_user_model()

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
        ('Lease', 'Lease'),
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
                # Remove status from changes if present
                changes.pop('status', None)
                
                # Only create change request if there are other changes
                if changes:
                    ChangeRequest.objects.create(
                        content_type=ContentType.objects.get_for_model(self),
                        object_id=self.pk,
                        changes=changes
                    )
            super().save(*args, **kwargs)

    def get_changes(self):
        if not self.pk:
            return {}
        old_instance = Application.objects.get(pk=self.pk)
        changes = {}
        for field in self._meta.fields:
            if getattr(self, field.name) != getattr(old_instance, field.name):
                changes[field.name] = getattr(self, field.name)
        return changes

    def get_pending_changes(self):
        return ChangeRequest.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk,
            status='Pending'
        )

    def approve_changes(self, change_request):
        if change_request.content_type == ContentType.objects.get_for_model(self) and change_request.object_id == self.pk:
            # Get the fields being changed in current change request
            changing_fields = set(change_request.changes.keys())
            
            # Reject only pending changes that modify the same fields
            pending_changes = self.get_pending_changes().exclude(pk=change_request.pk)
            for pending_change in pending_changes:
                pending_fields = set(pending_change.changes.keys())
                if pending_fields & changing_fields:  # If there's any intersection
                    pending_change.status = 'Rejected'
                    pending_change.save()
            
            # Apply the approved changes
            for field, value in change_request.changes.items():
                field_type = self._meta.get_field(field)
                
                # Handle date fields
                if isinstance(field_type, models.DateField) and value:
                    date_value = datetime.fromisoformat(value).date()
                    setattr(self, field, date_value)
                # Handle decimal fields
                elif isinstance(field_type, models.DecimalField) and value:
                    setattr(self, field, Decimal(str(value)))
                # Handle other fields
                else:
                    setattr(self, field, value)
            
            self.approved_version = change_request
            super().save()
            change_request.status = 'Approved'
            change_request.approved_at = timezone.now()
            change_request.save()

    def reject_changes(self, change_request):
        if change_request.content_type == ContentType.objects.get_for_model(self) and change_request.object_id == self.pk:
            change_request.status = 'Rejected'
            change_request.save()

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
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    changes = models.JSONField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='change_requests_created')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='change_requests_approved')
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Change request for {self.content_object} - {self.get_status_display()}"

    class Meta:
        ordering = ['-created_at']
