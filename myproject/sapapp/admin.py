from django.contrib import admin

# Register your models here.
from .models import ReferenceProtein

class ReferenceProteinAdmin(admin.ModelAdmin):
    list_display = ('protein_id', 'uploaded_at', 'selected_as_main_ref')  # Fields to display in the list view
    list_filter = ('selected_as_main_ref',)  # Add filters for the admin list view
    search_fields = ('protein_id',)  # Add search capability

admin.site.register(ReferenceProtein, ReferenceProteinAdmin)