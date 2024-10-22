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

    def __str__(self):
        return f"Application for {self.user.first_name} {self.user.last_name}"

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