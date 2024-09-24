from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username',required=True,widget=forms.TextInput(attrs={'class' : 'form-control footr-input margin-b-20','placeholder':'Username'}))
    password1 = forms.CharField(label = "Parol", required=True,widget=forms.PasswordInput(attrs={'class' : 'form-control footer-input margin-b-20','placeholder':'Parol'}))

    password2 = forms.CharField(label="Takroriy parol",required=True,widget=forms.PasswordInput(attrs={'class' : 'form-control footer_input margin-b-20','placeholder':'Takroriy parol'}))

    email = forms.EmailField(label = "Email", required=True, widget=forms.TextInput(attrs={'class' : 'form-control footer-input margin-b-20','placeholder':'Email'}))

    first_name = forms.CharField(label = "Ism", required=True, widget=forms.TextInput(attrs={'class' : 'form-control footer-input margin-b-20','placeholder':'Ism'}))

    last_name = forms.CharField(label = "Familiya", required=True, widget=forms.TextInput(attrs={'class' : 'form-control footer-input margin-b-20','placeholder':'Familiya'}))

    class Meta:
        model = User
        fields = ("first_name","last_name",  "email", "username", "password1", "password2", )

    def save(self,commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
        return user