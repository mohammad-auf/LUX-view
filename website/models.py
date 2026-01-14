import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# ============================================
# CUSTOM USER MODEL WITH ROLES
# ============================================

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    Supports three roles: Installer, Dealer, and Admin
    """
    
    ROLE_CHOICES = [
        ('INSTALLER', 'Installer'),
        ('DEALER', 'Dealer'),
        ('ADMIN', 'Admin (LuxView)'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='INSTALLER')
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


# ============================================
# DEALER COMPANY MODEL
# ============================================

class DealerCompany(models.Model):
    """
    Represents a dealer company that can create jobs and assign installers
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    service_area = models.CharField(max_length=200, blank=True, null=True, 
                                    help_text="Geographic area served by this dealer")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'dealer_companies'
        verbose_name = 'Dealer Company'
        verbose_name_plural = 'Dealer Companies'
        ordering = ['name']


# ============================================
# INSTALLER PROFILE MODEL
# ============================================

class InstallerProfile(models.Model):
    """
    Profile for installers who perform installation jobs
    One-to-one relationship with User model
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='installer_profile',
        limit_choices_to={'role': 'INSTALLER'}
    )
    display_name = models.CharField(max_length=100, 
                                    help_text="Name displayed to dealers and customers")
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True, 
                                    help_text="Whether installer is currently available for jobs")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.display_name} - {'Active' if self.is_active else 'Inactive'}"
    
    class Meta:
        db_table = 'installer_profiles'
        verbose_name = 'Installer Profile'
        verbose_name_plural = 'Installer Profiles'
        ordering = ['display_name']


# ============================================
# DEALER PROFILE MODEL
# ============================================

class DealerProfile(models.Model):
    """
    Profile for dealers who create and manage jobs
    One-to-one relationship with User model
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='dealer_profile',
        limit_choices_to={'role': 'DEALER'}
    )
    dealer_company = models.ForeignKey(
        DealerCompany, 
        on_delete=models.CASCADE, 
        related_name='dealers'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.dealer_company.name}"
    
    class Meta:
        db_table = 'dealer_profiles'
        verbose_name = 'Dealer Profile'
        verbose_name_plural = 'Dealer Profiles'
        ordering = ['dealer_company__name', 'user__first_name']


# ============================================
# JOB MODEL
# ============================================

class Job(models.Model):
    """
    Represents an installation or service job
    Created by dealers and assigned to installers
    """
    
    SERVICE_TYPE_CHOICES = [
        ('MEASURE', 'Measure'),
        ('SERVICE_CALL', 'Service Call'),
        ('BLINDS_SHADES_INSTALL', 'Blinds/Shades Install'),
        ('DRAPERY_SHUTTERS_INSTALL', 'Drapery/Shutters Install'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PAID', 'Paid'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relationships
    dealer_company = models.ForeignKey(
        DealerCompany, 
        on_delete=models.CASCADE, 
        related_name='jobs'
    )
    assigned_installer = models.ForeignKey(
        InstallerProfile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_jobs',
        help_text="Installer assigned to this job"
    )
    
    # Job Information
    title = models.CharField(max_length=200)
    service_type = models.CharField(max_length=30, choices=SERVICE_TYPE_CHOICES)
    
    # Address Information
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    
    # Additional Details
    notes = models.TextField(blank=True, null=True, 
                            help_text="Additional notes or special instructions")
    
    # Status Fields
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='UNPAID')
    
    # Timestamps
    scheduled_date = models.DateTimeField(null=True, blank=True, 
                                         help_text="When the job is scheduled to be performed")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    @property
    def full_address(self):
        """Returns the complete formatted address"""
        return f"{self.address}, {self.city}, {self.state} {self.zip_code}"
    
    class Meta:
        db_table = 'jobs'
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['dealer_company', 'status']),
            models.Index(fields=['assigned_installer', 'status']),
        ]


# ============================================
# JOB PHOTO MODEL
# ============================================

class JobPhoto(models.Model):
    """
    Photos uploaded for jobs (before/after installation)
    Supports future integration with Square and invoicing
    """
    
    PHOTO_TYPE_CHOICES = [
        ('BEFORE', 'Before'),
        ('AFTER', 'After'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(
        Job, 
        on_delete=models.CASCADE, 
        related_name='photos'
    )
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='uploaded_photos'
    )
    photo_type = models.CharField(max_length=10, choices=PHOTO_TYPE_CHOICES)
    image = models.ImageField(upload_to='job_photos/%Y/%m/%d/', 
                             help_text="Upload job photo")
    caption = models.CharField(max_length=200, blank=True, null=True, 
                              help_text="Optional description of the photo")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.job.title} - {self.get_photo_type_display()} ({self.created_at.strftime('%Y-%m-%d')})"
    
    class Meta:
        db_table = 'job_photos'
        verbose_name = 'Job Photo'
        verbose_name_plural = 'Job Photos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['job', 'photo_type']),
        ]


# ============================================
# LEGACY LEAD MODEL (from Phase 1)
# ============================================

class Lead(models.Model):
    """
    Legacy model for marketing website leads
    Kept for backward compatibility with Phase 1
    """
    
    SERVICE_CHOICES = [
        ('general', 'General Inquiry'),
        ('blinds', 'Window Blinds'),
        ('shades', 'Roller/Solar Shades'),
        ('motorized', 'Motorized Solutions'),
        ('commercial', 'Commercial Project'),
        ('custom', 'Custom Window Treatments'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default='general')
    city = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service}"
    
    class Meta:
        db_table = 'leads'
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        ordering = ['-created_at']
