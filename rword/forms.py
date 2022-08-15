from django import forms
from .models import SentenceList
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

#일반인
class RSentencesWriteForm(forms.ModelForm):
    sentence = forms.CharField(
        label='문장',
        widget=forms.TextInput(
            attrs={
                'placeholder': '게시글 문장'
            }
        ),
        required=True,
    )

    contents = SummernoteTextField()

    field_order = [
        'sentence',
    ]

    class Meta:
        model = SentenceList
        fields = [
            'sentence',
        ]
        widgets = {
            'contents' : SummernoteWidget()
        }
    
    def clean(self):
        cleaned_data = super().clean()

        sentence = cleaned_data.get('sentence', '')

        if sentence == '':
            self.add_error('title', '글 제목을 입력하세요.')
        else:
            self.sentence = sentence

