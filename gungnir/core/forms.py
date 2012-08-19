from emailusernames.forms import EmailUserCreationForm, EmailAuthenticationForm
from django.forms import ModelForm
from django import forms
from gungnir.core.models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user','can_build',)
    
    aws_akey = forms.CharField(label="Access Key")
    aws_skey = forms.CharField(label="Secret Key")
    
# workaround to get username-as-emails to work with django-registration
class CompatEmailUserCreationForm(EmailUserCreationForm):
    def clean(self):
        cleaned_data = super(CompatEmailUserCreationForm, self).clean()
        if cleaned_data.has_key('email'):
            cleaned_data['username'] = cleaned_data['email']
        return cleaned_data


from gungnir.core.decorators import order_fields
@order_fields('email','password')
class CoreEmailAuthForm(EmailAuthenticationForm):
    pass
