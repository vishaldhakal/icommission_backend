from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import datetime
from django.db.models import Sum, Avg

class DealType(models.TextChoices):
    PRE_CONSTRUCTION = 'Pre-construction', 'Pre-construction'
    RESALE = 'Resale', 'Resale'
    COMMERCIAL = 'Commercial', 'Commercial'
    LINE_OF_CREDIT = 'Line of Credit', 'Line of Credit'
    ROYALTY_LOAN = 'Royalty Loan', 'Royalty Loan'
    TERM_LOAN = 'Term Loan', 'Term Loan'
    BRIDGE_LOAN_PRIVATE = 'Bridge Loan (Private)', 'Bridge Loan (Private)'

class DealCategory(models.TextChoices):
    SINGLE = 'Single', 'Single'
    MULTIPLE = 'Multiple', 'Multiple'

class DealStatus(models.TextChoices):
    OPEN = 'Open', 'Open'
    CLOSED = 'Closed', 'Closed'

class Deal(models.Model):
    file = models.CharField(max_length=255, unique=True, db_index=True)
    date = models.DateField(db_index=True)
    category = models.CharField(
        max_length=255,
        choices=DealCategory.choices,
        default=DealCategory.SINGLE,
        db_index=True
    )
    transaction_address = models.CharField(max_length=500)
    name = models.CharField(max_length=255, db_index=True)
    company = models.CharField(max_length=255, db_index=True)
    type = models.CharField(
        max_length=255,
        choices=DealType.choices,
        db_index=True
    )
    purchased_commission_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        db_index=True
    )
    purchase_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    closing_date = models.DateField(db_index=True)
    agent_commission = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    internal_notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=255,
        choices=DealStatus.choices,
        default=DealStatus.OPEN,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_term_days(self):
        return (self.closing_date - self.date).days if self.closing_date and self.date else 0

    def calculate_discount_fee(self):
        return float(self.purchased_commission_amount - self.purchase_price)

    def calculate_rate(self):
        term_days = self.calculate_term_days()
        if term_days > 0 and self.purchased_commission_amount:
            discount_fee = self.calculate_discount_fee()
            return float((discount_fee / float(self.purchased_commission_amount) / term_days * 365) * 100)
        return 0

    def calculate_advance_ratio(self):
        if self.agent_commission and float(self.agent_commission) > 0:
            return float(self.purchased_commission_amount / self.agent_commission)
        return 0

    def calculate_countdown(self):
        if self.closing_date:
            return (self.closing_date - timezone.now().date()).days
        return 0

    def __str__(self):
        return f"{self.file} - {self.name}"

    class Meta:
        ordering = ['date']
        indexes = [
            models.Index(fields=['file']),
            models.Index(fields=['status']),
            models.Index(fields=['type']),
            models.Index(fields=['date']),
            models.Index(fields=['closing_date']),
            models.Index(fields=['name']),
            models.Index(fields=['company']),
        ]

class PortfolioSettings(models.Model):
    exposure_basis = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=1500000.00,
        validators=[MinValueValidator(0)]
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Portfolio Settings"
