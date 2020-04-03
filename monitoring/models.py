from bitfield import BitField
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from accounts.models import Account
from prediction.models import HealthCenter
import validators
from . import choices


# Create your models here.

class Profile(models.Model):
    class Meta:
        ordering = ['-id']

    full_name = models.CharField(verbose_name='Nome completo', max_length=100, blank=True, default='')
    mother_name = models.CharField(verbose_name='Nome da mãe', max_length=100, blank=True, default='')
    birth_date = models.DateField(verbose_name='Data de nascimento', default='',
                                  validators=[validators.prevent_future_date])
    cns = models.CharField(verbose_name='Cartão do SUS', max_length=15, blank=True, default='000000000000000')
    id_document = models.CharField(verbose_name='RG', max_length=15, blank=True, default='000000000')
    cpf = models.CharField(verbose_name='CPF', max_length=11, blank=True, default='00000000000',
                           validators=[validators.validate_cpf], null=True)
    phone_number = models.CharField(verbose_name='Número de telefone', max_length=20, blank=True, default='')
    gender = models.CharField(verbose_name='Sexo biológico', max_length=1, choices=choices.genders, blank=True,
                              default='')
    age = models.PositiveIntegerField(verbose_name='Idade', default=0)
    weight = models.FloatField(verbose_name='Peso (Kg)', blank=True, default=0,
                               validators=[MinValueValidator(0)])
    height = models.FloatField(verbose_name='Altura (m)', blank=True, default=0, validators=[MinValueValidator(0)])

    smoker = models.BooleanField(verbose_name='Fumante', blank=True, default=False)
    vaccinated = models.BooleanField(verbose_name='Tomou vacina da gripe em 2020', blank=True, default=False)
    oxygen = models.BooleanField(verbose_name='Precisou de oxigênio recentemente', blank=True, default=False)

    comorbidities = BitField(verbose_name='Comorbidades', flags=choices.comorbidities, default=0)

    status = models.CharField(verbose_name='Status', max_length=1, choices=choices.status, default='N')

    def __str__(self):
        return self.full_name

