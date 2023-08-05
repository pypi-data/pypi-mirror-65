import numpy as np
from skultrafast import unit_conversions
from lmfit import model
import lmfit
import inspect
import sympy



def peak_decay(wl, t, A, Ac, xc, w, tau, angle, peak_type='lor'):
    x = (wl[None, :] - xc) / w
    if peak_type == 'lor':
        yperp = (A * np.exp(-t[:, None] / tau) + Ac) * 1 / (1 + x**2)
    elif peak_type == 'gauss':
        yperp = (A * np.exp(-t[:, None] / tau) + Ac) * np.exp(-.5 * x**2)
    ypara = unit_conversions.angle2dichro(angle) * yperp
    return np.dstack((yperp, ypara))


def peak_const(wl, t, A, xc, w, angle, peak_type='lor'):
    x = (wl[None, :] - xc) / w
    if peak_type == 'lor':
        yperp = A * 1 / (1 + x**2)
    elif peak_type == 'gauss':
        yperp = A * np.exp(-.5 * x**2)  #1/(1+x**2)
    #
    ypara = unit_conversions.angle2dichro(angle) * yperp
    return np.dstack((yperp, ypara))


print(inspect.signature(peak_const))


class ModelBuilder:
    def __init__(self, wl: np.ndarray, t: np.ndarray):
        self.funcs = []
        self.args = []

    @property
    def n(self):
        return len(self.funcs)

    def add_decaying(self,
                     A: float,
                     Ac: float,
                     xc: float,
                     w: float,
                     tau: float,
                     angle: float,
                     peak_type: str = 'lor') -> int:
        self.funcs.append(peak_decay)
        self.args.append((A, Ac, xc, w, tau, angle, peak_type))
        return len(self.funcs)

    def add_constant(self, A, xc, w, angle, peak_type='lor'):  #
        self.funcs.append(peak_const)
        self.args.append(A, xc, w, angle, peak_type='lor')
        return len(self.funcs)

    def build_model(self, equal_list=None):
        if equal_list is None:
            equal_list = []
        params = lmfit.Parameters()
        all_names = []
        for i, (f, a) in enumerate(zip(self.funcs, self.args)):
            names = list(inspect.signature(f).parameters)
            for name in names[2:]:                
                if name in equal_list:
                    if name in all_names:
                        pass
                    else:
                        all_names.append(name)
                else:
                    all_names.append(f"{name}_{i:d}")
            
            def wrap(p: lmfit.Parameters):                
                args = p.valuesdict[]                
                return        


def full_model(wl,
               t,
               sum_up=True,
               tau1=30,
               A1=-.4,
               xc1=1661,
               w1=8,
               angle1=45,
               A2=-.2,
               xc2=1690,
               w2=8,
               angle2=35,
               A3=0.1,
               xc3=1703,
               w3=4,
               angle3=10,
               A4=0.2,
               xc4=1669,
               w4=4,
               angle4=45):
    d1 = peak_decay(wl, t, 0, A1, xc1, w1, tau1, angle1, peak_type='lor')
    d2 = peak_decay(wl, t, 0, A2, xc2, w2, tau1, angle2, peak_type="lor")
    d3 = peak_decay(wl, t, -A3, A3, xc3, w3, tau1, angle3, peak_type='lor')
    d4 = peak_decay(wl, t, -A4, A4, xc4, w4, tau1, angle4, peak_type='lor')

    if sum_up:
        return (d1+d2+d3+d4) + np.sum((A1, A2, A3, A4)) * 0.001
    else:
        return d1, d2, d3, d4



if __name__ == "__main__":
    wl = np.linspace(-100, 100, 300)
    t = np.linspace(0, 10, 50)
    mb = ModelBuilder(wl, t)
    mb.add_decaying(1, 0.2, -50, 30, 10, 45)
    mb.build_model()