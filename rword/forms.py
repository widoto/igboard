from importlib.resources import contents
from django import forms
from .models import SentenceList

#일반인
class RSentencesWriteForm(forms.Form):
    sentence = forms.CharField(error_messages={'required':"문장을 입력하세요"}, label="문장")
    contents = forms.CharField(error_messages={'required':"문장을 입력하세요"}, widget=forms.Textarea, label='설명')
