from emailusernames.forms import EmailUserCreationForm
from django.forms import ModelForm
from gungnir.core.models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user','can_build',)

# workaround to get username-as-emails to work with django-registration
class CompatEmailUserCreationForm(EmailUserCreationForm):
    def clean(self):
        cleaned_data = super(CompatEmailUserCreationForm, self).clean()
        if cleaned_data.has_key('email'):
            cleaned_data['username'] = cleaned_data['email']
        return cleaned_data

