# Copyright (C) 2019 Charlie Hoy <charlie.hoy@ligo.org>
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


from pesummary.core.plots.main import _PlotGeneration


class Notebook(_PlotGeneration):
    """Class to handle the generation of a python notebook to display plots

    Parameters
    ----------

    Attributes
    ----------
    """
    def __init__(self, savedir=None, webdir=None, labels=None, samples=None,
        kde_plot=False, same_parameters=None, injection_data=None, colors=None, 
        priors={}, include_prior=False, weights=None,
        disable_comparison=False, linestyles=None, disable_interactive=False,
    ):
        super(Notebook, self).__init__(
            savedir=savedir, webdir=webdir, labels=labels, samples=samples,
            kde_plot=kde_plot, same_parameters=same_parameters,
            injection_data=injection_data, colors=colors, prior=prior,
            include_prior=include_prior, weights=weights,
            disable_comparison=disable_comparison, linestyles=linestyles,
            disable_interaction=disable_interactive
        )

    def generate_notebook(self):
        """
        """
        import IPython.nbformat.current as nbf

        nb = nbf.read(open('test.py', 'r'), 'py')
        nbf.write(nb, open('test.ipynb', 'w'), 'ipynb')
