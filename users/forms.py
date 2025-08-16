from dataclasses import field
from django import forms
from .models import CustomUserModel

class CustomUserCreationForm(forms.ModelForm):
    """
    Create user form (with hash password)
    """
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUserModel
        fields = ('email', 'username')

        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password'])
            if commit:
                user.save()
            return user



class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUserModel
        fields = '__all__'