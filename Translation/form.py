from django import forms
from .models import Key
from .models import Translation
import re
import detectlanguage

detectlanguage.configuration.api_key = "ee97da1f2c23d8274796a0b99fd620c8"

class KeyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(KeyForm, self).__init__(*args, **kwargs)
        self.message = 'Invalid data'
    def clean_name(self):
        name = self.cleaned_data['name']

        # check that Key Object with {name} exist
        key_object = Key.objects.filter(name = name)
        if key_object.exists():
            self.message = 'Integrity constraint - [ "name" : ' + name + ' ] is already exist'
            raise forms.ValidationError(self.message)

        # Check {name} consists of only lowercase letters and dots.
        Pattern = re.compile("^([a-z]*[.]*)+$")
        result = Pattern.match(name)
        if result == None:
            self.message = 'Invalid name - [ "name" : ' + name + ' ] is not valid'
            raise forms.ValidationError(self.message)
        return name

    class Meta:
        model = Key
        fields = ('id', 'name')

class TranslationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TranslationForm, self).__init__(*args, **kwargs)
        self.message = 'Invalid data'
    def clean(self):
        cleaned_data = super(TranslationForm, self).clean()
        try:
            locale = self.cleaned_data['locale']
            value = self.cleaned_data['value']
        except:
            self.message = 'Invalid input value'
            raise forms.ValidationError(self.message)

        LocaleOfValue = detectlanguage.simple_detect(value)

        # check {value}'s language is equal to {locale}
        if LocaleOfValue != locale:
            self.message = 'Language Does Not Match - [ "value" : ' + value  + ' ]\'s  language is not equal to "' + locale + '"'
            raise forms.ValidationError(self.message)
        return cleaned_data

    class Meta:
        model = Translation
        fields = ('id', 'key_id', 'locale', 'value')
