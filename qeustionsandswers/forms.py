from django import forms
from QA.models import Reply, QA

class QAForms(forms.ModelForm):
    question = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder': 'اكتب سؤالك'}), label='')
    form_type = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = QA
        fields = ('question',)
    def __init__(self, *args, **kwargs):
        super(QAForms, self).__init__(*args, **kwargs)

        self.fields['form_type'].required = False
       


class ReplyForms(forms.ModelForm):
    reply = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder': 'اكتب جوابك'}), label='')
    r_id = forms.IntegerField(widget=forms.HiddenInput(), required=False, )
    form_type = forms.CharField(widget=forms.HiddenInput(), required=False)

    
    class Meta:
        model = Reply
        fields = ('reply',)
    def __init__(self, *args, **kwargs):
        super(ReplyForms, self).__init__(*args, **kwargs)

        self.fields['r_id'].required = False
        self.fields['form_type'].required = False