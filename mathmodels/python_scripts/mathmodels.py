import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# The SIR model differential equations.
def deriv(y, t, N , beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

def compute_sir(N=1000, S0=0, I0=1, R0=0, beta=1.75, gamma=0.5, days=160):
    """
    Total population, N.
    Initial number of infected and recovered individuals, I0 and R0.
    Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
    """
    
    # A grid of time points (in days)
    #t = np.linspace(0, 160, 160)
    t = np.linspace(0, days, days)

    # Initial conditions vector
    y0 = S0, I0, R0
    # Integrate the SIR equations over the time grid, t.
    ret = odeint(deriv, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T

    return (S, I, R)

def plot_sir(S, I, R, days):
    # Plot the data on three separate curves for S(t), I(t) and R(t)
    t = np.linspace(0, days, days)
    plt.plot(t, S/1000, 'b', alpha=0.5, lw=2, label='Susceptible')
    plt.plot(t, I/1000, 'r', alpha=0.5, lw=2, label='Infected')
    plt.plot(t, R/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
    legend = plt.legend()
    legend.get_frame().set_alpha(0.5)


#### BEGIN SEIR BÁSICO
def base_seir_model(N, init_vals, params, t):
    S_0, E_0, I_0, R_0 = init_vals
    S, E, I, R = [S_0], [E_0], [I_0], [R_0]
    alpha, beta, gamma = params
    dt = t[1] - t[0]
    for _ in t[1:]:
        next_S = S[-1] - (beta*S[-1]*I[-1])*dt
        next_E = E[-1] + (beta*S[-1]*I[-1] - alpha*E[-1])*dt
        next_I = I[-1] + (alpha*E[-1] - gamma*I[-1])*dt
        next_R = R[-1] + (gamma*I[-1])*dt
        S.append(next_S)
        E.append(next_E)
        I.append(next_I)
        R.append(next_R)
    S = np.array(S)*N
    E = np.array(E)*N
    I = np.array(I)*N
    R = np.array(R)*N
    return (S, E, I, R)

def plot_seir(S, E, I, R, days):
    # Plot the data on three separate curves for S(t), E(t), I(t) and R(t)
    t = np.linspace(0, days, days)
    plt.plot(t, S/1000, 'b', alpha=0.5, lw=2, label='Susceptible')
    plt.plot(t, E/1000, 'k', alpha=0.5, lw=2, label='Exposed')
    plt.plot(t, I/1000, 'r', alpha=0.5, lw=2, label='Infected')
    plt.plot(t, R/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
    legend = plt.legend()
    legend.get_frame().set_alpha(0.5)
#### END SEIR BÁSICO

#### BEGIN SEIR COM DISTANCIAMENTO SOCIAL
def seir_model_with_soc_dist(N, init_vals, params, t):
    S_0, E_0, I_0, R_0 = init_vals
    S, E, I, R = [S_0], [E_0], [I_0], [R_0]
    alpha, beta, gamma, rho = params
    dt = t[1] - t[0]
    for _ in t[1:]:
        next_S = S[-1] - (rho*beta*S[-1]*I[-1])*dt
        next_E = E[-1] + (rho*beta*S[-1]*I[-1] - alpha*E[-1])*dt
        next_I = I[-1] + (alpha*E[-1] - gamma*I[-1])*dt
        next_R = R[-1] + (gamma*I[-1])*dt
        S.append(next_S)
        E.append(next_E)
        I.append(next_I)
        R.append(next_R)
    S = np.array(S)*N
    E = np.array(E)*N
    I = np.array(I)*N
    R = np.array(R)*N
    return (S, E, I, R)

def plot_seir_with_soc_dist(S, E, I, R, days):
    # Plot the data on three separate curves for S(t), E(t), I(t) and R(t)
    t = np.linspace(0, days, days)
    plt.plot(t, S/1000, 'b', alpha=0.5, lw=2, label='Susceptible')
    plt.plot(t, E/1000, 'k', alpha=0.5, lw=2, label='Exposed')
    plt.plot(t, I/1000, 'r', alpha=0.5, lw=2, label='Infected')
    plt.plot(t, R/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
    plt.grid
    legend = plt.legend()
    legend.get_frame().set_alpha(0.5)
#### END SEIR COM DISTANCIAMENTO SOCIAL

#### BEGIN SEIR COM DISTANCIAMENT SOCIAL ADAPTATIVO
def proportions(S, I, R, population_proportion, symptomatic=0.2):
  # proporcoes
  print(population_proportion.keys())
  Ip = {
      "0-9":   population_proportion["0-9"] * I * symptomatic,
      "10-19": population_proportion["10-19"] * I * symptomatic,
      "20-29": population_proportion["20-29"] * I * symptomatic,
      "30-39": population_proportion["30-39"] * I * symptomatic,
      "40-49": population_proportion["40-49"] * I * symptomatic,
      "50-59": population_proportion["50-59"] * I * symptomatic,
      "60-69": population_proportion["60-69"] * I * symptomatic,
      "70-79": population_proportion["70-79"] * I * symptomatic,
      "80+":   population_proportion["80+"] * I * symptomatic
  }
  Sp = {
      "0-9":   population_proportion["0-9"] * S,
      "10-19": population_proportion["10-19"] * S,
      "20-29": population_proportion["20-29"] * S,
      "30-39": population_proportion["30-39"] * S,
      "40-49": population_proportion["40-49"] * S,
      "50-59": population_proportion["50-59"] * S,
      "60-69": population_proportion["60-69"] * S,
      "70-79": population_proportion["70-79"] * S,
      "80+":   population_proportion["80+"] * S
  }

  Rp = {
      "0-9":   population_proportion["0-9"] * R,
      "10-19": population_proportion["10-19"] * R,
      "20-29": population_proportion["20-29"] * R,
      "30-39": population_proportion["30-39"] * R,
      "40-49": population_proportion["40-49"] * R,
      "50-59": population_proportion["50-59"] * R,
      "60-69": population_proportion["60-69"] * R,
      "70-79": population_proportion["70-79"] * R,
      "80+":   population_proportion["80+"] * R
  }

  H = {
      "0-9":    0.1/100 * Ip["0-9"],
      "10-19":  0.3/100 * Ip["10-19"],
      "20-29":  1.2/100 * Ip["20-29"],
      "30-39":  3.2/100 * Ip["30-39"],
      "40-49":  4.9/100 * Ip["40-49"],
      "50-59": 10.2/100 * Ip["50-59"],
      "60-69": 16.6/100 * Ip["60-69"],
      "70-79": 24.3/100 * Ip["70-79"],
      "80+":   27.3/100 * Ip["80+"]
  }

  ICU = {
      "0-9":      5/100 * H["0-9"],
      "10-19":    5/100 * H["10-19"],
      "20-29":    5/100 * H["20-29"],
      "30-39":    5/100 * H["30-39"],
      "40-49":  6.3/100 * H["40-49"],
      "50-59": 12.2/100 * H["50-59"],
      "60-69": 27.4/100 * H["60-69"],
      "70-79": 43.2/100 * H["70-79"],
      "80+":   70.9/100 * H["80+"]
  }

  # D = {
  #     "0-9":   0.002/100 * ICU["0-9"],
  #     "10-19": 0.006/100 * ICU["10-19"],
  #     "20-29":  0.03/100 * ICU["20-29"],
  #     "30-39":  0.08/100 * ICU["30-39"],
  #     "40-49":  0.15/100 * ICU["40-49"],
  #     "50-59":   0.6/100 * ICU["50-59"],
  #     "60-69":   2.2/100 * ICU["60-69"],
  #     "70-79":   5.1/100 * ICU["70-79"],
  #     "80+":     9.3/100 * ICU["80+"]
  # }
  death_constant = 1e-3
  D = {
      "0-9":   0.00002 * Ip["0-9"]/symptomatic,
      "10-19": 0.00006 * Ip["10-19"]/symptomatic,
      "20-29": 0.0003 * Ip["20-29"]/symptomatic,
      "30-39": 0.0008 * Ip["30-39"]/symptomatic,
      "40-49": 0.0015 * Ip["40-49"]/symptomatic,
      "50-59": 0.006 * Ip["50-59"]/symptomatic,
      "60-69": 0.022 * Ip["60-69"]/symptomatic,
      "70-79": 0.051 * Ip["70-79"]/symptomatic,
      "80+":   0.093 * Ip["80+"]/symptomatic
  }
  return (Sp, Ip, Rp, H, ICU, D)

def seir_model_with_soc_dist_adap(init_vals, params, t, N, changes, population_proportion):
    S_0, E_0, I_0, R_0 = init_vals
    S, E, I, R = [S_0], [E_0], [I_0], [R_0]
    L = np.zeros(len(t))
    U = np.zeros(len(t))
    alpha, beta, gamma, rho_iso, rho_relax = params
    dt = t[1] - t[0]
    rho = rho_iso
    isolated = True
    next_change=0
    k=0
    for today in t[1:]:
      #print(today)
      if next_change<len(changes):
        if today == changes[next_change]:
          next_change=next_change+1
          if isolated:
            isolated=False
            rho = rho_relax
          else:
            isolated=True
            rho = rho_iso
      next_S = S[-1] - (rho*beta*S[-1]*I[-1])*dt
      next_E = E[-1] + (rho*beta*S[-1]*I[-1] - alpha*E[-1])*dt
      next_I = I[-1] + (alpha*E[-1] - gamma*I[-1])*dt
      next_R = R[-1] + (gamma*I[-1])*dt
      Sp, Ip, Rp, H, ICU, D = proportions(next_S, (alpha*E[-1])*dt, next_R, population_proportion)
      S.append(next_S)
      E.append(next_E)
      I.append(next_I)
      R.append(next_R)

      L_total = 0
      for age, population in H.items():
        L_total += population
      for day in range(k,k+8):
        if(day<L.size):
         L[day] += L_total*N

      U_total = 0
      for age, population in ICU.items():
        U_total += population
      for day in range(k+3,k+13): # soma os dias de UTI
        if(day<U.size):
         U[day] += U_total*N
      for day in range(k+3,k+8): # subtrai dias do leito que está na UTI
        if(day<U.size):
         L[day] -= U_total*N
      for day in range(k+13,k+16): # soma dias finais de leito dos que foram pra UTI
        if(day<U.size):
         L[day] += U_total*N

      k=k+1
    S = np.array(S)*N
    E = np.array(E)*N
    I = np.array(I)*N
    R = np.array(R)*N
    return (S, E, I, R, L,U)

def plot_seir_with_soc_dist2(S, E, I, R, L, U,days):
    # Plot the data on three separate curves for S(t), E(t), I(t) and R(t)
    t = np.linspace(0, days, days)


    plt.subplot(1, 2, 1)
    plt.plot(t, S/1000, 'b', alpha=0.5, lw=2, label='Suscetíveis')
    plt.plot(t, E/1000, 'k', alpha=0.5, lw=2, label='Em incubação')
    plt.plot(t, I/1000, 'r', alpha=0.5, lw=2, label='Doentes')
    plt.plot(t, R/1000, 'g', alpha=0.5, lw=2, label='Recuperados com imunidade')

    plt.subplot(1, 2, 2)
    plt.plot(t, L, 'y', alpha=0.5, lw=2, label='Leitos ocupados')
    plt.plot(t, U, 'm', alpha=0.5, lw=2, label='UTIs ocupadas')
  #  plt.ylim([0,125])
    legend = plt.legend()
    legend.get_frame().set_alpha(0.5)
#### END SEIR COM DISTANCIAMENT SOCIAL ADAPTATIVO