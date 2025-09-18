
from django.urls import path
from .views import *

urlpatterns = [
    path('styles/create/', StyleListCreateView.as_view(), name='style-list-create'),
    path('styles/my-styles/', user_styles, name='user-styles'),
    path('styles/<slug:slug>/', StyleDetailView.as_view(), name='style-detail'),
    path('styles/<slug:slug>/update/', StyleUpdateView.as_view(), name='style-update'),
    path('styles/<slug:slug>/delete/', StyleDeleteView.as_view(), name='style-delete'),
    path('styles/search/', style_search, name='style-search'),
    path('styles/', StyleListView.as_view(), name='style-list'),
]