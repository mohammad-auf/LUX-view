from django.urls import path
from .views import HomePageView, ServicesPageView, DealersPageView, ContactPageView, AboutPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('services/', ServicesPageView.as_view(), name='services'),
    path('dealers/', DealersPageView.as_view(), name='dealers'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('about/', AboutPageView.as_view(), name='about'),
]
