from django.contrib import admin
from .models import Lead, PartnerApplication

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('service', 'created_at')

@admin.register(PartnerApplication)
class PartnerApplicationAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'email', 'business_type', 'created_at')
    search_fields = ('company', 'name', 'email', 'phone')
    list_filter = ('business_type', 'created_at')
