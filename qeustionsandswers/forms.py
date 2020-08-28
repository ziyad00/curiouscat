from django import forms
from QA.models import Reply, QA

class QAForms(forms.ModelForm):
    question = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder': 'اكتب سؤالك'}), label='')
    class Meta:
        model = QA
        fields = ('question',)
       


class ReplyForms(forms.ModelForm):
    reply = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder': 'اكتب جوابك'}), label='')
    class Meta:
        model = Reply
        fields = ('reply',)