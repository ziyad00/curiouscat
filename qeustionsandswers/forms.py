from django import forms

class QAForms(forms.Form):
    question = forms.CharField(label='اكتب سؤالك', widget=forms.Textarea)