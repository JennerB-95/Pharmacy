from django import forms

from core.user.models import User

class ResetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingresa tu usuario',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        if not User.objects.filter(username=cleaned['username']).exists():
            self.errors['error'] = self.errors.get('error', self.error_class())
            self.errors['error'].append('El usuario no existe!')
            # raise forms.ValidationError('El usuario no existe')
        return cleaned


    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingresa tu contraseña',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repite tu contraseña',
        'class': 'form-control',
        'autocomplete': 'off'
    }))


    def clean(self):
        cleaned = super().clean()
        password = cleaned['password']
        confirmPassword = cleaned['confirmPassword']

        if password != confirmPassword:
            self.errors['error'] = self.errors.get('error', self.error_class())
            self.errors['error'].append('Las contraseñas deben ser iguales!')
            # raise forms.ValidationError('El usuario no existe')
        return cleaned