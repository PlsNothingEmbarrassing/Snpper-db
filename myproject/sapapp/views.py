from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import ReferenceProteinForm
from django.views import View
from .models import *
import requests
# Create your views here.


    
def upload_protein(request):
        form = ReferenceProteinForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('protein_dashboard')
        else:
            form = ReferenceProteinForm()
        return render(request, "upload_protein.html", {"form": form})

def protein_dashboard_view(request):
    proteins = ReferenceProtein.objects.prefetch_related('sap_addresses').all()

    context = {
        'proteins': proteins
    }
    return render(request, "protein_dashboard.html", context)

def delete_protein(request, protein_id):
     protein = get_object_or_404(ReferenceProtein, id= protein_id)     
     if request.method =="POST":
          protein.delete()
          print("Article Deleted")
          return redirect(reverse("protein_dashboard"))
     return redirect(reverse('protein_dashboard'))
    