class Address(models.Model):
    profile = models.ForeignKey(Profile, models.CASCADE, null = True, blank = True, default=None)
    primary = models.BooleanField(verbose_name='Principal', blank=True, default=False)
    type = models.CharField(verbose_name='Tipo', max_length=2, choices=choices.address_types, blank=True, default='')
    postal_code = models.CharField(verbose_name='CEP', max_length=8, blank=True, default='')
    neighbourhood = models.CharField(verbose_name='Bairro', max_length=100, blank=True, default='')
    street_name = models.CharField(verbose_name='Logradouro', max_length=100, blank=True, default='')
    number = models.PositiveIntegerField(verbose_name='Número', blank=True, null=True, default=0)
    complement = models.CharField(verbose_name='Complemento', max_length=100, blank=True, default='')
    city = models.CharField(verbose_name='Cidade', max_length=30, default='', choices=choices.cities)
    people = models.PositiveIntegerField(verbose_name='Quantidade de pessoas', blank=True, null=True, default=1)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.profile.address_set.count() == 0:
            self.primary = True

        return super(Address, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        if self.primary:
            for address in self.profile.address_set.exclude(id=self.id).order_by('type'):
                if address.type == 'HM':
                    address.primary = True
                    address.save()
                    break

        super(Address, self).delete(using, keep_parents)

    def __str__(self):
        return '%s, %s - %s, %s, %s' % (
        self.street_name, str(self.number or 'S/N'), self.neighbourhood, self.city, self.postal_code)


class Monitoring(models.Model):
    class Meta:
        ordering = ['-created']

    profile = models.ForeignKey(Profile, models.CASCADE)
    tested = models.BooleanField(verbose_name='Já foi testado', blank=True, default=False)
    date = models.DateField(verbose_name='Data', auto_now_add=True)
    suspect = models.BooleanField(verbose_name='Suspeito de COVID-19', default=False)
    virus_exposure = BitField(verbose_name='Exposição COVID-19', flags=choices.exposure, blank=True, default=0)
    result = models.CharField(verbose_name='Resultado do exame', max_length=2, choices=choices.results, default='SR')
    created = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.update_profile_status()
        super(Monitoring, self).save(force_insert, force_update, using, update_fields)

    def update_profile_status(self):
        if self.result == 'PO':
            self.profile.status = 'C'
        elif self.suspect:
            self.profile.status = 'S'

        self.profile.save()

    def get_absolute_url(self):
        return reverse('monitoring:monitoring-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s (%s)' % (self.profile, self.date.strftime('%d/%m/%Y'))


class Symptom(models.Model):
    monitoring = models.ForeignKey(Monitoring, models.CASCADE, default=1)
    symptom = models.CharField(verbose_name='Tipo de sintoma', max_length=2, choices=choices.symptoms, default='')
    intensity = models.CharField(verbose_name='Intensidade', max_length=1, choices=choices.intensities, blank=True,
                                 default='L')
    onset = models.DateField(verbose_name='Data do surgimento', blank=True, null=True,
                             validators=[validators.prevent_future_date])

    def __str__(self):
        return '%s %s desde %s' % (self.get_symptom_display(), self.get_intensity_display(),
                                   self.onset.strftime('%d/%m/%Y'))


class Trip(models.Model):
    profile = models.ForeignKey(Profile, models.CASCADE, default=1)
    departure_date = models.DateField(verbose_name='Ida', null=True, blank=True, default=None,
                                      validators=[validators.prevent_future_date])
    return_date = models.DateField(verbose_name='Volta', null=True, blank=True, default=None,
                                   validators=[validators.prevent_future_date])
    country = models.CharField(verbose_name='País', max_length=3, choices=choices.countries, default='')

    def __str__(self):
        return '%s - %s a %s' % (self.get_country_display(), self.departure_date.strftime('%d/%m/%Y'),
                                 self.return_date.strftime('%d/%m/%Y'))

class Request(models.Model):
    material = models.CharField(verbose_name='Material requisitado', default='', max_length=300)
    quantity = models.PositiveIntegerField(verbose_name='Quantidade necessária', default=0)
    name = models.CharField(verbose_name='Nome', default='', max_length=100)
    # profile = models.ForeignKey(Profile, models.CASCADE, default=1)
    cellphone = models.CharField(verbose_name='Telefone', default='', max_length=20, null=True, blank=True)
    email = models.CharField(verbose_name='E-mail', default='', max_length=50, null=True, blank=True)
    unidade = models.CharField(verbose_name='Unidade de Saúde', default='', max_length=50)


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Neighbourhood(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.city.__str__() + ', ' + self.name

class ActionLog(models.Model):
    action = models.CharField(max_length=1, choices=choices.action_choices)
    model = models.CharField(max_length=2, choices=choices.model_choices)
    user = models.ForeignKey(Account, models.SET_NULL, null=True)
    ip = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Action: ' + self.action + ', Model: ' + self.model + ', Account: ' + self.user.__str__()


class DeadProfile(models.Model):
    full_name = models.CharField(verbose_name='Nome completo', max_length=100, blank=True, default='')
    cns = models.CharField(verbose_name='Cartão do SUS', max_length=15, blank=True, default='000000000000000')
    id_document = models.CharField(verbose_name='RG', max_length=15, blank=True, default='000000000')
    cpf = models.CharField(verbose_name='CPF', max_length=11, blank=True, default='00000000000',
                           validators=[validators.validate_cpf], null=True)
    age = models.PositiveIntegerField(verbose_name='Idade', default=0)
    death_date = models.DateField(verbose_name='Data do óbito', default='',
                                  validators=[validators.prevent_future_date])
    hospital = models.ForeignKey(HealthCenter, on_delete=models.CASCADE, verbose_name="Local do óbito(Hospital)")

class Familiar(models.Model):

    dead_profile = models.ForeignKey(DeadProfile, on_delete=models.CASCADE)
    full_name = models.CharField(verbose_name='Nome completo', max_length=100, blank=True, default='')

    cns = models.CharField(verbose_name='Cartão do SUS', max_length=15, blank=True, default='000000000000000')
    id_document = models.CharField(verbose_name='RG', max_length=15, blank=True, default='000000000')
    cpf = models.CharField(verbose_name='CPF', max_length=11, blank=True, default='00000000000',
                           validators=[validators.validate_cpf], null=True)

    phone_number = models.CharField(verbose_name='Número de telefone', max_length=20, blank=True, default='')

    age = models.PositiveIntegerField(verbose_name='Idade', default=0)

    comorbidities = BitField(verbose_name='Comorbidades', flags=choices.comorbidities, default=0)

    def __str__(self):
        return self.full_name

class DeadAddress(Address, models.Model):
    dead_profile = models.ForeignKey(DeadProfile, on_delete=models.CASCADE)
    def __init__(self,dead_profile, *args, **kwargs):
        self.dead_profile = dead_profile
        super(DeadAddress, self).__init__(args, kwargs)

class FamiliarAddress(Address, models.Model):
    familiar = models.ForeignKey(Familiar, on_delete=models.CASCADE)
    def __init__(self, familiar, *args, **kwargs):
        self.familiar = familiar
        super(FamiliarAddress, self).__init__(args, kwargs)
