from django import forms

class Registrazione(forms.Form):
    email = forms.EmailField(label='Indirizzo e-mail')
    #email_confirmation = forms.EmailField(label='Conferma e-mail')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = 'cliente'
        fields = [
            'nome',
            'cognome'
            'email',
            'telefono',
            'password',
        ]