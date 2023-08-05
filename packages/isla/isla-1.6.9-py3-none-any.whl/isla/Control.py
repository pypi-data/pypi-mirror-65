import os
import itertools
import copy
import warnings
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

from .LoadFollow import LoadFollow
from .NullComp import NullComp
from .Component import Component
from .LoadComponent import LoadComponent
from .IntermittentComponent import IntermittentComponent
from .StorageComponent import StorageComponent
from .DispatchableComponent import DispatchableComponent
from .SinkComponent import SinkComponent
from .GridComponent import GridComponent
from .SupplementaryComponent import SupplementaryComponent
from .Connector import Connector
from .LoadConnector import LoadConnector
from .IntermittentConnector import IntermittentConnector
from .StorageConnector import StorageConnector
from .DispatchableConnector import DispatchableConnector
from .SinkConnector import SinkConnector
from .GridConnector import GridConnector
from .SupplementaryConnector import SupplementaryConnector

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class Control(object):
    """Power system controller module.

    Parameters
    ----------
    comp_list : list
        List of initialized component objects.
    dt : float, optional
        Size of one timestep [h] (default: 1)
    t_span : float, optional
        Duration of the simulation [h] (default: 8760)

    """

    def __init__(self, comp_list, dt=1, t_span=8760):
        """Initializes the base class."""

        # store parameters
        self.comp_list = comp_list  # list of components
        self.dt = dt  # length of timestep [h]
        self.t_span = t_span  # length of simulation [h]

        # calculate number of simulation points
        self.nt = int(np.ceil(t_span/dt))

        # initialize data storage
        self.algo = None  # dispatch algorithm
        self.infl = 0
        self.yr_proj = 0
        self.proj_capex_tot = 0
        self.proj_capex = 0
        self.proj_caprt = 0
        self.proj_opex_tot = 0
        self.proj_opex = 0
        self.time_ser = dict(  # time series data for power
            (i, np.zeros(self.nt)) for i in comp_list
        )
        self.time_sersoc = dict(  # time series data for SOC
            (i, np.ones(self.nt)) for i in comp_list
            if isinstance(i, StorageComponent)
        )

        # initialize metrics arrays
        self.npv = np.array([])  # NPV
        self.lcoe = np.array([])  # LCOE
        self.lcow = np.array([])  # LCOW
        self.re_frac = np.array([])  # RE-share
        self.lolp = np.array([])  # LOLP

        # initialize rigorous economics metrics
        self.cashflow = {}
        self.irr = np.array([])
        self.capex = np.array([])
        self.opex = np.array([])
        self.repex = np.array([])
        self.ucme = np.array([])

        # initialize capacity factor
        self.capfac = {}

    def simu(
        self, size, spin_res=0.1, yr_proj=20.0, infl=0.1,
        proj_capex=0.0, proj_caprt=0.0, proj_opex=0.0,
        algo=LoadFollow, **kwargs
    ):
        """Simulates a scenario given a set of sizes and calculates the LCOE.

        Parameters
        ----------
        size : dict
            Sizes [kW] or [kWh] of the components. Use component objects as
            keys and sizes as values.
        spin_res : float
            Spinning reserve.
        yr_proj : float
            Project lifetime [yr].
        infl : float
            Inflation rate.
        proj_capex : float
            Capital expenses [USD] of the project.
        proj_caprt : float
            Capital expenses of project as ratio of component CapEx.
        proj_opex : float
            Fixed yearly operating expenses [USD/yr] of the project.
        algo : Dispatch
            The dispatch algorithm to be used.

        Other Parameters
        ----------------
        do_inval : bool
            True if invalid cases should have nan LCOE and RE-share.
        print_prog : bool
            True if calculation progress should be printed.
        print_out : bool
            True if results should be printed. Invokes res_print().

        Notes
        -----
        Sets LCOE to nan when the size combination is infeasible.

        """
        # get keyword arguments
        do_inval = kwargs.pop('do_inval', True)
        print_prog = kwargs.pop('print_prog', True)
        print_out = kwargs.pop('print_out', True)
        self.infl = infl
        self.yr_proj = yr_proj
        self.proj_capex = proj_capex
        self.proj_caprt = proj_caprt
        self.proj_opex = proj_opex

        # initialize for console output
        t0 = time.time()  # time
        mark = np.arange(0, self.nt, self.nt//10)

        # initialize dispatch algorithm
        al = algo(self.comp_list, self.dt, self.t_span, size, spin_res)

        # perform simulation
        for n in range(self.nt):
            al._step()  # increment simulation
            for cp in self.comp_list:
                self.time_ser[cp][n] = cp.pow  # record power at timestep
                if isinstance(cp, StorageComponent):
                    self.time_sersoc[cp][n] = cp.soc  # record SOC at timestep
            if print_prog and n in mark:  # display progress
                print(
                    'Simulation Progress: {:.0f}%'.format((n+1)*100/self.nt),
                    flush=True
                )

        # store completed dispatch algorithm object
        self.algo = al

        # calculate metrics
        self.proj_capex_tot, self.proj_opex_tot = Control._proj_cost(
            al, yr_proj, infl, proj_capex, proj_caprt, proj_opex
        )
        self.npv = Control._npv(
            al, yr_proj, infl, proj_capex, proj_caprt, proj_opex
        )[0]
        self.lcoe = Control._lcoe(
            al, yr_proj, infl, proj_capex, proj_caprt, proj_opex
        )[0]
        self.lcow = Control._lcow(
            al, yr_proj, infl, proj_capex, proj_caprt, proj_opex
        )[0]

        # calculate RE-share
        pow_ldts = np.zeros(self.nt)  # time-series data of total load
        enr_tot = np.zeros(self.nt)  # total energy
        enr_re = np.zeros(self.nt)  # total renewable energy
        for cp in self.comp_list:
            if isinstance(cp, LoadComponent):
                pow_ldts += self.time_ser[cp]  # time series data of total load
        for cp in self.comp_list:
            if not isinstance(cp, LoadComponent) and cp.is_re is not None:
                ld_def = np.maximum(pow_ldts-enr_tot, 0)  # load deficit
                enr_tot += np.minimum(  # add to energy
                    self.time_ser[cp], ld_def  # do not go over load
                )*self.dt
                if cp.is_re:  # add to RE energy
                    enr_re += np.minimum(  # add to energy
                        self.time_ser[cp], ld_def  # do not go over load
                    )*self.dt
        self.re_frac = np.sum(enr_re)/np.sum(enr_tot)

        # check if invalid
        if do_inval and not al.feas:
            self.lcoe = np.nan
            self.re_frac = np.nan

        # print results
        if print_prog:
            t1 = time.time()
            print('Simulation completed in {:.4f} s.'.format(t1-t0))
        if print_out:
            self.res_print()

    def opt(
        self, spin_res=0.1, yr_proj=20.0, infl=0.1,
        proj_capex=0.0, proj_caprt=0.0, proj_opex=0.0, size_max=None,
        size_min=None, iter_simu=10, iter_npv=3, algo=LoadFollow, **kwargs
    ):
        """Set component sizes such that NPV is optimized.

        Parameters
        ----------
        spin_res : float
            Spinning reserve.
        yr_proj : float
            Project lifetime [yr].
        infl : float
            Inflation rate.
        proj_capex : float
            Capital expenses [USD] of the project.
        proj_caprt : float
            Project capital expenses as a fraction of the component CapEx.
        proj_opex : float
            Fixed yearly operating expenses [USD/yr] of the project.
        size_max : dict
            Maximum size constraint. Use the component object as keys and the
            size constraint as values.
        size_min : dict
            Minimum size constraint. Use the component object as keys and the
            size constraint as values.
        iter_simu : int
            Number of cases to simulate simultaneously.
        iter_npv : int
            Number of iterations to find the NPV.

        Other Parameters
        ----------------
        im_range : tuple of float or str
            Boundaries of the search space for the sizes of intermittent power
            components. Input as (min, max). Set to 'auto' to automatically
            find the search space.
        st_range : tuple of float or str
            Boundaries of the search space for the sizes of energy storage
            components. Input as (min, max). Set to 'auto' to automatically
            find the search space.
        dp_range : tuple of float or str
            Boundaries of the search space for the sizes of dispatchable power
            components. Input as (min, max). Set to 'auto' to automatically
            find the search space.
        sk_range : tuple of float or str
            Boundaries of the search space for the sizes of sink power
            components. Input as (min, max). Set to 'auto' to automatically
            find the search space.
        gd_range : tuple of float or str
            Boundaries of the search space for the size of the grid. Input as
            (min, max). Set to 'auto' to automatically find the search space.
        su_range : tuple of float or str
            Boundaries of the search space for the sizes of supplementary power
            components. Input as (min, max). Set to 'auto' to automatically
            find the search space.
        batch_size : int
            Number of simulations to be carried out simultaneously. Prevents
            the program from consuming too much memory.
        print_npv : bool
            True if opimization progress should be printed.
        print_simu : bool
            True if simulation progress should be printed.
        print_res : bool
            True if results should be printed.

        """
        # get keyword arguments
        im_range = kwargs.pop('im_range', 'auto')
        st_range = kwargs.pop('st_range', 'auto')
        dp_range = kwargs.pop('dp_range', 'auto')
        sk_range = kwargs.pop('sk_range', 'auto')
        gd_range = kwargs.pop('gd_range', 'auto')
        su_range = kwargs.pop('su_range', 'auto')
        batch_size = kwargs.pop('batch_size', 10000)
        print_prog = kwargs.pop('print_prog', True)
        print_out = kwargs.pop('print_out', True)
        self.proj_capex = proj_capex
        self.proj_caprt = proj_caprt
        self.proj_opex = proj_opex
        self.infl = infl
        self.yr_proj = yr_proj

        # initialize for console output
        t0 = time.time()  # time

        # replace constraints with empty dict if there are none
        if size_max is None:
            size_max = {}
        if size_min is None:
            size_min = {}

        # check if adj or grid components are present
        has_dp = any(
            isinstance(i, DispatchableComponent) for i in self.comp_list
        )
        has_gd = any(isinstance(i, GridComponent) for i in self.comp_list)
        if has_dp or has_gd:  # no adjustable or grid components
            small_size = True  # use smaller search space
        else:
            small_size = False  # use larger search space

        # use smaller search space if adj or grid is present
        if small_size:  # based on peak
            approx_powmax = sum(  # sum of peak loads
                i.approx_powmax for i in self.comp_list
                if isinstance(i, LoadComponent)
            )
            auto_range = (0, approx_powmax*3.5)
        else:  # based on daily consumption
            approx_enrtot = sum(  # total annual load
                i.approx_enrtot for i in self.comp_list
                if isinstance(i, LoadComponent)
            )
            auto_range = (0, approx_enrtot*2/365)

        # determine number of components to be sized:
        num_comp = sum(  # load is not counted
            1 for i in self.comp_list if not isinstance(i, LoadComponent)
        )

        # initialize
        rng_list = [im_range, st_range, dp_range, sk_range, gd_range, su_range]
        rng_dict = {}  # dict with ranges
        cls_list = [  # list of component classes
            IntermittentComponent, StorageComponent, DispatchableComponent,
            SinkComponent, GridComponent, SupplementaryComponent
        ]

        # assign auto search spaces
        for i in range(6):
            if rng_list[i] == 'auto':  # replace auto ranges
                rng_list[i] = auto_range

        # create dict of ranges
        for cp in self.comp_list:
            for i in range(6):
                if isinstance(cp, cls_list[i]):  # sort by component type
                    rng_dict[cp] = rng_list[i]  # copy the range

        # make a copy of the original ranges
        orig_dict = copy.deepcopy(rng_dict)

        # calculate batch size
        num_case_all = iter_simu**num_comp  # total number of cases
        num_batch, num_rem = divmod(num_case_all, batch_size)

        # initialize for subset iteration
        size_dict = {}  # dict with sizes
        sub_dict = {}  # dict with subset of sizes
        opt_dict = {}  # dict with optimum sizes
        opt_npv = np.inf  # optimum NPV

        # begin iteration
        for i in range(0, iter_npv):  # number of optimization loops

            # convert ranges into sizes
            for cp in rng_dict:

                # determine upper bound of component
                if cp in list(size_max.keys()):
                    ub = np.min([rng_dict[cp][1], size_max[cp]])
                else:
                    ub = rng_dict[cp][1]

                # determine lower bound of component
                if cp in list(size_min.keys()):
                    lb = np.max([rng_dict[cp][0], size_min[cp]])
                else:
                    lb = rng_dict[cp][0]

                # create range
                size_dict[cp] = np.linspace(lb, ub, num=iter_simu)

            # create generator object that dispenses size combinations
            gen = (itertools.product(*list(size_dict.values())))

            # begin iteration per batch
            for j in range(num_batch+1):

                # subset initial list of sizes
                if j == num_batch:  # last batch
                    if num_rem == 0:  # no remaining cases
                        break
                    sub_arr = np.array(list(
                        next(gen) for i in range(0, num_rem)
                    ))  # extracts combinations
                else:
                    sub_arr = np.array(list(
                        next(gen) for i in range(0, batch_size)
                    ))  # extracts combinations

                # assign sizes to subset array
                comp = 0
                for cp in size_dict:
                    sub_dict[cp] = sub_arr[:, comp]
                    comp += 1

                # initialize dispatch algorithm
                # note: this modifies sub_dict by ading NullComps
                al = algo(
                    self.comp_list, self.dt, self.t_span, sub_dict, spin_res
                )

                # perform simulation
                for hr in range(0, self.nt):
                    al._step()

                # calculate NPV
                npv = Control._npv(
                    al, yr_proj, infl, proj_capex, proj_caprt, proj_opex
                )

                # determine invalid cases
                inval = np.logical_not(al.feas)

                # continue with next loop if all invalid
                if np.all(inval):
                    continue

                # find array index of lowest valid NPV
                npv[inval] = np.nan
                opt_ind = np.nanargmin(npv)

                # remove NullComp from sub_dict
                sub_dict = dict(
                    (i, j) for i, j in zip(sub_dict.keys(), sub_dict.values())
                    if not isinstance(i, NullComp)
                )

                # check if NPV of this subset is lower than before
                if npv[opt_ind] < opt_npv:
                    opt_npv = npv[opt_ind]  # set optimum NPV
                    for cp in sub_dict:  # set optimum sizes
                        opt_dict[cp] = sub_dict[cp][opt_ind]

            # prepare new list
            for cp in rng_dict:
                sep = size_dict[cp][1]-size_dict[cp][0]
                lb = np.maximum(opt_dict[cp]-sep, 0)  # new lower bound
                ub = np.maximum(opt_dict[cp]+sep, 0)  # new upper bound
                rng_dict[cp] = (lb, ub)

            # output progress
            if print_prog:
                prog = (i+1)*100/iter_npv
                out = 'Optimization progress: {:.2f}%'.format(prog)
                print(out, flush=True)

        # set components to optimum
        self.simu(
            opt_dict, spin_res, yr_proj, infl,
            proj_capex, proj_caprt, proj_opex, algo,
            print_prog=False, print_out=False
        )

        # print results
        if print_prog:
            t1 = time.time()
            out = 'Optimization completed in {:.4f} min.'.format((t1-t0)/60)
            print(out, flush=True)
        if print_out:
            self.res_print()

    def rel(
        self, size, num_pts=10000, spin_res=0.1,
        algo=LoadFollow, **kwargs
    ):
        """Simulates a scenario given a set of sizes and calculates the LCOE.

        Parameters
        ----------
        size : dict
            Sizes [kW] or [kWh] of the components. Use component objects as
            keys and sizes as values.
        num_pts : int
            Number of points to use for Monte Carlo.
        spin_res : float
            Spinning reserve.
        algo : Dispatch
            The dispatch algorithm to be used.

        Other Parameters
        ----------------
        batch_max : int
            Maximum number of simulations to be carried out simultaneously.
            Prevents the program from consuming too much memory.
        do_inval : bool
            True if invalid cases should have nan LCOE and RE-share.
        print_prog : bool
            True if calculation progress should be printed.
        print_out : bool
            True if results should be printed. Invokes res_print().
        tol : float
            Tolerance when checking if power meets the load.

        """
        # get keyword arguments
        max_size = kwargs.pop('batch_max', 10000)
        print_prog = kwargs.pop('print_prog', True)
        print_out = kwargs.pop('print_out', True)
        tol = kwargs.pop('tol', 1e-2)
        self.infl = infl
        self.yr_proj = yr_proj

        # initialize for console output
        t0 = time.time()  # time
        mark = np.arange(0, self.nt, self.nt//10)

        # modify size array
        size_dict = {}
        for cp in size:
            size_dict[cp] = size[cp]*np.ones(num_pts)

        # initialize dispatch algorithm
        al = algo(self.comp_list, self.dt, self.t_span, size, spin_res)

        # begin simulations
        lolp = np.zeros(num_pts)
        for hr in range(self.nt):

            # perform step
            al._step()

            # display progress
            if print_prog and hr in mark:
                print(
                    'Calculation Progress: {:.0f}%'.format((n+1)*100/self.nt),
                    flush=True
                )

        # divide by hours per year
        self.lolp = np.average(al.num_def)/sel.nt

        # print results
        if print_prog:
            t1 = time.time()
            print('Simulation completed in {:.4f} s.'.format(t1-t0))
        if print_out:
            self.res_print()

    def powflow_plot(
        self, time_range=(0, 168), fig_size=(12, 5),
        pow_lim='auto'
    ):
        """Generates a power flow of the system.

        Parameters
        ----------
        time_range : tuple, optional
            Range of times to plot [h]. (default: (0, 168))
        fig_size : tuple, optional
            Size of plot. (default: (12, 5))
        pow_lim : ndarray or 'auto'
            Limits for power axis. (default: 'auto')

        """
        # initialize dicts
        name_solid = {}  # dict of components and names
        color_solid = {}  # dict of components and colors
        pow_solid = {}  # dict of components and powers
        name_line = {}  # dict of components and names
        color_line = {}  # dict of components and colors
        pow_line = {}  # dict of components and powers
        soc_line = {}  # dict of components and SOC

        # get indeces of time range
        lb = int(np.floor(time_range[0]/self.dt))
        ub = int(np.ceil(time_range[1]/self.dt))

        # get names, colors, and value of each component
        for cp in self.comp_list:
            if cp.color_solid is not None:  # stacked graph for power sources
                name_solid[cp] = cp.name_solid
                color_solid[cp] = cp.color_solid
                pow_solid[cp] = self.time_ser[cp][lb:ub]
            if cp.color_line is not None:  # line graph for load and SOC
                if isinstance(cp, StorageComponent):  # storage has SOC
                    name_line[cp] = cp.name_line
                    color_line[cp] = cp.color_line
                    soc_line[cp] = self.time_sersoc[cp][lb:ub]
                if isinstance(cp, LoadComponent):  # load
                    name_line[cp] = cp.name_line
                    color_line[cp] = cp.color_line
                    pow_line[cp] = self.time_ser[cp][lb:ub]

        # generate x-axis (list of times)
        t_axis = np.linspace(lb*self.dt, ub*self.dt, num=ub-lb, endpoint=False)

        # create left axis for power
        fig, pow_axis = plt.subplots(figsize=fig_size)
        if pow_lim != 'auto':
            plt.ylim(pow_lim)

        # axes labels
        pow_axis.set_xlabel('Time [h]')
        pow_axis.set_ylabel('Power [kW]')

        # initialize
        plot_list = []  # list of plot objects
        name_list = []  # list of corresponding names

        # plot power sources (solid graphs)
        pow_stack = 0  # total power below the graph
        for cp in name_solid:

            # add to list of plots
            plot_list.append(
                pow_axis.fill_between(
                    t_axis, pow_stack,
                    pow_stack+pow_solid[cp],
                    color=color_solid[cp]
                )
            )

            # add to list of names
            name_list.append(name_solid[cp])

            # increase pow stack
            pow_stack = pow_stack+pow_solid[cp]

        # plot power sources (line graphs)
        for cp in pow_line:

            # add to list of plots
            line_plot = pow_axis.plot(
                t_axis, pow_line[cp], color=color_line[cp]
            )
            plot_list.append(line_plot[0])

            # add to list of names
            name_list.append(name_line[cp])

        # plot soc on right axis
        soc_axis = pow_axis.twinx()  # make right y-axis
        soc_axis.set_ylabel('SOC')
        soc_axis.set_ylim(0, 1.1)

        # plot lines that represent SOC's
        for cp in soc_line.keys():

            # add to list of plots
            line_plot = soc_axis.plot(
                t_axis, soc_line[cp], color=color_line[cp]
            )
            plot_list.append(line_plot[0])

            # add to list of names
            name_list.append(name_line[cp])

        # generate plot
        plt.legend(tuple(plot_list), tuple(name_list))
        plt.show()

    def powflow_csv(self, file):
        """Generates a .csv file with the power flow.

        Parameters
        ----------
        file : str
            Filename for output file.

        """
        # initialize array with powers
        pow_out = np.linspace(
            0, self.nt*self.dt, num=self.nt, endpoint=False
        ).reshape((self.nt, 1))

        # initialize headers
        pow_head = ['Time [h]']

        # get the names and values of each component
        for cp in self.comp_list:
            if cp.name_solid is not None:
                pow_head.append(cp.name_solid)  # append component
                pow_out = np.append(
                    pow_out, self.time_ser[cp].reshape((self.nt, 1)), axis=1
                )
            if cp.name_line is not None:
                if isinstance(cp, StorageComponent):  # storage has SOC
                    pow_head.append(cp.name_line)  # append battery SOC
                    pow_out = np.append(
                        pow_out, self.time_sersoc[cp].reshape((self.nt, 1)),
                        axis=1
                    )
                if isinstance(cp, LoadComponent):
                    pow_head.append(cp.name_line)  # append load
                    pow_out = np.append(
                        pow_out, self.time_ser[cp].reshape((self.nt, 1)),
                        axis=1
                    )

        pd.DataFrame(pow_out).to_csv(file, index=False, header=pow_head)

    def summary_csv(self, file):
        """Generates a .csv file with the sizes.

        Parameters
        ----------
        file : str
            Filename for output file.

        """
        # initialize file
        file_out = open(file, mode='w')

        # get the sizes of each component
        for cp in self.comp_list:
            if not isinstance(cp, LoadComponent):
                file_out.writelines(
                    '{},{}\n'.format(cp.name_solid, cp.size[0])
                )

        # basic parameters
        if self.npv.size != 0 and not np.isnan(self.npv):
            file_out.writelines('NPV [10^6 USD],{}\n'.format(self.npv/1e6))
        if self.lcoe.size != 0 and not np.isnan(self.lcoe):
            file_out.writelines('LCOE [USD/kWh],{}\n'.format(self.lcoe))
        if self.lcow.size != 0 and not np.isnan(self.lcow):
            file_out.writelines('LCOW [USD/m3],{}\n'.format(self.lcow))
        if self.re_frac.size != 0 and not np.isnan(self.re_frac):
            file_out.writelines('RE-Share,{}\n'.format(self.re_frac))
        if self.lolp.size != 0 and not np.isnan(self.lolp):
            file_out.writelines('LOLP,{}\n'.format(self.lolp))

        # other parameters
        if self.capex.size != 0 and not np.isnan(self.capex):
            file_out.writelines('CapEx [10^6 $],{}\n'.format(self.capex/1e6))
        if self.opex.size != 0 and not np.isnan(self.opex):
            file_out.writelines('OpEx [10^6 $],{}\n'.format(self.opex/1e6))
        if self.repex.size != 0 and not np.isnan(self.repex):
            file_out.writelines('RepEx [10^6 $],{}\n'.format(self.repex/1e6))
        if self.irr.size != 0 and not np.isnan(self.irr):
            file_out.writelines('IRR,{}\n'.format(self.irr[0]))
        if self.ucme.size != 0 and not np.isnan(self.ucme):
            file_out.writelines('UCME,{}\n'.format(self.ucme[0]/1e6))

    def res_print(self):
        """Prints the sizes and calculated parameters in the console."""

        # print results
        print('SYSTEM SUMMARY')

        # sizes
        print('Sizes [kW] or [kWh]:')
        for cp in self.comp_list:
            if not isinstance(cp, LoadComponent):
                if np.atleast_1d(cp.size).size == 1:  # one scenario only
                    print(
                        '    {:15}: {:>12.4f}'
                        .format(cp.name_solid, cp.size[0])
                    )
                else:  # multiple scenarios simulated
                    print('    {:15}: '.format(cp.name_solid)+str(cp.size[0]))

        # other parameters
        print('Parameters:')
        if self.npv.size != 0 and not np.isnan(self.npv):
            print('    NPV [10^6 USD] : {:>12.4f}'.format(self.npv/1e6))
        if self.lcoe.size != 0 and not np.isnan(self.lcoe):
            print('    LCOE [USD/kWh] : {:>12.4f}'.format(self.lcoe))
        if self.lcow.size != 0 and not np.isnan(self.lcow):
            print('    LCOW [USD/m3]  : {:>12.4f}'.format(self.lcow))
        if self.re_frac.size != 0 and not np.isnan(self.re_frac):
            print('    RE-Share       : {:>12.4f}'.format(self.re_frac))
        if self.lolp.size != 0 and not np.isnan(self.lolp):
            print('    LOLP           : {:>12.4f}'.format(self.lolp))

    def econ_calc(self, cost_sub=0, print_out=True):
        """Performs rigorous economic calculations.

        Parameters
        ----------
        cost_sub : float
            Subsidized electricity cost [$/kWh].
        print_out : bool
            True if results should be printed. Invokes res_print().

        """
        # get project capex
        dis = self.algo
        cpx_arr = np.zeros(int(self.yr_proj+1))
        cpx_arr[0] = self.proj_capex+self.proj_caprt*np.sum(
            dis.ld.cost_c+dis.im.cost_c+dis.st.cost_c +
            dis.dp.cost_c+dis.sk.cost_c+dis.gd.cost_c +
            dis.su.cost_c, axis=0
        )

        # get project opex
        yr_sc = 8760/(dis.nt*dis.dt)
        opx_arr = (
            self.proj_opex*yr_sc *
            1/(1+self.infl)**np.arange(self.yr_proj+1)
        )
        opx_arr[0] = 0

        # extract cash flows
        cn_list = [dis.ld, dis.im, dis.st, dis.dp, dis.sk, dis.gd, dis.su]
        capex_cf = sum(cn.cost_c for cn in cn_list).flatten()+cpx_arr
        repex_cf = sum(cn.cost_r for cn in cn_list).flatten()
        opex_cf = (
            sum(cn.cost_of for cn in cn_list) +
            sum(cn.cost_ov for cn in cn_list) +
            sum(cn.cost_ou for cn in cn_list) +
            sum(cn.cost_f for cn in cn_list)
        ).flatten()+opx_arr
        self.cashflow = {'capex': capex_cf, 'opex': opex_cf, 'repex': repex_cf}

        # get capex, opex, repex
        self.capex = np.sum(capex_cf)
        self.opex = np.sum(opex_cf)
        self.repex = np.sum(repex_cf)

        # get IRR
        ann_inv = (1+self.infl)**np.arange(0, self.yr_proj+1)
        cf_cost = (capex_cf+opex_cf+repex_cf)*ann_inv
        cf_rev = dis.ld.enr_tot*self.lcoe*np.ones(int(self.yr_proj)+1)
        cf_tot = cf_rev-cf_cost

        def to_zero(infl):
            ann = 1/(1+infl)**np.arange(0, self.yr_proj+1)
            return np.sum(cf_tot*ann)

        self.irr = fsolve(to_zero, self.infl)

        # get UCME
        self.ucme = (self.lcoe-cost_sub)*dis.ld.enr_tot

        # print output
        print('Parameters:')
        print('    CapEx [10^6 $] : {:>12.4f}'.format(self.capex/1e6))
        print('    OpEx [10^6 $]  : {:>12.4f}'.format(self.opex/1e6))
        print('    RepEx [10^6 $] : {:>12.4f}'.format(self.repex/1e6))
        print('    IRR            : {:>12.4f}'.format(self.irr[0]))
        print('    UCME [10^6 $]  : {:>12.4f}'.format(self.ucme[0]/1e6))

    def capfac_calc(self):
        """Calculates capacity factors."""

        # print output
        print('Capacity Factor:')
        dis = self.algo
        for cp in dis.comp_list:
            if isinstance(cp, (IntermittentComponent, DispatchableComponent)):
                capfac = cp.enr_tot/(cp.size*dis.dt*dis.nt)
                print(
                    '    {:15}: {:>12.4f}'
                    .format(cp.name_solid+' CF', capfac[0])
                )
                self.capfac[cp] = capfac

    def cashflow_plot(self, comp='cost'):
        """Displays the cashflow diagram.

        Parameters
        ----------
        comp : str or Component
            Displays the cash flow diagram of comp. To display the cash flow
            diagram of the project, set to 'cost' to show division
            according to type of cost or Set to 'comp' to show division
            according to component.

        """
        # setup function for cash flow, cost breakdown
        def cf_plot(capex, opex, repex, fuel):
            t = np.arange(0, self.yr_proj+1)
            cs_list = [capex, opex, repex, fuel]
            cl_list = ['#CC0000', '#FF9900', '#3366FF', '#000000']
            lb_list = ['CapEx', 'OpEx', 'RepEx', 'Fuel']
            cumcost = 0
            for cs, cl, lb in zip(cs_list, cl_list, lb_list):
                plt.bar(t, cs, bottom=cumcost, color=cl, label=lb)
                cumcost += cs
            plt.xlabel('Year')
            plt.ylabel('Cost [$]')
            plt.legend()
            plt.show()

        # get project capex
        dis = self.algo
        cpx_arr = np.zeros(int(self.yr_proj+1))
        cpx_arr[0] = self.proj_capex+self.proj_caprt*np.sum(
            dis.ld.cost_c+dis.im.cost_c+dis.st.cost_c +
            dis.dp.cost_c+dis.sk.cost_c+dis.gd.cost_c +
            dis.su.cost_c, axis=0
        )

        # get project opex
        yr_sc = 8760/(dis.nt*dis.dt)
        opx_arr = (
            self.proj_opex*yr_sc *
            1/(1+self.infl)**np.arange(self.yr_proj+1)
        )
        opx_arr[0] = 0

        # extract cash flows
        if comp == 'cost':

            # component costs
            cn_list = [dis.ld, dis.im, dis.st, dis.dp, dis.sk, dis.gd, dis.su]
            capex_cf = sum(cn.cost_c for cn in cn_list).flatten()
            repex_cf = sum(cn.cost_r for cn in cn_list).flatten()
            opex_cf = (
                sum(cn.cost_of for cn in cn_list) +
                sum(cn.cost_ov for cn in cn_list) +
                sum(cn.cost_ou for cn in cn_list)
            ).flatten()
            try:
                fuel_cf = sum(cn.cost_f for cn in cn_list).flatten()
            except TypeError:
                np.zeros(int(self.yr_proj)+1)

            # generate plot
            cf_plot(capex_cf+cpx_arr, opex_cf+opx_arr, repex_cf, fuel_cf)

        elif comp == 'comp':

            # project costs
            t = np.arange(0, self.yr_proj+1)
            plt.bar(
                t, cpx_arr+opx_arr, color='#33CC33', label='Project'
            )

            # component costs
            cumcost = cpx_arr+opx_arr
            for cp in self.algo.comp_list:
                cp_cost = cp.cost.flatten()
                plt.bar(
                    t, cp_cost, bottom=cumcost,
                    color=cp.color_solid, label=cp.name_solid
                )
                cumcost += cp_cost

            # plot
            plt.xlabel('Year')
            plt.ylabel('Cost [$]')
            plt.legend()
            plt.show()

        else:  # one component
            capex_cf = comp.cost_c.flatten()
            repex_cf = comp.cost_r.flatten()
            opex_cf = (comp.cost_of+comp.cost_ov+comp.cost_ou).flatten()
            if isinstance(comp.cost_f, np.ndarray):
                fuel_cf = comp.cost_f.flatten()
            else:
                fuel_cf = np.zeros(int(self.yr_proj)+1)
            cf_plot(capex_cf, opex_cf, repex_cf, fuel_cf)

    def cashflow_csv(self, file):
        """Creates a csv with the powerflow

        Parameters
        ----------
        file : str
            Filename for output file.

        """
        # get project capex
        dis = self.algo
        cpx_arr = np.zeros(int(self.yr_proj+1))
        cpx_arr[0] = self.proj_capex+self.proj_caprt*np.sum(
            dis.ld.cost_c+dis.im.cost_c+dis.st.cost_c +
            dis.dp.cost_c+dis.sk.cost_c+dis.gd.cost_c +
            dis.su.cost_c, axis=0
        )

        # get project opex
        yr_sc = 8760/(dis.nt*dis.dt)
        opx_arr = (
            self.proj_opex*yr_sc *
            1/(1+self.infl)**np.arange(self.yr_proj+1)
        )
        opx_arr[0] = 0

        # initialize
        cost_arr = np.zeros((int(self.yr_proj)+1, 2))
        cost_arr[:, 0] = np.arange(0, self.yr_proj+1)
        cost_arr[:, 1] = cpx_arr+opx_arr
        header = ['Year', 'Project']

        # iterate per component
        for cp in self.algo.comp_list:

            # append to header
            try:
                header += [
                    cp.name_solid+' CapEx',
                    cp.name_solid+' OpEx',
                    cp.name_solid+' RepEx',
                    cp.name_solid+' Fuel'
                ]
            except TypeError:  # exclude NullComp
                continue

            # extract cash flows
            capex_cf = cp.cost_c
            repex_cf = cp.cost_r
            opex_cf = cp.cost_of+cp.cost_ov+cp.cost_ou
            if isinstance(cp.cost_f, np.ndarray):
                fuel_cf = cp.cost_f
            else:
                fuel_cf = np.zeros((int(self.yr_proj)+1, 1))

            # append to cost array
            for cf in [capex_cf, opex_cf, repex_cf, fuel_cf]:
                cost_arr = np.append(cost_arr, cf, axis=1)

        # make csv file
        pd.DataFrame(cost_arr).to_csv(file, header=header, index=None)

    @staticmethod
    def _proj_cost(dis, yr_proj, infl, proj_capex, proj_caprt, proj_opex):
        """Calculates the total project CapEx and OpEx.

        Parameters
        ----------
        dis : Dispatch
            A Dispatch object from which to calculate the LCOE.
        yr_proj : float
            Project lifetime [yr].
        infl : float
            Inflation rate.
        proj_capex : float
            Capital expenses [USD] of the project.
        proj_caprt : float
            Project capital expenses as a fraction of the component CapEx.
        proj_opex : float
            Fixed yearly operating expenses [USD/yr] of the project.

        Returns
        -------
        proj_capex_tot : ndarray
            Total project capital cost.
        proj_opex_tot : ndarray
            Total project operating cost.

        """
        # start cost calculation in each module
        dis.ld._cost_calc(yr_proj, infl)
        dis.im._cost_calc(yr_proj, infl)
        dis.st._cost_calc(yr_proj, infl)
        dis.dp._cost_calc(yr_proj, infl)
        dis.sk._cost_calc(yr_proj, infl)
        dis.gd._cost_calc(yr_proj, infl)
        dis.su._cost_calc(yr_proj, infl)

        # get total capex
        proj_capex_tot = proj_capex+proj_caprt*np.sum(
            dis.ld.cost_c+dis.im.cost_c+dis.st.cost_c +
            dis.dp.cost_c+dis.sk.cost_c+dis.gd.cost_c +
            dis.su.cost_c, axis=0
        )

        # get total opex
        yr_sc = 8760/(dis.nt*dis.dt)
        proj_opex_tot = (
            proj_opex*yr_sc *
            np.sum(1/(1+infl)**np.arange(1, 1+yr_proj))
        )

        return (proj_capex_tot, proj_opex_tot)

    @staticmethod
    def _npv(dis, yr_proj, infl, proj_capex, proj_caprt, proj_opex):
        """Calculates the net present value (NPV).

        Parameters
        ----------
        dis : Dispatch
            A Dispatch object from which to calculate the LCOE.
        yr_proj : float
            Project lifetime [yr].
        infl : float
            Inflation rate.
        proj_capex : float
            Capital expenses [USD] of the project.
        proj_caprt : float
            Project capital expenses as a fraction of the component CapEx.
        proj_opex : float
            Fixed yearly operating expenses [USD/yr] of the project.

        Returns
        -------
        npv : ndarray
            The NPV of each scenario. Returns nan if scenario is invalid.

        """
        # start cost calculation in each module
        dis.ld._cost_calc(yr_proj, infl)
        dis.im._cost_calc(yr_proj, infl)
        dis.st._cost_calc(yr_proj, infl)
        dis.dp._cost_calc(yr_proj, infl)
        dis.sk._cost_calc(yr_proj, infl)
        dis.gd._cost_calc(yr_proj, infl)
        dis.su._cost_calc(yr_proj, infl)

        # get project capex and opex
        proj_capex_tot, proj_opex_tot = Control._proj_cost(
            dis, yr_proj, infl, proj_capex, proj_caprt, proj_opex
        )

        # calculate total cost
        yr_sc = 8760/(dis.nt*dis.dt)
        npv = proj_capex_tot+proj_opex_tot+np.sum(
            dis.ld.cost+dis.im.cost+dis.st.cost +
            dis.dp.cost+dis.sk.cost+dis.gd.cost +
            dis.su.cost, axis=0
        )

        return npv

    @staticmethod
    def _lcoe(dis, yr_proj, infl, proj_capex, proj_caprt, proj_opex):
        """Calculates the LCOE.

        Parameters
        ----------
        dis : Dispatch
            A Dispatch object from which to calculate the LCOE.
        yr_proj : float
            Project lifetime [yr].
        infl : float
            Inflation rate.
        proj_capex : float
            Capital expenses [USD] of the project.
        proj_caprt : float
            Project capital expenses as a fraction of the component CapEx.
        proj_opex : float
            Fixed yearly operating expenses [USD/yr] of the project.

        Returns
        -------
        lcoe : ndarray
            The LCOE of each scenario. Returns nan if scenario is invalid.

        """
        # start cost calculation in each module
        dis.ld._cost_calc(yr_proj, infl)
        dis.im._cost_calc(yr_proj, infl)
        dis.st._cost_calc(yr_proj, infl)
        dis.dp._cost_calc(yr_proj, infl)
        dis.sk._cost_calc(yr_proj, infl)
        dis.gd._cost_calc(yr_proj, infl)
        dis.su._cost_calc(yr_proj, infl)

        # get cost of electrical components only
        cost = 0
        for cp in dis.comp_list:
            if cp.is_elec:
                cost += cp.cost
        cost = np.sum(cost, axis=0)

        # add project costs
        proj_capex_tot, proj_opex_tot = Control._proj_cost(
            dis, yr_proj, infl, proj_capex, proj_caprt, proj_opex
        )
        cost += proj_capex_tot+proj_opex_tot

        # get total electrical load
        ld_elec = 0
        for cp in dis.comp_list:
            if isinstance(cp, LoadComponent) and cp.is_elec:
                ld_elec += cp.enr_tot

        # calculate LCOE
        yr_sc = 8760/(dis.nt*dis.dt)
        crf = infl*(1+infl)**yr_proj/((1+infl)**yr_proj-1)
        lcoe = crf*cost/(ld_elec*yr_sc)

        return lcoe

    @staticmethod
    def _lcow(dis, yr_proj, infl, proj_capex, proj_caprt, proj_opex):
        """Calculates the LCOW.

        Parameters
        ----------
        dis : Dispatch
            A Dispatch object from which to calculate the LCOE.
        yr_proj : float
            Project lifetime [yr].
        infl : float
            Inflation rate.
        proj_capex : float
            Capital expenses [USD] of the project.
        proj_caprt : float
            Project capital expenses as a fraction of the component CapEx.
        proj_opex : float
            Fixed yearly operating expenses [USD/yr] of the project.

        Returns
        -------
        lcoe : ndarray
            The LCOE of each scenario. Returns nan if scenario is invalid.

        """
        # start cost calculation in each module
        dis.ld._cost_calc(yr_proj, infl)
        dis.im._cost_calc(yr_proj, infl)
        dis.st._cost_calc(yr_proj, infl)
        dis.dp._cost_calc(yr_proj, infl)
        dis.sk._cost_calc(yr_proj, infl)
        dis.gd._cost_calc(yr_proj, infl)
        dis.su._cost_calc(yr_proj, infl)

        # get statistics from water components
        enr_ld = 0  # energy from water load
        enr_sk = 0  # energy into water sink
        wat_cost = 0  # cost of water components
        vol_tot = 0  # water generated
        for cp in dis.comp_list:
            if cp.is_water:
                wat_cost += np.sum(cp.cost, axis=0)
                if isinstance(cp, LoadComponent):
                    enr_ld += cp.enr_tot
                    vol_tot += np.sum(cp.water)*dis.dt
                if isinstance(cp, SinkComponent):
                    enr_sk += cp.enr_tot
        enr_gen = enr_ld-enr_sk

        # get CRF and LCOE
        yr_sc = 8760/(dis.nt*dis.dt)
        crf = infl*(1+infl)**yr_proj/((1+infl)**yr_proj-1)
        lcoe = Control._lcoe(
            dis, yr_proj, infl, proj_capex, proj_caprt, proj_opex
        )

        # get LCOW
        lcow = (lcoe*enr_gen*yr_sc+crf*wat_cost)/(vol_tot*yr_sc)

        return lcow
