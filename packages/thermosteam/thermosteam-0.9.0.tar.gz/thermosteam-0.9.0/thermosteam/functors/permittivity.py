# -*- coding: utf-8 -*-

__all__ = ('Permittivity',)

import numpy as np
from .utils import CASDataReader
from .._constants import N_A, epsilon_0, k
from ..base import TDependentHandleBuilder, epsilon

read = CASDataReader(__file__, 'Electrolytes')
_CRC_Permittivity = read('Permittivity (Dielectric Constant) of Liquids.tsv')

@epsilon
def IAPWS_Permittivity(T, Vl,
                       dipole = 6.138E-30, # actual molecular dipole moment of water, in C*m
                       polarizability = 1.636E-40, # actual mean molecular polarizability of water, C^2/J*m^2
                       MW = 0.018015268, # molecular weight of water, kg/mol
                       ih = np.array([1, 1, 1, 2, 3, 3, 4, 5, 6, 7, 10]),
                       jh = np.array([0.25, 1, 2.5, 1.5, 1.5, 2.5, 2, 2, 5, 0.5, 10]),
                       Nh = np.array([0.978224486826, -0.957771379375, 0.237511794148, 0.714692244396,
                   -0.298217036956, -0.108863472196, 0.949327488264E-1, 
                   -.980469816509E-2, 0.165167634970E-4, 0.937359795772E-4, 
                   -0.12317921872E-9])):
    rhom = 1/Vl(T, 101325)
    rho = MW * rhom
    delta = rho/322.
    tau = 647.096/T
    g = (1 + (Nh*delta**ih*tau**jh).sum() + 0.196096504426E-2*delta*(T/228. - 1)**-1.2)
    
    A = N_A*dipole**2*(rhom)*g/epsilon_0/k/T
    B = N_A*polarizability*(rhom)/3./epsilon_0
    return (1. + A + 5.*B + (9. + 2.*A + 18.*B + A**2 + 10.*A*B + 9.*B**2)**0.5)/(4. - 4.*B)

@epsilon
def CRC(T, A, B, C, D):
    return A + B*T + C*T**2 + D*T**3

@TDependentHandleBuilder
def Permittivity(handle, CAS, Vl):
    add_model = handle.add_model
    if Vl and CAS == '7732-18-5':
        add_model(IAPWS_Permittivity.from_args((Vl,)))
    if CAS in _CRC_Permittivity:
        _, CRC_CONSTANT_T, CRC_permittivity, A, B, C, D, Tmin, Tmax = _CRC_Permittivity[CAS]
        args = tuple(0 if np.isnan(x) else x for x in [A, B, C, D])
        Tmin = 0 if np.isnan(Tmin) else Tmin
        Tmax = 1e6 if np.isnan(Tmax) else Tmax
        add_model(CRC.from_args(args), Tmin, Tmax, name='CRC')
        add_model(CRC_permittivity, Tmin, Tmax, name='CRC_constant')


#from scipy.constants import pi, N_A, k
##from scipy.optimize import fsolve
#
#def calc_molecular_polarizability(T, Vm, dipole, permittivity):
#    dipole *= 3.33564E-30
#    rhom = 1./Vm
#    alpha = (-4*N_A*permittivity*dipole**2*pi*rhom - 8*N_A*dipole**2*pi*rhom + 9*T*permittivity*k - 9*T*k)/(12*N_A*T*k*pi*rhom*(permittivity + 2))
#
##    def to_solve(alpha):
##        ans = rhom*(4*pi*N_A*alpha/3. + 4*pi*N_A*dipole**2/9/k/T) - (permittivity-1)/(permittivity+2)
##        return ans
##
##    alpha = fsolve(to_solve, 1e-30)
#
#    return alpha

#
#print(calc_molecular_polarizability(T=293.15, Vm=0.023862, dipole=0.827, permittivity=1.00279))
#3.61E-24

