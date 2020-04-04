from django.test import TestCase
from django.utils import timezone

from . import forms
from prediction.forms import HealthCenterForm

# Create your tests here.


class AccountTests(TestCase):

    def test_blacklisted_cpf(self):

        hc_form = HealthCenterForm(data={
            'center_name': 'SUS - Maceió',
            'latitude' : -9.66625,
            'longitude': -35.7351
        })

        hc = hc_form.save()

        data = {
            'cpf': '11111111111',
            'user_profile': 'SS',
            'health_center': hc,
            'password': 'qwcsczsc1',
            'confirm_password': 'qwcsczsc1'
        }

        form = forms.AccountCreationForm(data=data)
        self.assertTrue(form.has_error('cpf'))

    def test_valid_cpf(self):

        hc_form = HealthCenterForm(data={
            'center_name': 'SUS - Maceió',
            'latitude': -9.66625,
            'longitude': -35.7351
        })

        hc = hc_form.save()

        data = {
            'cpf': '09716630417',
            'user_profile': 'SS',
            'health_center': hc,
            'password': 'qwcsczsc1',
            'confirm_password': 'qwcsczsc1'
        }

        form = forms.AccountCreationForm(data=data)
        self.assertTrue(not form.has_error('cpf'))

    def test_invalid_cpf(self):

        hc_form = HealthCenterForm(data={
            'center_name': 'SUS - Maceió',
            'latitude': -9.66625,
            'longitude': -35.7351
        })

        hc = hc_form.save()

        data = {
            'cpf': '12345678910',
            'user_profile': 'SS',
            'health_center': hc,
            'password': 'qwcsczsc1',
            'confirm_password': 'qwcsczsc1'
        }

        form = forms.AccountCreationForm(data=data)
        self.assertTrue(form.has_error('cpf'))

    def test_passwords_doesnt_match(self):

        hc_form = HealthCenterForm(data={
            'center_name': 'SUS - Maceió',
            'latitude': -9.66625,
            'longitude': -35.7351
        })

        hc = hc_form.save()

        data = {
            'cpf': '09716630417',
            'user_profile': 'SS',
            'health_center': hc,
            'password': 'qwcsczsc1',
            'confirm_password': 'qwcsczsc'
        }

        form = forms.AccountCreationForm(data=data)
        self.assertTrue(form.has_error('confirm_password'))

    def test_passwords_match(self):

        hc_form = HealthCenterForm(data={
            'center_name': 'SUS - Maceió',
            'latitude': -9.66625,
            'longitude': -35.7351
        })

        hc = hc_form.save()

        data = {
            'cpf': '09716630417',
            'user_profile': 'SS',
            'health_center': hc,
            'password': 'qwcsczsc1',
            'confirm_password': 'qwcsczsc1'
        }

        form = forms.AccountCreationForm(data=data)
        self.assertTrue(not form.has_error('password') and not form.has_error('confirm_password'))


    def test_weak_password(self):
        hc_form = HealthCenterForm(data={
            'center_name': 'SUS - Maceió',
            'latitude': -9.66625,
            'longitude': -35.7351
        })

        hc = hc_form.save()

        data = {
            'cpf': '09716630417',
            'user_profile': 'SS',
            'health_center': hc,
            'password': '12345678',
            'confirm_password': '12345678'
        }

        form = forms.AccountCreationForm(data=data)
        self.assertFalse(not form.has_error('password') and not form.has_error('confirm_password'))
