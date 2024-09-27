from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model

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
        ('Purchase', 'Purchase'),
        ('Sale', 'Sale'),
        ('Refinance', 'Refinance'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    deal_administrator_name = models.CharField(max_length=100, null=True, blank=True)
    deal_administrator_email = models.EmailField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, default='Purchase')
    transaction_address = models.CharField(max_length=255, null=True, blank=True)
    total_commission_amount_requested = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_commission_amount_received = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def __str__(self):
        return f"Application for {self.user.first_name} {self.user.last_name}"

    class Meta:
        ordering = ['-submitted_at']

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
        ('Other', 'Other'),
    ]

    DOCUMENT_STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    status = models.CharField(max_length=20, choices=DOCUMENT_STATUS, default='Pending')
    file = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_document_type_display()} for {self.application.user.first_name} {self.application.user.last_name}"

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