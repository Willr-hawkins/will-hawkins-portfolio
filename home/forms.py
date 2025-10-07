from django import forms
from. models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'phone_number', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholer': 'Your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '07123 456789 (optional)',
                'required': False
            }),
            'message': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your message here...',
                'required': True
            }),
        }
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number (Optional)',
            'message': 'Message',
        }

    def clean_message(self):
        """ Ensure message has minimum length. """
        message = self.cleaned_data.get('message')
        if len(message.strip()) < 10:
            raise ValidationError("Please provide a mesage with at least 10 characters.")
        return message 
    
    def clean_full_name(self):
        """ Basic name validation """
        full_name = self.cleaned_data.get('full_name')
        if len(full_name.strip()) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return full_name