from django import forms
from .models import ReferenceProtein

class ReferenceProteinForm(forms.ModelForm):
    class Meta:
        model = ReferenceProtein
        fields = ['protein_id', "fasta_file", "selected_as_main_ref"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if ReferenceProtein.objects.filter(selected_as_main_ref=True).exists():
            self.fields['selected_as_main_ref'].widget = forms.HiddenInput()
            # Hide the 'selected_as_main_ref' field if an instance already exists
            self.fields['selected_as_main_ref'].widget = forms.HiddenInput()
            # Optionally, set the value to False
            self.fields['selected_as_main_ref'].initial = False
        else:
            # If no such instance exists, ensure the field is displayed
            self.fields['selected_as_main_ref'].widget = forms.CheckboxInput()