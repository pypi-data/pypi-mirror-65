# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 07:37:35 2019

@author: yoelr
"""
from .base import PhaseMixtureProperty, display_asfunctor

__all__ = ('Mixture',
           'ideal_mixture',
           'IdealMixtureProperty',)

# %% Mixture methods

mixture_phaseT_methods = ('Cn',)
mixture_hidden_T_methods = ('_H',)
mixture_phaseTP_methods = ('mu', 'V', 'kappa')
mixture_hidden_phaseTP_methods = ('_H_excess', '_S_excess', '_S')
mixture_T_methods  = ('Hvap', 'sigma', 'epsilon')
mixture_methods = (*mixture_phaseT_methods,
                   *mixture_phaseTP_methods,
                   *mixture_hidden_T_methods,
                   *mixture_hidden_phaseTP_methods,
                   *mixture_T_methods)


# %% Mixture properties

class IdealMixtureProperty:
    """
    Create an IdealMixtureProperty object that calculates mixture properties
    based on the molar weighted sum of pure chemical properties.
    
    Parameters
    ----------
    properties : Iterable[function(T, P)]
        Chemical property functions of temperature and pressure.
    var : str
        Description of thermodynamic variable returned.
    
    """
    __slots__ = ('var', 'properties',)

    def __init__(self, properties, var):
        self.properties = tuple(properties)
        self.var = var

    @classmethod
    def from_chemicals(cls, chemicals, var):
        getfield = getattr
        return cls([getfield(i, var) for i in chemicals], var)

    def __call__(self, mol, T, P=None):
        return sum([j * i(T, P) for i, j in zip(self.properties, mol) if j])
    
    def __repr__(self):
        return f"<{display_asfunctor(self)}>"


# %% Ideal mixture phase property
        
def group_properties_by_phase(phase_properties):
    hasfield = hasattr
    getfield = getattr
    iscallable = callable
    properties_by_phase = {'s': [],
                           'l': [],
                           'g': []}
    for phase, properties in properties_by_phase.items():
        for phase_property in phase_properties:
            if iscallable(phase_property) and hasfield(phase_property, phase):
                prop = getfield(phase_property, phase)
            else:
                prop = phase_property
            properties.append(prop)
    return properties_by_phase
    
def build_ideal_PhaseMixtureProperty(chemicals, var):
    setfield = setattr
    getfield = getattr
    phase_properties = [getfield(i, var) for i in chemicals]
    new = PhaseMixtureProperty.__new__(PhaseMixtureProperty)
    for phase, properties in group_properties_by_phase(phase_properties).items():
        setfield(new, phase, IdealMixtureProperty(properties, var))
    new.var = var
    return new


# %% Ideal mixture


class Mixture:
    """
    Create an Mixture object for estimating mixture properties.
    
    Parameters
    ----------
    description : str
        Description of mixing rules used.
    Cn : PhaseZTProperty
        Molar heat capacity functor [J/mol/K].
    H : PhaseZTProperty
        Enthalpy functor [J/mol].
    S : PhaseZTPProperty
        Entropy functor [J/mol].
    H_excess : PhaseZTPProperty
        Excess enthalpy functor [J/mol].
    S_excess : PhaseZTPProperty
        Excess entropy functor [J/mol].
    mu : PhaseZTPProperty
        Dynamic viscosity functor [Pa*s].
    V : PhaseZTPProperty
        Molar volume functor [m^3/mol].
    kappa : PhaseZTPProperty
        Thermal conductivity functor [W/m/K].
    Hvap : ZTProperty
        Heat of vaporization functor [J/mol]
    sigma : ZTProperty
        Surface tension functor [N/m].
    epsilon : ZTProperty
        Relative permitivity functor [-]
    rigorous_energy_balance=True : bool
        Whether to rigorously solve for temperature
        in energy balance or simply approximate.
    include_excess_energies=False : bool
        Whether to include excess energies
        in enthalpy and entropy calculations.
    
    Attributes
    ----------
    description : str
        Description of mixing rules used.
    rigorous_energy_balance : bool
        Whether to rigorously solve for temperature
        in energy balance or simply approximate.
    include_excess_energies : bool
        Whether to include excess energies
        in enthalpy and entropy calculations.
    Cn(phase, z, T) : PhaseZTProperty
        Molar heat capacity functor [J/mol/K].
    mu(phase, T, P) : PhaseZTPProperty
        Dynamic viscosity functor [Pa*s].
    V(phase, T, P) : PhaseZTPProperty
        Molar volume functor [m^3/mol].
    kappa(phase, T, P) : PhaseZTPProperty
        Thermal conductivity functor [W/m/K].
    Hvap(phase, T, P) : ZTProperty
        Heat of vaporization functor [J/mol]
    sigma(phase, T, P) : ZTProperty
        Surface tension functor [N/m].
    epsilon(phase, T, P) : ZTProperty
        Relative permitivity [-]
    
    
    """
    __slots__ = ('rule',
                 'rigorous_energy_balance',
                 'include_excess_energies',
                 *mixture_methods)
    
    def __init__(self, rule, Cn, H, S, H_excess, S_excess,
                 mu, V, kappa, Hvap, sigma, epsilon,
                 rigorous_energy_balance=True,
                 include_excess_energies=False):
        self.rule = rule
        self.rigorous_energy_balance = rigorous_energy_balance
        self.include_excess_energies = include_excess_energies
        self.Cn = Cn
        self.mu = mu
        self.V = V
        self.kappa = kappa
        self.Hvap = Hvap
        self.sigma = sigma
        self.epsilon = epsilon
        self._H = H
        self._S = S
        self._H_excess = H_excess
        self._S_excess = S_excess
    
    def H(self, phase, z, T, P):
        """Return enthalpy in J/mol"""
        H = self._H(phase, z, T)
        if self.include_excess_energies:
            H += self._H_excess(phase, z, T, P)
        return H
    
    def S(self, phase, z, T, P):
        """Return entropy in J/mol"""
        S = self._S(phase, z, T, P)
        if self.include_excess_energies:
            S += self._S_excess(phase, z, T, P)
        return S
    
    def solve_T(self, phase, z, H, T_guess, P):
        """Solve for temperature in Kelvin"""
        # First approximation
        H_guess = self.H(phase, z, T_guess, P)
        if (H - H_guess) < 1e-3: return T_guess
        Cn = self.Cn(phase, z, T_guess)
        T = T_guess + (H - H_guess) / Cn
        if self.rigorous_energy_balance:
            # Solve enthalpy by iteration
            it = 3
            it2 = 0
            while abs(T - T_guess) > 0.05:
                T_guess = T
                if it == 3:
                    it = 0
                    it2 += 1
                    if it2 > 5: break # Its good enough, no need to find exact solution
                    Cn = self.Cn(phase, z, T)
                else:
                    it += 1
                T += (H - self.H(phase, z, T, P))/Cn
        return T
                
    def xsolve_T(self, phase_data, H, T_guess, P):
        """Solve for temperature in Kelvin"""
        # First approximation
        phase_data = tuple(phase_data)
        H_guess = self.xH(phase_data, T_guess, P)
        if (H - H_guess) < 1e-3: return T_guess
        Cn = self.xCn(phase_data, T_guess)
        T = T_guess + (H - H_guess)/Cn
        if self.rigorous_energy_balance:
            # Solve enthalpy by iteration
            it = 3
            it2 = 0
            while abs(T - T_guess) > 0.05:
                T_guess = T
                if it == 3:
                    it = 0
                    it2 += 1
                    if it2 > 5: break # Its good enough, no need to find exact solution
                    Cn = self.xCn(phase_data, T_guess)
                else:
                    it += 1
                T += (H - self.xH(phase_data, T, P))/Cn
        return T
    
    def xCn(self, phase_data, T):
        Cn = self.Cn
        return sum([Cn(phase, z, T) for phase, z in phase_data])
    
    def xH(self, phase_data, T, P):
        H = self._H
        H_total = sum([H(phase, z, T) for phase, z in phase_data])
        if self.include_excess_energies:
            H_excess = self._H_excess
            H_total += sum([H_excess(phase, z, T, P) for phase, z in phase_data])
        return H_total
    
    def xS(self, phase_data, T, P):
        S = self._S
        S_total = sum([S(phase, z, T, P) for phase, z in phase_data])
        if self.include_excess_energies:
            S_excess = self._S_excess
            S_total += sum([S_excess(phase, z, T, P) for phase, z in phase_data])
        return S_total
    
    def xV(self, phase_data, T, P):
        V = self.V
        return sum([V(phase, z, T, P) for phase, z in phase_data])
    
    def xmu(self, phase_data, T, P):
        mu = self.mu
        return sum([mu(phase, z, T, P) for phase, z in phase_data])
    
    def xkappa(self, phase_data, T, P):
        kappa = self.kappa
        return sum([kappa(phase, z, T, P) for phase, z in phase_data])
    
    def __repr__(self):
        return f"{type(self).__name__}(rule={repr(self.rule)}, ..., rigorous_energy_balance={self.rigorous_energy_balance}, include_excess_energies={self.include_excess_energies})"
    
    def _info(self):
        return (f"{type(self).__name__}(\n"
                f"    rule={repr(self.rule)}, ...\n"
                f"    rigorous_energy_balance={self.rigorous_energy_balance},\n"
                f"    include_excess_energies={self.include_excess_energies}\n"
                 ")")
    
    def show(self):
        print(self._info())
    _ipython_display_ = show
        
    
def ideal_mixture(chemicals,
                  rigorous_energy_balance=True,
                  include_excess_energies=False):
    """
    Create a Mixture object that computes mixture properties using ideal mixing rules.
    
    Parameters
    ----------
    chemicals : Chemicals
        For retrieving pure component chemical data.
    rigorous_energy_balance=True : bool
        Whether to rigorously solve for temperature in energy balance or simply approximate.
    include_excess_energies=False : bool
        Whether to include excess energies in enthalpy and entropy calculations.

    """
    chemicals = tuple(chemicals)
    Cn =  build_ideal_PhaseMixtureProperty(chemicals, 'Cn')
    H =  build_ideal_PhaseMixtureProperty(chemicals, 'H')
    S = build_ideal_PhaseMixtureProperty(chemicals, 'S')
    H_excess = build_ideal_PhaseMixtureProperty(chemicals, 'H_excess')
    S_excess = build_ideal_PhaseMixtureProperty(chemicals, 'S_excess')
    mu = build_ideal_PhaseMixtureProperty(chemicals, 'mu')
    V = build_ideal_PhaseMixtureProperty(chemicals, 'V')
    kappa = build_ideal_PhaseMixtureProperty(chemicals, 'kappa')
    Hvap = IdealMixtureProperty.from_chemicals(chemicals, 'Hvap')
    sigma = IdealMixtureProperty.from_chemicals(chemicals, 'sigma')
    epsilon = IdealMixtureProperty.from_chemicals(chemicals, 'epsilon')
    return Mixture('ideal mixing', Cn, H, S, H_excess, S_excess,
                   mu, V, kappa, Hvap, sigma, epsilon,
                   rigorous_energy_balance, include_excess_energies)