from django import forms

from book.models import Terrarium, Specimen, Repas, Mue, Mesure, Emplacement, Maintenance, Achat


class TerrariumForm(forms.ModelForm):
    class Meta:
        model = Terrarium
        fields = '__all__'


class SpecimenForm(forms.ModelForm):
    class Meta:
        model = Specimen
        fields = '__all__'


class RepasForm(forms.ModelForm):
    class Meta:
        model = Repas
        fields = ('specimen', 'date', 'type', 'origine', 'quantite', 'remarque', )


class MueForm(forms.ModelForm):
    class Meta:
        model = Mue
        fields = '__all__'


class MesureForm(forms.ModelForm):
    class Meta:
        model = Mesure
        fields = '__all__'


class EmplacementForm(forms.ModelForm):
    class Meta:
        model = Emplacement
        fields = '__all__'


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = '__all__'


class AchatForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = '__all__'


class UploadFileForm(forms.Form):
    file = forms.FileField()
