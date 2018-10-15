import json
import os
import tempfile
# import textract

from django import forms
from django.contrib.auth.forms import UserCreationForm

from app import models
from TTS.settings import (MEDIA_ROOT)

# class FromControl(forms.From):
#     def __init__(self, arg):
#         super(FromControl, self).__init__()
#         self.fields


class Login(forms.Form):
    
    email = forms.EmailField(required=True, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")

    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class' : 'form-control'})
            self.fields[i].widget.attrs.update({'placeholder' : self.fields[i].label})

    def clean_email(self):
        return self.cleaned_data['email'].lower()


class SignUp(UserCreationForm):

    class Meta():
        model = models.User
        fields = ("email", "username")
    
    def __init__(self, *args, **kwargs):
        super(SignUp, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class' : 'form-control'})

    def clean_email(self):
        return self.cleaned_data['email'].lower()

class NewAudio(forms.Form):
    type_choices = (('', "Seleccionar"), ('word', 'Archivo Word'), 
                    ('txt', 'Archivo txt'), ('existant', 'Audio existente'),
                    ('new', 'Nuevo texto'))
    type = forms.ChoiceField(choices=type_choices)

    audio = forms.ModelChoiceField(queryset=None, label="Audio Existente", required=False)
    file = forms.FileField(label="Archivo", required=False)
    
    def clean_type(self):
        if self.cleaned_data['type'] == '':
            raise forms.ValidationError('Seleccione una opción.')
        return self.cleaned_data['type']

    def clean_audio(self):
        if self.cleaned_data['type'] == 'existant' and self.cleaned_data['audio'] is None:
            raise forms.ValidationError('Seleccione una audio existente.')
        return self.cleaned_data['audio']            

    def clean_file(self):
        type = self.cleaned_data['type']
        if type == 'new':
            return None
        
        if type == 'existant' and self.cleaned_data['audio'] is not None:
            return None

        file = self.cleaned_data['file']
        fileTypes = {
            'word': ['.doc', '.docx'],
            'txt': ['.txt']
        }    
        
        if not type in ['new',''] and not file:
            raise forms.ValidationError('Debe subir un archivo %s.'% type)
        
        filename, file_extension = os.path.splitext(file.name)
        print(file_extension, fileTypes[type])
        
        if not file_extension in fileTypes[type]:
            raise forms.ValidationError("El archivo debe tener extension %s"%', '.join(fileTypes[type]))
        
        memfile = self.cleaned_data['file']
        temp_file_name = os.path.join(MEDIA_ROOT, tempfile.mktemp()) + file_extension
        print(temp_file_name)
        with open(temp_file_name, "wb") as file:
          file.write(memfile.read())
        try:
            pass
          # text = textract.process(temp_file_name).decode('utf-8')
        except Exception as e:
          raise forms.ValidationError("El archivo es invalido.")
        os.remove(temp_file_name)
        return text

    def __init__(self, *args, **kwargs):
        super(NewAudio, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class' : 'form-control'})


class CreateAudio(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)
    description = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(CreateAudio, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({
                'placeholder': 'Introduzca un texto.',
                'style':'width:100%',
                'class': 'context-menu-one',
                })
        self.fields['description'].widget.attrs.update({'placeholder': "Opcional", "rows":"5"})
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class' : 'form-control'})

    class Meta:
        model = models.Audio
        fields = ("name", "description", "text", 'format')
        widgets = {
            'format': forms.RadioSelect(),
        }