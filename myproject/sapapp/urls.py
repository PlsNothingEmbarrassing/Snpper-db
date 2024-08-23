
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.protein_dashboard_view, name='protein_dashboard'),
    path("upload_protein/", views.upload_protein, name="upload_protein"),
    path("protein_dashboard/", views.protein_dashboard_view, name = "protein_dashboard"),
    path('delete_protein/<int:protein_id>/', views.delete_protein, name='delete_protein'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)