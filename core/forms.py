from django import forms

class MailForm(forms.Form):
    email = forms.EmailField(label=u'E-mail')

    def save_mail(self):
        mail = self.cleaned_data['email']
        return mail