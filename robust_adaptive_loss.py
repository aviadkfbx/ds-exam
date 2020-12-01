from typing import Callable, Tuple

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize

Vector = np.ndarray


def rho(x: Vector, alpha: float, c: float) -> Vector:
    assert c > 0
    _base = 0.5*((x/c)**2)
    if alpha == 2:
        return _base
    elif alpha == 0:
        return np.log(_base + 1)
    elif alpha == -float('inf'):
        return 1-np.exp(-_base)
    else:
        nom = abs(alpha - 2)
        r = nom / alpha
        r *= ((2*_base/nom + 1)**(alpha/2)-1)
        return r


def z(alpha: float) -> float:
    int_ = quad(lambda x: rho(x, alpha, 1), -np.inf, np.inf)[0]
    return min(int_, 10**2)


def objective_generator(x: np.ndarray,
                        y: Vector,
                        c: float = 1,
                        redundant: bool = False,
                        with_control: bool = True,
                        approx_control: bool = True) -> Callable[[Vector], float]:
    assert c > 0
    assert x.shape[0] == y.shape[0]
    assert y.shape[0] == y.size

    def redundant_objective(pars: np.ndarray) -> float:
        k = pars.size - 1
        n = x.shape[0]
        assert k == x.shape[1]
        alpha = 2
        assert 0 <= alpha <= 2
        beta = pars[1:].reshape(k, 1)
        mu = x.dot(beta)
        e = y.reshape(n, 1) - mu
        loss = rho(e, alpha, c).sum()  # + n*np.log(z(alpha)[0])
        return loss

    def objective(pars: np.ndarray) -> float:
        k = pars.size - 1
        n = x.shape[0]
        assert k == x.shape[1]
        alpha = pars[0]
        beta = pars[1:].reshape(k, 1)
        mu = x.dot(beta)
        e = y.reshape(n, 1) - mu
        loss = rho(e, alpha, c).sum()
        if with_control:
            if approx_control:
                loss -= n * np.log(curve(alpha))
            else:
                loss += n * np.log(z(alpha))
        return loss / n

    if redundant:
        return redundant_objective
    else:
        return objective


def curve(alpha: float) -> float:
    assert alpha >= 0
    if alpha < 4:
        return 9*(alpha - 2)/(4*abs(alpha-2)+1)+alpha+2
    else:
        return (5/18)*np.log(4*alpha - 15) + 8


def optimize(X: np.ndarray,
             y: Vector,
             c: float = 1,
             options: Tuple[Tuple[str, object], ...] = (('maxfev', 5000),)):
    assert c > 0

    f = objective_generator(X, y, c)
    pars0 = np.zeros(X.shape[1] + 1)
    return minimize(f, pars0, method='Nelder-Mead', options={k: v for k, v in options})
