from django import forms
from .models import CustomUser
from django.core.validators import RegexValidator
from .models import Profile
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    code = forms.CharField(validators=[RegexValidator(regex='^.{5}$', message='验证码长度为5', code='nomatch')])

class RegisterForm(forms.ModelForm):
    password = forms.CharField()
    password_confirm = forms.CharField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email','password')

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('密码输入不一致,请重试')
        return password_confirm

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'info','gender','bod')



