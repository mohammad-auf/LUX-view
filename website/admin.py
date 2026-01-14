from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('service', 'created_at')
