from django.db import models

class Lead(models.Model):
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
