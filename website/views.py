from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import LeadForm

class HomePageView(TemplateView):
    template_name = 'home.html'

import os
from django.conf import settings

class ServicesPageView(TemplateView):
    template_name = 'services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images_dir = os.path.join(settings.BASE_DIR, 'static', 'images')
        gallery_images = []
        try:
            for filename in os.listdir(images_dir):
                if filename.startswith('gallery-'):
                    # Create a readable title from filename
                    # e.g. gallery-commercial-ceiling-reference.png -> Commercial Ceiling Reference
                    title = filename.replace('gallery-', '').replace('.png', '').replace('.jpg', '').replace('-', ' ').title()
                    gallery_images.append({
                        'url': f'images/{filename}',
                        'title': title
                    })
        except FileNotFoundError:
            pass
        context['gallery_images'] = gallery_images
        return context

class DealersPageView(TemplateView):
    template_name = 'dealers.html'

class ContactPageView(FormView):
    template_name = 'contact.html'
    form_class = LeadForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thank you! Your request has been received. We will contact you shortly.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your submission. Please check the form and try again.")
        return super().form_invalid(form)

class AboutPageView(TemplateView):
    template_name = 'about.html'
