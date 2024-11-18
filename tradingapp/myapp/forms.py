from django import forms

# If you have predefined choices, define them as a list of tuples
CHOICES = [
    ('option1', 'Option 1'),
    ('option2', 'Option 2'),
    ('option3', 'Option 3'),
]

class MyForm(forms.Form):
    dropdown = forms.ChoiceField(label="Select an option")

    def __init__(self, *args, **kwargs):
        # Extract the choices from the keyword arguments if they are passed in
        choices = kwargs.pop('choices', None)
        
        # Call the parent constructor
        super(MyForm, self).__init__(*args, **kwargs)
        
        # Set default choice
        default_choice = [('', 'Select an option...')]
        
        # Set choices if provided, otherwise keep dropdown empty
        if choices:
            self.fields['dropdown'].choices = default_choice + choices