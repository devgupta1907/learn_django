from django import forms
from django.core.validators import MaxValueValidator, EmailValidator, MinLengthValidator
from django.contrib.auth.forms import BaseUserCreationForm, ReadOnlyPasswordHashField
from .models import FoundationalModel, Student, StudentExtended, Teacher
from django.core.exceptions import ObjectDoesNotExist, ValidationError




# Here initial is the default value of the standard field.
class StudentRegistration(BaseUserCreationForm):
    standard = forms.IntegerField(validators=[
                                                MaxValueValidator(
                                                limit_value=12, 
                                                message=("How you could study in this class?"))])
    
    class Meta:
        model = Student
        fields = ('name', 'email', 'standard', 'password1', 'password2')
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if Student.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return email

    # this is how we add custom validator/validator message on the field that is present
    # in the "fields" attribute of Meta class.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].validators = [EmailValidator(message="Gentleman! This email is not good.")]
        self.fields['name'].validators.append(MinLengthValidator(limit_value=4, message="Not enough alphas!"))
        
        
    # The preference of validators is always given to client-side validation, i.e
    # the validators that are defined in forms (not in models).


class TeacherRegistration(BaseUserCreationForm):
    subject = forms.CharField(max_length=15)
    class Meta:
        model = Teacher
        fields = ('name', 'email', 'subject', 'password1', 'password2')



class StudentLogin(forms.Form):
    email = forms.CharField(label="Email", max_length=255, help_text="Put your registered email address here")
    password = forms.CharField(label = "Password", widget=forms.PasswordInput)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            # Check if the email exists in the database
            student = Student.objects.get(email=email)
        except ObjectDoesNotExist:
            # If the email does not exist, raise a ValidationError
            raise forms.ValidationError("The email you entered is not registered.")
        return email
    
class TeacherLogin(forms.Form):
    email = forms.CharField(label="Email", max_length=255)
    password = forms.CharField(label = "Password", widget=forms.PasswordInput)
    
    
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email']
    
    