from importlib.resources import contents
from django import forms
from .models import Board
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget


class BoardWriteForm(forms.ModelForm):
    title = forms.CharField(
        label='글 제목',
        widget=forms.TextInput(
            attrs={
                'placeholder': '게시글 제목'
            }
        ),
        required=True,
    )

    contents = SummernoteTextField()

    field_order = [
        'title',
        'writer',
        'sentence',
        'contents'
    ]

    class Meta:
        model = Board
        fields = [
            'title',
            'contents',
            'sentence',
            'writer',
        ]
        widgets = {
            'contents' : SummernoteWidget()
        }
    
    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title', '')
        contents = cleaned_data.get('contents', '')
        writer = cleaned_data.get('writer', '')
        sentence = cleaned_data.get('sentence', '')

        if title == '':
            self.add_error('title', '글 제목을 입력하세요.')
        elif contents == '':
            self.add_error('contents', '글 내용을 입력하세요.')
        else:
            self.title = title
            self.contents = contents
            self.writer = writer
            self.sentence = sentence

