from django import forms
from .models import Lead, PartnerApplication

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'service', 'city', 'message']

class PartnerApplicationForm(forms.ModelForm):
    class Meta:
        model = PartnerApplication
        fields = ['company', 'name', 'email', 'phone', 'business_type']

