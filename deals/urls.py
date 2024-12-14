from django.urls import path
from .views import (
    DealListCreateView,
    DealRetrieveUpdateDestroyView,
    PortfolioSettingsListCreateView,
    PortfolioSettingsRetrieveUpdateDestroyView,
    import_deals,
    export_deals,
    get_analytics
)

urlpatterns = [
    # Deal endpoints
    path('deals/', DealListCreateView.as_view(), name='deal-list-create'),
    path('deals/<int:pk>/', DealRetrieveUpdateDestroyView.as_view(), name='deal-detail'),
    path('deals/import/', import_deals, name='deal-import'),
    path('deals/export/', export_deals, name='deal-export'),
    path('deals/analytics/', get_analytics, name='deal-analytics'),
    
    # Portfolio Settings endpoints
    path('portfolio-settings/', PortfolioSettingsListCreateView.as_view(), name='portfolio-settings-list-create'),
    path('portfolio-settings/<int:pk>/', PortfolioSettingsRetrieveUpdateDestroyView.as_view(), name='portfolio-settings-detail'),
]
