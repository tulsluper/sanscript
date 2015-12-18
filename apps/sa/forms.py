from django import forms

class EmailForm(forms.Form):
    to_email = forms.EmailField(required=True)
    from_email = forms.EmailField(widget = forms.HiddenInput())
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea)
