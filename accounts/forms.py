from django import forms
from .models import User
from argon2 import PasswordHasher, exceptions

class RegisterForm(forms.ModelForm):
    user_id = forms.Field(
        label="아이디",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class' : 'user-id',
                'placeholder' : '아이디'
            }
        ),
        error_messages={'required' : '아이디를 입력해주세요.'}
    )
    user_pw = forms.Field(
        label="비밀번호",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class' : 'user-pw',
                'placeholder' : '비밀번호'
            }
        ),
        error_messages={'required' : '비밀번호를 입력해주세요.'}
    )
    field_order = [
        'user_id',
        'user_pw',
    ]
    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        cleand_data = super().clean()

        user_id = cleaned_data.get('user_id','')
        user_pw = cleaned_data.get('user_pw','')

        self.user_id = user_id
        self.user_pw = PasswordHasher().hash(user.pw)
        self.user_pw_confirm = user_pw_confirm

class LoginForm(forms.Form):
    user_id = forms.CharField(
        max_length=32,
        label="아이디",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class' : 'user-id',
                'placeholder' : '아이디'
            }
        ),
        error_messages={'required' : '아이디를 입력해주세요.'}
    )

    user_pw = forms.CharField(
        max_length=128,
        label='비밀번호',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class' : 'user-pw',
                'placeholder' : '비밀번호'
            }
        ),
        error_messages={'required' : '비밀번호를 입력해주세요.'}
    )

    field_order = [
        'user_id',
        'user_pw',
    ]

    def clean(self):
        cleaned_data = super().clean()

        user_id = cleaned_data.get('user_id', '')
        user_pw = cleaned_data.get('user_pw', '')

        if user_id == '':
            return self.add_error('user_id', '아이디를 다시 입력해주세요.')
        elif user_pw == '':
            return self.add_error('user_pw', '비밀번호를 다시 입력해주세요.')
        else:
            try:
                user = User.object.get(user_id=user_id)
            except User.DoesNotExist:
                return self.add_error('user_id', '아이디가 존재하지 않습니다')

            try:
                PasswordHasher().verify(user.user_pw, user_pw)
            except exceptions.VerifyMismatchError:
                return self.add_error('user_pw', '비밀번호가 다릅니다.')
