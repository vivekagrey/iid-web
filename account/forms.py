from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account
from django.contrib.auth import authenticate
from phonenumber_field import formfields, widgets

highest_qualification_choices =(
    ("No formal education", "No formal education"),
    ("Primary Education", "Primary Education"),
    ("Secondary Education", "Secondary Education"),
    ("Bachelor's Degree", "Bachelor's Degree"),
    ("Master's Degree", "Master's Degree"),
)


class SignUpForm(UserCreationForm):
    phone = formfields.PhoneNumberField(widget=widgets.PhoneNumberPrefixWidget(), initial='+91')

    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name', 'phone')   # Fields while signing up through the website


class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                # print('Not authenticated')
                raise forms.ValidationError("Invalid Details")

            # if email and password:
            #     user = authenticate(username = email, password = password)
            #     if not user:
            #         raise forms.ValidationError("This user does not exist..")
            #
            #     if not user.check_password(password):
            #         raise forms.ValidationError("Incorrect password...")
            #
            #     if not user.is_active:
            #         raise forms.ValidationError("This user does not appear to be active.")


class ProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1920,2020)), label="Date of Birth")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hq'].widget.attrs.update({'class': 'form-control'})
        self.fields['country'].widget.attrs.update({'class': 'form-control'})
        self.fields['dob'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Account
        fields = ('country', 'dob', 'hq', 'pro_pic')
