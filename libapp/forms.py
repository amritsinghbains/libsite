from django import forms
from libapp.models import Suggestion, Libuser

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        exclude = ['num_interested']
        labels = {'cost':'Estimated Cost in Dollars'}

        title = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'max_length': 100}))
        pubyr = forms.IntegerField(widget=forms.NumberInput())
        type = forms.IntegerField(widget=forms.NumberInput())
        cost = forms.IntegerField(widget=forms.NumberInput())
        comments = forms.CharField(widget=forms.Textarea())


class SearchlibForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter Title"}),label='',required=False)
    author = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter Author/Maker"}), label='',required=False)

class LoginForm(forms.Form):
    username = forms.CharField(widget=
                               forms.TextInput(
                                   attrs={'required': True, 'class': 'form-control', 'placeholder': 'Enter Username'}),
                               label="")
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Enter Password'}),
        label="")

class LibuserForm(forms.ModelForm):
    class Meta:
        model = Libuser
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        exclude = ['address', 'city', 'province']

    username = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'max_length': 100}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True, 'max_length': 100}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'max_length': 100}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'max_length': 100}))
    email = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'max_length': 100}))
