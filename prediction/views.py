from django.contrib import messages
from django.contrib.auth import mixins
from django.db.models import Count, Q, Avg
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django import forms


from monitoring import choices
from . import models

from django.shortcuts import render

from monitoring import utils

from django.views.generic import DetailView

from datetime import date


class HealthCenterStatusList(mixins.LoginRequiredMixin, generic.ListView):
    context_object_name = 'health_center_status'
    template_name = 'prediction/current_status.html'

    def get_queryset(self):
        return models.HealthCenterStatus.objects.filter(health_center__id=self.request.user.health_center.id)


class HealthCenterStatusCreate(mixins.LoginRequiredMixin, generic.CreateView):
    # form_class = forms.HealthCenterStatusForm
    model = models.HealthCenterStatus
    
    fields = ('health_center', 'beds', 'icus', 'respirators', 'occupied_beds', 'occupied_icus', 'occupied_respirators',)
    
    template_name = 'prediction/status_create.html'
    success_url = reverse_lazy('prediction:current_status')
    
    def get_form(self, form_class=None):
        form = super(HealthCenterStatusCreate, self).get_form(form_class)
        form.fields['health_center'].widget = forms.HiddenInput()
        return form
    
    def get_initial(self):
        init = super(HealthCenterStatusCreate, self).get_initial()
        init['health_center'] = self.request.user.health_center
        return init

    def form_valid(self, form):      
        query_set = []

        if self.request.method == 'POST':
            query_set = models.HealthCenterStatus.objects.filter(
                health_center__id=self.request.POST['health_center'],
                date=date.today()
            )

        if len(query_set) > 0:
            messages.error(self.request, 'O registro de hoje para esta unidade já está cadastrado.')
            return super(HealthCenterStatusCreate, self).form_invalid(form)
        
        print(self.request.POST)

        resource_list = [
            (self.request.POST['occupied_beds'], self.request.POST['beds']),
            (self.request.POST['occupied_icus'], self.request.POST['icus']),
            (self.request.POST['occupied_respirators'], self.request.POST['respirators'])
        ]

        for occupied_resource, resource in resource_list:
            if int(occupied_resource) > int(resource):
                messages.error(self.request, 'As quantidades de recursos ocupados não pode ser maior que a de recursos totais.')
                return super(HealthCenterStatusCreate, self).form_invalid(form)

        utils.create_log(self.request, 'C', 'RE')
        messages.success(self.request, 'Registro diário da unidade atualizado.')

        return super(HealthCenterStatusCreate, self).form_valid(form)

def delete(request, pk):
    query_set = models.HealthCenterStatus.objects.filter(pk=pk)
    query_set[0].delete()
    context = {
        'health_center_status': models.HealthCenterStatus.objects.filter(
            health_center__id=request.user.health_center.id
        )
    }
    return render(request, 'prediction/current_status.html', context)

