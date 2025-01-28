from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class MyForm(forms.Form):
    dropdown = forms.ChoiceField(label="Select an option")

    def __init__(self, *args, **kwargs):
        # Extract the choices from the keyword arguments if they are passed in
        choices = kwargs.pop("choices", None)

        # Call the parent constructor
        super(MyForm, self).__init__(*args, **kwargs)

        # Set default choice
        default_choice = [("", "Select an option...")]

        # Set choices if provided, otherwise keep dropdown empty
        if choices:
            self.fields["dropdown"].choices = default_choice + choices


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
