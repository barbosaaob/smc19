from django.shortcuts import render, redirect
from django.views import View

from django.views import generic
from django.views import View
from django.contrib.auth import mixins
from django.contrib import messages

from . import forms

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import six
from .python_scripts import mathmodels

from matplotlib.backends.backend_agg import FigureCanvasAgg


class SirSeirMathModel(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'mathmodels/sir_seir_math_model.html'

    def sir(self, N, S0, I0, R0, beta, gamma, days):
        fig = plt.figure(figsize=(8, 4), edgecolor='k')

        S, I, R = mathmodels.compute_sir(N=N, S0=N*S0, I0=N*I0, R0=N*R0, beta=beta, gamma=gamma, days=days)
        mathmodels.plot_sir(S, I, R, days)

        tmp = six.StringIO()
        fig.savefig(tmp, format='svg', bbox_inches='tight', dpi=250)

        return (tmp.getvalue(), np.max(I), np.argmax(I))

    def basic_seir(self, N, S0, E0, I0, R0, alpha, beta, gamma, days):
        fig = plt.figure(figsize=(8, 4), edgecolor='k')

        t_max = days ## supus q é a quantidade de dias
        dt = 1
        t = np.linspace(0, t_max, int(t_max/dt) + 1)
        init_vals = S0, E0, I0, R0
        params = alpha, beta, gamma

        S, E, I, R = mathmodels.base_seir_model(N, init_vals, params, t)
        mathmodels.plot_seir(S, E, I, R, int(t_max/dt)+1)
        
        tmp = six.StringIO()
        fig.savefig(tmp, format='svg', bbox_inches='tight', dpi=250)

        return (tmp.getvalue(), np.max(I), np.argmax(I))

    def seir(self, N, S0, E0, I0, R0, alpha, beta, gamma, rho, days):
        fig = plt.figure(figsize=(8, 4), edgecolor='k')

        t_max = days
        dt = 1
        t = np.linspace(0, t_max, int(t_max/dt) + 1)

        init_vals = S0, E0, I0, R0
        params = alpha, beta, gamma, rho
        
        S, E, I, R = mathmodels.seir_model_with_soc_dist(N, init_vals, params, t)
        mathmodels.plot_seir(S, E, I, R, int(t_max/dt)+1)

        tmp = six.StringIO()
        fig.savefig(tmp, format='svg', bbox_inches='tight', dpi=250)

        return (tmp.getvalue(), np.max(I), np.argmax(I))

    def adapt_seir(self, N, S0, E0, I0, R0, alpha, beta, gamma, rho_iso, rho_relax, changes, days, population_proportion):
        fig = plt.figure(figsize=(8, 4), edgecolor='k')

        t_max = days
        dt = 1 # time step (set to 1 day)
        t = np.linspace(0, t_max, int(t_max/dt) + 1) #sampling in time
        init_vals = S0, E0, I0, R0
        params = alpha, beta, gamma, rho_iso, rho_relax

        S, E, I, R, L, U = mathmodels.seir_model_with_soc_dist_adap(init_vals, params, t, N, changes, population_proportion)
        mathmodels.plot_seir_with_soc_dist2(S, E, I, R, L, U,int(t_max/dt)+1)

        tmp = six.StringIO()
        fig.savefig(tmp, format='svg', bbox_inches='tight', dpi=250)

        return (tmp.getvalue(), np.max(I), np.argmax(I))

    def get(self, request):
        form = forms.SirSeirForm(request.GET)
        form2 = forms.ProportionsForm(request.GET)

        if form.is_valid() and form2.is_valid():
            N = form.cleaned_data['N']
            S0 = form.cleaned_data['S0']
            E0 = form.cleaned_data['E0']
            I0 = form.cleaned_data['I0']
            R0 = form.cleaned_data['R0']
            alpha = form.cleaned_data['alpha']
            beta = form.cleaned_data['beta']
            gamma = form.cleaned_data['gamma']
            rho = form.cleaned_data['rho']
            rho_relax = form.cleaned_data['rho_relax']
            changes = form.cleaned_data['changes']
            days = form.cleaned_data['days']
            model = form.cleaned_data['model']

            if model == 'sir':
                title = 'SIR'
                graph, max_infected, day_D = self.sir(N=N, S0=S0, I0=I0, R0=R0, beta=beta, gamma=gamma, days=days)
            elif model == 'basic_seir':
                title = 'SEIR básico'
                graph, max_infected, day_D = self.basic_seir(N=N, S0=S0, E0=E0, I0=I0, R0=R0, alpha=alpha, beta=beta, gamma=gamma, days=days)
            elif model == 'adapt_seir':
                population_proportion = {}
                for k,v in form2.cleaned_data.items():
                    population_proportion[k.replace('from','').replace('to','-').replace('-80plus','+')] = v

                title = 'SEIR c/ dist. social adapt.'
                graph, max_infected, day_D = self.adapt_seir(N=N, S0=S0, E0=E0, I0=I0, R0=R0, alpha=alpha, beta=beta, gamma=gamma, rho_iso=rho, rho_relax=rho_relax, changes=[changes], days=days, population_proportion=population_proportion)
            else:
                title = 'SEIR c/ dist. social'
                graph, max_infected, day_D = self.seir(N=N, S0=S0, E0=E0, I0=I0, R0=R0, alpha=alpha, beta=beta, gamma=gamma, rho=rho, days=days)

            context = {
                'form': form,
                'form2': form2,
                'graph': graph,
                'max_infected': int(max_infected),
                'day_D': day_D,
                'title':title
            }

            return render(request, self.template_name, context=context)
        
        form = forms.SirSeirForm()
        form2 = forms.ProportionsForm()
        return render(request, self.template_name, {'form': form, 'form2': form2})
