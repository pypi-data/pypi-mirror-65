# Copyright (C) 2020  Charlie Hoy <charlie.hoy@ligo.org>
                      Michael Puerrer < michael.puerrer@ligo.org>
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from pesummary.core.plots.bounded_1d_kde import Bounded_1d_kde


def draw_conditioned_prior_samples(
    prior_samples, posterior_samples, xlow, xhigh, xN=1000, N=1000
):
    """Return a prior distribution that is conditioned on a given posterior
    via rejection sampling

    Parameters
    ----------
    prior_samples: np.ndarray
        array of prior samples that you wish to condition
    posterior_samples: np.ndarray
        array of posterior samples that you wish to condition on
    xlow: float
        lower bound for grid to be used
    xhigh: float
        upper bound for grid to be used
    xN: int, optional
        Number of points to use within the grid
    N: int, optional
        Number of samples to generate
    """
    prior_KDE = Bounded_1d_kde(prior)
    posterior_KDE = Bounded_1d_kde(posterior)

    x = np.linspace(xlow, xhigh, xN)
    # Find bound so that M*prior > posterior
    idx_nz = np.nonzero(posterior_KDE(x))
    pdf_ratio = prior_KDE(x)[idx_nz] / posterior_KDE(x)[idx_nz]
    M = 1.1 / min(pdf_ratio[np.where(pdf_ratio < 1)])
    
    samples = []
    indices = []
    i = 0
    while i < N:
        x_i = np.random.choice(prior)
        idx_i = np.argmin(np.abs(prior - x_i))
        u = np.random.uniform()
        if u < posterior_KDE(x_i) / (M * prior_KDE(x_i)):
            samples.append(x_i)
            indices.append(idx_i)
            i += 1
    return samples, indices
