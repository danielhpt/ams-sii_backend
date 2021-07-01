from django import forms


class OccurrenceNumberForm(forms.Form):
    occurrence_number = forms.IntegerField(label='Numero da Ocorrência')
