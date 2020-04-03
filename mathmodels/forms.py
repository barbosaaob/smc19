from django import forms
from . import choices


class ProportionsForm(forms.Form):
    from0to9 = forms.FloatField(
        label='De 0 a 9',
        help_text='Proporção de 0-9 anos',
        initial='0.20',
        widget=forms.NumberInput(attrs={'step': '0.0000001', 'min': '0', 'max':'1'}),
        required=True
        )

    from10to19 = forms.FloatField(
        label='De 10 a 19',
        help_text='Proporção de 10-19 anos',
        initial='0.20',
        widget=forms.NumberInput(attrs={'step': '0.0000001', 'min': '0', 'max':'1'}),
        required=True
        )

    from20to29 = forms.FloatField(
        label='De 20 a 29',
        help_text='Proporção de 20-29 anos',
        initial='0.20',
        widget=forms.NumberInput(attrs={'step': '0.0000001', 'min': '0', 'max':'1'}),
        required=True
        )

    from30to39 = forms.FloatField(
        label='De 30 a 39',
        help_text='Proporção de 30-39 anos',
        initial='0.20',
        widget=forms.NumberInput(attrs={'step': '0.0000001', 'min': '0', 'max':'1'}),
        required=True
        )

    from40to49 = forms.FloatField(
        label='De 40 a 49',
        help_text='Proporção de 40-49 anos',
        initial='0.04',
        widget=forms.NumberInput(attrs={'step': '0.0000001', 'min': '0', 'max':'1'}),
        required=True
        )

    from50to59 = forms.FloatField(
        label='De 50 a 59',
        help_text='Proporção de 50-59 anos',
        initial='0.04',
        widget=forms.NumberInput(attrs={'step': '0.0000001', 'min': '0', 'max':'1'}),
        required=True
        )

    from60to69 = forms.FloatField(
        label='De 60 a 69',
        help_text='Proporção de 60-69 anos',
        initial='0.04',
        widget=forms.NumberInput(attrs={'step': '0.0000001', 'min': '0', 'max':'1'}),
        required=True
        )

    from70to79 = forms.FloatField(
        label='De 70 a 79',
        help_text='Proporção de 70-79 anos',
        initial='0.04',
        widget=forms.NumberInput(attrs={'step': '0.0000001', 'min': '0', 'max':'1'}),
        required=True
        )

    from80to80plus = forms.FloatField(
        label='De 80 a 80+',
        help_text='Proporção de 80-80+ anos',
        initial='0.04',
        widget=forms.NumberInput(attrs={'step': '0.0000001', 'min': '0', 'max':'1'}),
        required=True
        )

class SirSeirForm(forms.Form):
    N = forms.IntegerField(
        help_text='População total',
        initial=1000000,
        widget=forms.NumberInput(attrs={'step': '1000', 'min': '0'}),
        required=True
        )

    S0 = forms.FloatField(
        label='S0',
        help_text='Porcentagem inicial de suscetíveis',
        initial='0.99995',
        widget=forms.NumberInput(attrs={'step': '0.0000001', 'min': '0', 'max':'1'}),
        required=True
        )
    
    E0 = forms.FloatField(
        label='E0',
        help_text='Porcentagem inicial de expostos',
        initial='0.0',
        widget=forms.NumberInput(attrs={'step': '0.0000001', 'min': '0', 'max':'1'}),
        required=True
        )

    I0 = forms.FloatField(
        label='I0',
        help_text='Porcentagem inicial de infectados',
        initial='0.00005',
        widget=forms.NumberInput(attrs={'step': '0.0000001', 'min': '0', 'max':'1'}),
        required=True
        )

    R0 = forms.FloatField(
        label='R0',
        help_text='Porcentagem inicial de recuperados',
        initial='0.0',
        widget=forms.NumberInput(attrs={'step': '0.0000001', 'min': '0', 'max':'1'}),
        required=True
        )

    alpha = forms.FloatField(
        label='alpha',
        help_text='Parâmetro alpha (SEIR)',
        initial='0.2',
        widget=forms.NumberInput(attrs={'step': '0.01'}),
        required=True
        )

    beta = forms.FloatField(
        label='beta',
        help_text='Parâmetro beta',
        initial='1.75',
        widget=forms.NumberInput(attrs={'step': '0.01'}),
        required=True
        )

    gamma = forms.FloatField(
        label='gamma',
        help_text='Parâmetro gamma',
        initial='0.5',
        widget=forms.NumberInput(attrs={'step': '0.01'}),
        required=True
        )

    rho = forms.FloatField(
        label='rho (ou rho iso, dist. adapt.)',
        help_text='Parâmetro rho (dist. social)',
        initial='1.0',
        widget=forms.NumberInput(attrs={'step': '0.01', 'min': '0.0', 'max':'1.0'}),
        required=True
        )

    rho_relax = forms.FloatField(
        label='rho relax',
        help_text='Parâmetro rho relax (dist. social adapt.)',
        initial='1.0',
        widget=forms.NumberInput(attrs={'step': '0.01', 'min': '0.0', 'max':'1.0'}),
        required=True
        )

    days = forms.IntegerField(
        label='Changes',
        help_text='Changing quarentine status',
        initial='65',
        widget=forms.NumberInput(attrs={'step': '1', 'min': '0'}),
        required=True
        )

    changes = forms.IntegerField(
        label='Dias',
        help_text='Dias da simulação',
        initial='120',
        widget=forms.NumberInput(attrs={'step': '1', 'min': '0'}),
        required=True
        )

    model = forms.ChoiceField(
        label='Modelo',
        choices=choices.model_type
        )
