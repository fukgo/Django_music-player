from django import forms
from .models import ContactModel
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = ['name','email_or_phone','message']