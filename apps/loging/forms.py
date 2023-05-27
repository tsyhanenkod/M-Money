from django import forms


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'first name', 'autocomplete': 'off'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'last name', 'autocomplete': 'off'}))
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'email', 'autocomplete': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password', 'autocomplete': 'off'}))
    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password confirmation', 'autocomplete': 'off'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation:
            if password != password_confirmation:
                raise forms.ValidationError('Passwords do not match')

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'email', 'autocomplete': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password', 'autocomplete': 'off'}))
    remember = forms.BooleanField(required=False)


class ChangeUserData(forms.Form):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password_confirmation = forms.CharField(widget=forms.PasswordInput)

