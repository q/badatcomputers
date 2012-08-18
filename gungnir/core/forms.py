from emailusernames.forms import EmailUserCreationForm

class CompatEmailUserCreationForm(EmailUserCreationForm):
    def clean(self):
        cleaned_data = super(CompatEmailUserCreationForm, self).clean()
        if cleaned_data.has_key('email'):
            cleaned_data['username'] = cleaned_data['email']
        return cleaned_data