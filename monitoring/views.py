from django.contrib import messages
from django.contrib.auth import mixins
from django.db import connection
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.http import JsonResponse

from monitoring import choices
from . import forms
from . import models
from . import utils

from prediction.models import HealthCenter, HealthCenterStatus


# Create your views here.

class Index(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Profile
    paginate_by = 10
    template_name = 'monitoring/index.html'

    def get_queryset(self):
        params = dict(zip(self.request.GET.keys(), self.request.GET.values()))

        if params.get('search-target') == 'profile':
            search_term = self.request.GET.get('term')
            return models.Profile.objects.filter(Q(full_name__icontains=search_term) |
                                                 Q(id_document__startswith=search_term) |
                                                 Q(cpf__startswith=search_term) |
                                                 Q(cns__startswith=search_term))

        return super(Index, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)

        context['params'] = self.request.GET
        context['monitorings'] = models.Monitoring.objects.all().order_by('-created')[:20]
        context['monitoring_create_form'] = forms.MonitoringForm()
        symptoms_initial = [{'symptom': symptom[0], 'label': symptom[1]} for symptom in choices.symptoms]
        context['symptom_formset'] = forms.SymptomInlineFormset(initial=symptoms_initial)

        return context


class Map(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'monitoring/map.html'

    def get_context_data(self, **kwargs):
        context = super(Map, self).get_context_data(**kwargs)

        params = {key: value for key, value in self.request.GET.items() if value != '' and value != 0}
        context['params'] = params

        sql_query = '''
        SELECT 
            monitoring_address.city,
            SUM(last_monitorings.suspect) AS suspect_cases, 
            SUM(CASE  WHEN last_monitorings.result = 'PO' THEN 1 ELSE 0 END) AS confirmed_cases,
            SUM(CASE  WHEN last_monitorings.result = 'M' THEN 1 ELSE 0 END) AS deaths,
            AVG(monitoring_address.people) as people_average,
            SUM(monitoring_profile.smoker) AS smokers
        FROM 
            monitoring_profile 
            JOIN 
                (
                SELECT 
                    monitoring_monitoring.*,
                    MAX(monitoring_monitoring.created) AS latest_date 
                FROM
                    monitoring_monitoring 
                GROUP BY
                    monitoring_monitoring.profile_id
                ) last_monitorings
            ON 
                monitoring_profile.id = last_monitorings.profile_id
            JOIN 
                monitoring_address
            ON
                monitoring_profile.id = monitoring_address.profile_id 
        WHERE 
            monitoring_address."primary" = 1
        
        '''

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            total = cursor.fetchone()

        with connection.cursor() as cursor:
            cursor.execute(sql_query + ' GROUP BY monitoring_address.city')
            stats = cursor.fetchall()

        print(stats)

        context['territory_stats'] = {
            'total': {
                'suspect_cases': total[1],
                'confirmed_cases': total[2],
                'deaths': total[3],
                'people_average': total[4],
                'smokers': total[5],
            },
            'cities': {
                stat[0]: {
                    'suspect_cases': stat[1],
                    'confirmed_cases': stat[2],
                    'deaths': stat[3],
                    'people_average': stat[4],
                    'smokers': stat[5],
                }
                for stat in stats
            }

        }

        '''
        O P E R A Ç Ã O   L A V A   C Ó D I G O
        As consultas abaixo estão extremamente ineficientes(cada HealthCenterStatus.objects.filter(...) faz uma consulta 
        (e ordena) ao banco para no final só pegar um campo de cada vez) além de estar ilegível
        '''
        context['health_center_stats'] = [{
            "healthCenterName": u.center_name,
            "latitude": u.latitude,
            "longitude": u.longitude,
            "healthCenterStatus": {
                "beds": HealthCenterStatus.objects.filter(health_center=u).order_by('-date')[0].beds if len(HealthCenterStatus.objects.filter(health_center=u)) > 0 else 0,
                "intensiveCareUnits": HealthCenterStatus.objects.filter(health_center=u).order_by('-date')[0].icus if len(HealthCenterStatus.objects.filter(health_center=u)) > 0 else 0,
                "respirators": HealthCenterStatus.objects.filter(health_center=u).order_by('-date')[0].respirators if len(HealthCenterStatus.objects.filter(health_center=u)) > 0 else 0,
                "occupiedBeds": HealthCenterStatus.objects.filter(health_center=u).order_by('-date')[0].occupied_beds if len(HealthCenterStatus.objects.filter(health_center=u)) > 0 else 0,
                "occupiedIntensiveCareUnits": HealthCenterStatus.objects.filter(health_center=u).order_by('-date')[0].occupied_icus if len(HealthCenterStatus.objects.filter(health_center=u)) > 0 else 0,
                "occupiedRespirators": HealthCenterStatus.objects.filter(health_center=u).order_by('-date')[0].occupied_respirators if len(HealthCenterStatus.objects.filter(health_center=u)) > 0 else 0,
                "date": str(HealthCenterStatus.objects.filter(health_center=u).order_by('-date')[0].date) if len(HealthCenterStatus.objects.filter(health_center=u)) > 0 else '2020-01-01'
            }
        } for u in HealthCenter.objects.all()]

        return context


class Dashboard(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'monitoring/dashboard.html'

    def get_context_data(self):
        context = super(Dashboard, self).get_context_data()

        sql_query = '''
        SELECT  
            SUM(last_monitorings.suspect) AS suspect_cases, 
            SUM(monitoring_profile.smoker) AS smokers,
            SUM(CASE  WHEN last_monitorings.result = 'PO' THEN 1 ELSE 0 END) AS confirmed_cases,
            SUM(CASE  WHEN last_monitorings.result = 'M' THEN 1 ELSE 0 END) AS deaths,
            AVG(monitoring_address.people) as people_average
        FROM 
            monitoring_profile 
            JOIN 
                (
                SELECT 
                    monitoring_monitoring.*,
                    MAX(monitoring_monitoring.created) AS latest_date 
                FROM
                    monitoring_monitoring 
                GROUP BY
                    monitoring_monitoring.profile_id
                ) last_monitorings
            ON 
                monitoring_profile.id = last_monitorings.profile_id
            JOIN 
                monitoring_address
            ON
                monitoring_profile.id = monitoring_address.profile_id 
        WHERE 
            monitoring_address."primary" = 1
        GROUP BY 
            monitoring_address.city
        '''

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            stats = cursor.fetchone()
        print(stats)
        context['stats'] = {
            'total': {
                'suspect_cases': stats[0],
                'confirmed_cases': stats[1],
                'deaths': stats[2],
                'people_average': stats[3],
                'smokers': stats[4],
            }
        }

        return context


#Profile
class ProfileSearch(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Profile
    def get(self, request, *args, **kwargs):
        search_term = self.kwargs['term']
        profiles = list(models.Profile.objects.filter(Q(full_name__icontains=search_term) |
                                                    Q(id_document__startswith=search_term) |
                                                    Q(cpf__startswith=search_term) |
                                                    Q(cns__startswith=search_term)).values())
        return JsonResponse(profiles, safe=False)

class ProfileCreate(mixins.LoginRequiredMixin, generic.CreateView):
    form_class = forms.ProfileForm
    template_name = 'monitoring/new_profile.html'
    success_url = reverse_lazy('monitoring:index')

    def get_context_data(self, **kwargs):
        context = super(ProfileCreate, self).get_context_data(**kwargs)

        if self.request.POST:
            context['primary_address_form'] = forms.AddressInlineFormset(self.request.POST)
        else:
            context['primary_address_form'] = forms.AddressInlineFormset()

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        self.object = form.save(commit=True)
        address_form = context['primary_address_form']
        address = address_form.save(commit=False)[0]
        address.profile = self.object

        if address_form.is_valid():
            address.primary = True

            utils.create_log(self.request, 'C', 'AD')
            address.save()
        else:
            print(address_form.errors)
            return self.form_invalid(form)

        utils.create_log(self.request, 'C', 'PR')
        return super(ProfileCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super(ProfileCreate, self).form_invalid(form)


class ProfileDetail(mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Profile
    template_name = 'monitoring/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)

        context['update_profile_form'] = forms.ProfileForm(instance=self.object)
        context['address_form'] = forms.AddressForm(data={
            'profile': self.object.id
        })
        context['trip_form'] = forms.TripForm(data={
            'profile': self.object.id
        })

        comorbidities = []
        for comorbidity in self.object.comorbidities:
            comorbidities.append({
                'label': self.object.comorbidities.get_label(comorbidity[0]),
                'set': comorbidity[1]
            })

        context['comorbidities'] = comorbidities

        return context


class ProfileUpdate(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Profile
    form_class = forms.ProfileForm

    def form_valid(self, form):
        utils.create_log(self.request, 'U', 'PR')
        return super(ProfileUpdate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['pk']])


class ProfileDelete(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Profile
    success_url = reverse_lazy('monitoring:index')

    def post(self, request, *args, **kwargs):
        utils.create_log(request, 'D', 'PR')
        return super(ProfileDelete, self).post(request, *args, **kwargs)


# Address

class AddressCreate(mixins.LoginRequiredMixin, generic.CreateView):
    form_class = forms.AddressForm

    def form_valid(self, form):
        utils.create_log(self.request, 'C', 'AD')
        return super(AddressCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['profile']])


class AddressUpdate(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Address
    form_class = forms.AddressForm

    def form_valid(self, form):
        utils.create_log(self.request, 'U', 'AD')
        return super(AddressUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['profile']])


class AddressDelete(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Address

    def post(self, request, *args, **kwargs):
        utils.create_log(request, 'D', 'AD')
        return super(AddressDelete, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['profile']])


# Monitoring

class MonitoringDetail(mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Monitoring

    def get_context_data(self, **kwargs):
        context = super(MonitoringDetail, self).get_context_data(**kwargs)

        # Formulário de edição do atendimento atual
        context['monitoring_update_form'] = forms.MonitoringForm(instance=self.object)

        symptoms_initial = []
        for symptom in choices.symptoms:
            s = models.Symptom.objects.filter(symptom=symptom[0])
            if len(s) > 0:
                symptoms_initial.append({
                    'symptom': symptom[0],
                    'label': symptom[1],
                    'onset': s[0].onset
                })
            else:
                symptoms_initial.append({
                    'symptom': symptom[0],
                    'label': symptom[1]
                })

        else:
            context['symptom_formset'] = forms.SymptomInlineFormset(initial=symptoms_initial)

        exposures = []
        for exposure in self.object.virus_exposure:
            exposures.append({
                'label': self.object.virus_exposure.get_label(exposure[0]),
                'set': exposure[1]
            })

        context['exposures'] = exposures

        return context


class MonitoringCreate(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Monitoring
    form_class = forms.MonitoringForm

    def get_context_data(self, **kwargs):
        context = super(MonitoringCreate, self).get_context_data(**kwargs)

        symptoms_initial = [{'symptom': symptom[0], 'label': symptom[1]} for symptom in choices.symptoms]

        if self.request.POST:
            context['symptom_formset'] = forms.SymptomInlineFormset(self.request.POST, initial=symptoms_initial)
        else:
            context['symptom_formset'] = forms.SymptomInlineFormset(initial=symptoms_initial)

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        symptom_formset = context['symptom_formset']

        if symptom_formset.is_valid():
            self.object = form.save(commit=True)

            for formset in symptom_formset:
                instance = formset.save(commit=False)
                if instance.onset != None:
                    instance.monitoring = self.object
                    instance.save()

            messages.success(self.request, 'Atendimento cadastrado com sucesso!')

            utils.create_log(self.request, 'C', 'MO')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super(MonitoringCreate, self).form_invalid(form)

    def get_success_url(self):
        return reverse('monitoring:index')


class MonitoringUpdate(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Monitoring
    form_class = forms.MonitoringForm

    def get_context_data(self, **kwargs):
        context = super(MonitoringUpdate, self).get_context_data(**kwargs)

        if self.request.POST:
            symptoms_initial = [{'symptom': symptom[0], 'label': symptom[1]} for symptom in choices.symptoms]
            context['symptom_formset'] = forms.SymptomInlineFormset(self.request.POST, initial=symptoms_initial)

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        symptom_formset = context['symptom_formset']

        if symptom_formset.is_valid():
            self.object = form.save(commit=True)

            for formset in symptom_formset:
                instance = formset.save(commit=False)
                symptoms = self.object.symptom_set.filter(symptom=instance.symptom)
                if len(symptoms) == 1:
                    if instance.onset is not None:
                        symptoms[0].onset = instance.onset
                        symptoms[0].save()
                    else:
                        symptoms[0].delete()
                else:
                    if instance.onset is not None:
                        instance.monitoring = self.object
                        instance.save()

            messages.success(self.request, 'Atendimento atualizado com sucesso!')

            utils.create_log(self.request, 'U', 'MO')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('monitoring:monitoring-detail', args=[self.kwargs['pk']])


class MonitoringDelete(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Monitoring

    def post(self, request, *args, **kwargs):
        utils.create_log(request, 'D', 'MO')
        return super(MonitoringDelete, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('monitoring:index')


# Trip

class TripCreate(mixins.LoginRequiredMixin, generic.CreateView):
    form_class = forms.TripForm

    def form_valid(self, form):
        utils.create_log(self.request, 'C', 'TR')
        return super(TripCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['profile']])


class TripUpdate(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Trip
    form_class = forms.TripForm

    def form_valid(self, form):
        utils.create_log(self.request, 'U', 'TR')
        return super(TripUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('monitoring:index')


class TripDelete(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Trip

    def post(self, request, *args, **kwargs):
        utils.create_log(request, 'D', 'TR')
        return super(TripDelete, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['profile']])


class RequestCreate(mixins.LoginRequiredMixin, generic.CreateView):
    form_class = forms.RequestForm
    template_name = 'monitoring/new_request.html'
    success_url = reverse_lazy('monitoring:request')

    def form_valid(self, form):
        utils.create_log(self.request, 'C', 'RE')
        return super(RequestCreate, self).form_valid(form)


class RequestIndex(mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'monitoring/request_index.html'
    context_object_name = 'all_requests'

    def get_queryset(self):
        return models.Request.objects.all()


class RequestDelete(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Request
    success_url = reverse_lazy('monitoring:request')

    def post(self, request, *args, **kwargs):
        utils.create_log(request, 'D', 'RE')
        return super(RequestDelete, self).post(request, *args, **kwargs)
