from django import forms
from payu.gateway import get_hash
from captcha.fields import CaptchaField, CaptchaTextInput,CaptchaAnswerInput
from .models import Query

PAYMENT_CHOICES = (
    ('PU', 'Debit/Credit Card (PayU Gateway)'),
    ('PP', 'PayPal')
)


class QueryForm(forms.ModelForm):
    captcha = CaptchaField(help_text='Type the characters you see in the picture', widget=CaptchaTextInput())

    class Meta:
        model = Query
        fields = "__all__"
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'query': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type your query', 'cols': 40, 'rows': 5}),
        }


class CheckoutForm(forms.Form):

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class PayUForm(forms.Form):
    # payu specific fields
    key = forms.CharField(widget=forms.HiddenInput())
    hash = forms.CharField(widget=forms.HiddenInput())  # Required

    # cart order related fields
    txnid = forms.CharField(widget=forms.HiddenInput())
    productinfo = forms.CharField(widget=forms.HiddenInput())
    amount = forms.DecimalField(decimal_places=2, widget=forms.HiddenInput())

    # buyer details
    firstname = forms.CharField(widget=forms.HiddenInput())
    lastname = forms.CharField(required=False, widget=forms.HiddenInput())
    email = forms.EmailField(widget=forms.HiddenInput())
    phone = forms.RegexField(regex=r'\d{10}', min_length=10, max_length=13, widget=forms.HiddenInput())
    address1 = forms.CharField(required=False, widget=forms.HiddenInput())
    address2 = forms.CharField(required=False, widget=forms.HiddenInput())
    city = forms.CharField(required=False, widget=forms.HiddenInput())
    state = forms.CharField(required=False, widget=forms.HiddenInput())
    country = forms.CharField(required=False, widget=forms.HiddenInput())
    zipcode = forms.RegexField(regex=r'\d{6}', min_length=6, max_length=6, required=False, widget=forms.HiddenInput())

    # merchant's side related fields
    furl = forms.URLField(widget=forms.HiddenInput())
    surl = forms.URLField(widget=forms.HiddenInput())
    curl = forms.URLField(required=False, widget=forms.HiddenInput())
    service_provider = forms.CharField(widget=forms.HiddenInput())
    codurl = forms.URLField(required=False, widget=forms.HiddenInput())
    touturl = forms.URLField(required=False, widget=forms.HiddenInput())
    udf1 = forms.CharField(required=False, widget=forms.HiddenInput())
    udf2 = forms.CharField(required=False, widget=forms.HiddenInput())
    udf3 = forms.CharField(required=False, widget=forms.HiddenInput())
    udf4 = forms.CharField(required=False, widget=forms.HiddenInput())
    udf5 = forms.CharField(required=False, widget=forms.HiddenInput())
    pg = forms.CharField(required=False, widget=forms.HiddenInput())
    drop_category = forms.CharField(required=False, widget=forms.HiddenInput())
    custom_note = forms.CharField(required=False, widget=forms.HiddenInput())
    note_category = forms.CharField(required=False, widget=forms.HiddenInput())
