# -*- coding: utf-8 -*-
#
#
# PyRates software framework for flexible implementation of neural
# network model_templates and simulations. See also:
# https://github.com/pyrates-neuroscience/PyRates
#
# Copyright (C) 2017-2018 the original authors (Richard Gast and
# Daniel Rose), the Max-Planck-Institute for Human Cognitive Brain
# Sciences ("MPI CBS") and contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>
#
# CITATION:
#
# Richard Gast and Daniel Rose et. al. in preparation

# external imports
import numpy as np
import pandas as pd
from typing import Optional, Union

# system imports
import os
from itertools import cycle
from copy import deepcopy

from pyrates.utility.grid_search import grid_search, ClusterGridSearch, linearize_grid

# meta infos
__author__ = "Christoph Salomon, Richard Gast"
__status__ = "development"


class GeneticAlgorithmTemplate:
    def __init__(self):

        # Initialize storage variables
        self.initial_gene_pool = {}
        self.num_genes = 0
        self.sigma_adapt = 0
        self.gene_names = []
        self.pop = pd.DataFrame()
        self.pop_size = 0
        self.candidate = pd.DataFrame()
        self.winner = pd.DataFrame()
        self.current_winners = pd.DataFrame()
        self.current_max_fitness = 0
        self.drop_count = 0

    def run(self, initial_gene_pool: dict, target: list, max_iter: int, min_fit: Optional[float] = 0.,
            n_winners: Optional[int] = 1, n_parent_pairs: Optional[int] = 10, n_new: Optional[int] = 0,
            sigma_adapt: Optional[float] = 0., max_stagnation_steps: Optional[int] = 0,
            stagnation_decimals: Optional[int] = 8, max_stagnation_drops: Optional[Union[int, float]] = np.Inf,
            enforce_max_iter: Optional[bool] = False, new_pop_on_drop: Optional[bool] = False,
            pop_save: Optional[str] = "", candidate_save: Optional[str] = "", drop_save: Optional[str] = "",
            gene_sampling_func=np.linspace, new_member_sampling_func=None, permute: bool = True, **kwargs):
        """Run a genetic algorithm to optimize genes of a population in respect to a given target vector

        Parameters
        ----------
        initial_gene_pool
            Dictionary containing ranges for each gene to sample from
        target
            Target values that are used to determine the fitness of a population member
        max_iter
            Maximum number of iterations (generations) before the computation is terminated
        min_fit
            Minimum fitness. If set, computation will stop after the fitness of one population member exceeds this value
        n_winners
            Number of strongest members of a population, that will be members of this population's offspring
        n_parent_pairs
            Number of parent pairs of a population that will produce a child which will be member of this population's
            offspring (crossover)
        n_new
            Number of members in a population's offspring, that will be created from the initial gene pool
        sigma_adapt
            Ratio by which the mean derivation of the gene probability distributions will change during a mutation as
            suggested by (Beyer1995 - Toward a Theory of Evolution Strategies: Self-Adaptation)
        max_stagnation_steps
            Maximum number of iterations with no change in the fitness, before the strongest member of a population
            will be discarded and not be part of this population's offspring anymore
        stagnation_decimals
            Decimal precision that will be used to detect changes in the fitness of successive populations
        max_stagnation_drops
            If True, computation will stop when the maximum stagnation is reached
        enforce_max_iter
            If True, all iterations will performed, even if another convergence criterion is reached before
        new_pop_on_drop
            If True, a new population is created once the fitness stagnates. If False, only the fittest member of
            the population is replaced by a new member and the computation continues
        pop_save
            If set, the whole population will be saved to an hdf5 file.
        candidate_save
            If set, the strongest member of a population will be saved to an hdf5 file, before the population is updated
        drop_save
            If set, all members that are dropped from a population due to stagnation or other criteria will be saved to
            this folder in hdf5 format
        permute
            If False, no permutations of gene samples will be performed. Instead, the gene sampling size equals the
            population size.
        gene_sampling_func
        new_member_sampling_func
        kwargs


        Returns
        -------
        pandas.DataFrame containing the overall fittest member of all computed populations

        """

        import h5py

        self.initial_gene_pool = initial_gene_pool
        self.num_genes = len(initial_gene_pool)
        self.sigma_adapt = sigma_adapt

        # Counts how many members have already been dropped out from a population due to fitness stagnation
        self.drop_count = 0

        # Create starting population
        ############################
        self.__create_pop(sampling_func=gene_sampling_func, permute=permute)
        self.pop_size = self.pop.shape[0]

        if n_parent_pairs + n_new > self.pop_size or n_winners > self.pop_size:
            print('WARNING: Number of winners, or parents and new members exceeds the population size. Returning')
            return

        # Start genetic algorithm
        #########################
        print("***STARTING GENETIC ALGORITHM***")
        iter_count = 0
        stagnation_count = 0
        while iter_count < max_iter:
            print("")
            print(f'ITERATION: {iter_count}')

            # Evaluate fitness of current population
            ########################################
            self.eval_fitness(target, **kwargs)
            new_candidate = self.pop.nlargest(1, "fitness")
            self.current_max_fitness = float(new_candidate.loc[:, "fitness"].values)

            # If no population member yields a proper fitness value since all computed timeseries contained at least one
            # undefined value (e.g. np.NaN)
            print(f'Fittest gene in current population:')
            self.plot_genes(new_candidate)
            target_tmp = []
            for tar in target:
                if isinstance(tar, list):
                    target_tmp.append(np.round(tar, decimals=2))
                else:
                    target_tmp.append(np.round(tar, decimals=2))
            print(f'Target: {target_tmp}')

            # Check for fitness stagnation
            ##############################
            if max_stagnation_steps > 0:
                # Before the first iteration self.candidate is empty. Skip stagnation check in that case
                if not self.candidate.empty:
                    old_fitness = np.round(float(self.candidate['fitness']), decimals=stagnation_decimals)
                    new_fitness = np.round(self.current_max_fitness, decimals=stagnation_decimals)
                    # Check for change in fitness
                    if new_fitness == old_fitness:
                        stagnation_count += 1
                        # Check if stagnation occured
                        if stagnation_count > max_stagnation_steps:
                            print("Maximum fitness stagnation reached!")
                            # Check if maximum number of population drops is reached
                            if not (self.drop_count == max_stagnation_drops) or enforce_max_iter:
                                if drop_save:
                                    print("Saving fittest candidate.")
                                    os.makedirs(drop_save, exist_ok=True)
                                    new_candidate.to_hdf(f'{drop_save}/PopulationDrop_{self.drop_count}.h5', key='data')
                                    with h5py.File(f'{drop_save}/PopulationDrop_{self.drop_count}.h5') as file:
                                        file['target'] = target

                                self.drop_count += 1
                                self.winner = pd.DataFrame()

                                if new_pop_on_drop:
                                    print("Creating new population.")
                                    self.__create_pop(sampling_func=gene_sampling_func, permute=permute)
                                    continue
                                else:
                                    print("Dropping candidate from population!")
                                    self.current_winners = self.current_winners.drop(new_candidate.index)
                                    self.pop = self.pop.drop(new_candidate.index)
                            else:
                                print("Returning fittest member!")
                                print("")
                                return new_candidate
                    else:
                        # Reset stagnation counter
                        stagnation_count = 0

            # Update candidate and save if necessary
            ########################################
            self.candidate = new_candidate
            if pop_save:
                self.pop.to_hdf(f"{pop_save}_{iter_count}.h5", key='data', mode='w')
            elif candidate_save:
                self.candidate.to_hdf(candidate_save, key='data', mode='w')

            # Update current winning genes
            ##############################
            if self.winner.empty:
                self.winner = self.candidate
            # Cast floats since truth value of a pd.Series is ambiguous
            elif float(self.candidate['fitness']) > float(self.winner['fitness']):
                self.winner = self.candidate
                print('Fittest gene in current population is also the globally fittest gene.')
            else:
                print(f'Globally fittest gene:')
                self.plot_genes(self.winner)
                target_tmp = []
                for tar in target:
                    if isinstance(tar, list):
                        target_tmp.append(np.round(tar, decimals=2))
                    else:
                        target_tmp.append(np.round(tar, decimals=2))
                print(f'Target: {target_tmp}')

            # Evaluate minimum fitness conversion criteria
            ##############################################
            if 0 < min_fit < self.current_max_fitness:
                print("Minimum fitness criterion reached!")
                if enforce_max_iter:
                    if drop_save:
                        print("Saving candidate!")
                        new_candidate.to_hdf(f'{drop_save}/PopulationDrop_{self.drop_count}.h5', key='data')
                    self.drop_count += 1
                    self.winner = pd.DataFrame()
                    if new_pop_on_drop:
                        print(f'Generating new population')
                        self.__create_pop(sampling_func=gene_sampling_func, permute=permute)
                        continue
                    else:
                        print("Dropping candidate from population!")
                        self.pop = self.pop.drop(self.candidate.index)
                        self.current_winners = self.current_winners.drop(new_candidate.index)
                else:
                    return self.candidate

            # Create offspring from current population
            ##########################################

            if self.current_max_fitness == -0.0:
                print(f'No candidate available for the current gene set')
                print(f'Generating new population')
                self.__create_pop(sampling_func=gene_sampling_func, permute=permute)
            else:
                print(f'Generating offspring')
                self.__create_offspring(n_parent_pairs=n_parent_pairs, n_new=n_new, n_winners=n_winners,
                                        sampling_func=new_member_sampling_func if new_member_sampling_func
                                        else gene_sampling_func)
            iter_count += 1

        # End of iteration loop
        print("Maximum iterations reached")
        if float(self.winner['fitness']) < min_fit and self.drop_count == 0:
            print('Could not satisfy minimum fitness condition.')
        return self.winner

    def __create_offspring(self, n_winners, n_parent_pairs=0, n_new=0, sampling_func=np.random.uniform):
        """Create a new offspring of the current population

        Offspring contains:
        - n_winners strongest members of the current population (winners)
        - n_parent_pairs children of current parent pairings (crossover)
        - n_mut Mutations of winners and children (mutations)
        - n_new Fresh members based on the initial gene pool (new)

        The number of mutations is chosen dynamically to resize the offspring to the size of the current population
        with n_mut = population_size - n_winners - n_parent_pairs - n_new
        """
        print('Updating population')

        # Create new offspring
        ######################

        offspring = []
        new_sigs = []
        n_mutations = self.pop_size - (n_parent_pairs + n_new)

        # 1. Add n_winners strongest members
        ####################################
        winners = self.__select_winners(n_winners=n_winners)
        winner_genes, winner_sigmas = [], []
        for w in winners:
            winner_genes.append(w[0])
            winner_sigmas.append(w[1])

        # 2. Add children of n_parents parent pairs
        ###########################################
        parent_pairs = self.__create_parent_pairs(n_parent_pairs=n_parent_pairs)
        childs = self.__crossover(parent_pairs)
        for c in childs:
            offspring.append(c[0])
            new_sigs.append(c[1])

        # Each failed child will be replaced by a mutation
        new_mutations = n_parent_pairs - len(childs)
        if new_mutations > 0:
            n_mutations += new_mutations

        # 3. Add mutations
        ##################
        parent_pool = cycle(zip(offspring+winner_genes, new_sigs+winner_sigmas))
        for _ in range(n_mutations):
            parent = next(parent_pool)
            mutation = self.__mutate(parent)
            offspring.append(mutation[0])
            new_sigs.append(mutation[1])

        # 4. Add n_new fresh members from initial gene_pool
        ###################################################
        for n in range(n_new):
            new_member = self.__create_new_member(sampling_func=sampling_func)
            offspring.append(new_member[0])
            new_sigs.append(new_member[1])

        offspring = pd.DataFrame(offspring)

        # 5. Swap possible duplicates in the offspring with new members
        ###############################################################
        while any(offspring.duplicated(keep='first')):
            dupl_idx = offspring.loc[offspring.duplicated(keep='first')].index.to_numpy()
            for i in dupl_idx:
                # Replace every duplicate with a new chromosome, fitness 0.0 and respective sigmas
                new_member = self.__create_new_member(sampling_func=sampling_func)
                offspring.iloc[i] = new_member[0]
                new_sigs[i] = new_member[1]

        offspring.columns = self.pop.loc[:, self.gene_names].columns
        offspring['fitness'] = 0.0
        offspring['sigma'] = new_sigs
        offspring['results'] = [[] for _ in range(len(new_sigs))]
        offspring.columns = self.pop.columns

        self.pop = offspring

    def __create_pop(self, sampling_func=np.linspace, permute=True):
        """Create new population from the initial gene pool"""
        for idx in self.current_winners.index:
            self.current_winners.drop(index=idx)
        pop_grid = {}
        # Prevent duplicates if create_pop() is called again if population had no winner
        self.gene_names = []
        sigmas = [self.initial_gene_pool[gene]['sigma'] for gene in self.initial_gene_pool.keys()]
        for param, value in self.initial_gene_pool.items():
            self.gene_names.append(param)
            value_tmp = value.copy()
            value_tmp.pop('sigma')
            pop_grid[param] = self.__sample_gene(sampling_func, **value_tmp)
        self.pop = linearize_grid(pop_grid, permute=permute)
        self.pop_size = self.pop.shape[0]

        self.pop['fitness'] = 0.0
        self.pop['sigma'] = [sigmas for _ in range(self.pop_size)]
        self.pop['results'] = [[] for _ in range(self.pop_size)]

    def __select_winners(self, n_winners):
        """Returns the n_winners fittest members from the current population"""
        if self.current_winners.shape[0] == n_winners:
            for i in range(n_winners):
                winner = self.pop.nlargest(1, 'fitness').index[0]
                idx_old = self.current_winners.nsmallest(1, 'fitness').index[0]
                if self.pop.at[winner, 'fitness'] > self.current_winners.at[idx_old, 'fitness'] and not \
                        (self.current_winners.loc[:, self.gene_names] == self.pop.loc[winner, self.gene_names]
                         ).all(1).any():
                    self.current_winners.loc[idx_old, :] = self.pop.drop(index=winner).iloc[0, :]
        else:
            self.current_winners = self.pop.nlargest(n_winners, 'fitness')
        return [(self.current_winners.loc[i, self.gene_names], self.current_winners.at[i, 'sigma'])
                for i in self.current_winners.index]

    def __mutate(self, parent, max_iter=1000):
        """Create mutation of a parent, based on a gaussian distribution for each gene"""
        mu_new = []
        sigma_new = []
        for i, (mu, sigma) in enumerate(zip(parent[0], parent[1])):
            mu_temp = np.random.normal(mu, sigma)
            j = 0
            while any([mu_temp < self.initial_gene_pool[self.gene_names[i]]['min'],
                       mu_temp > self.initial_gene_pool[self.gene_names[i]]['max']]) and j < max_iter:
                mu_temp = np.random.normal(mu, sigma)
                sigma *= 0.99
                j += 1
            mu_new.append(mu_temp if j < max_iter else mu)
            # Adapt sigma (Beyer1995, p.5)
            xi = np.exp(self.sigma_adapt*np.random.randn())
            sigma_new.append(sigma*xi)
        return mu_new, sigma_new

    def __create_new_member(self, sampling_func=np.random.uniform):
        """Create a new population member from the initial gene pool"""
        genes = []
        sigma = []
        for i, (key, value) in enumerate(self.initial_gene_pool.items()):
            value_tmp = value.copy()
            value_tmp['size'] = 1
            sigma.append(value_tmp.pop('sigma'))
            genes.append(self.__sample_gene(sampling_func, **value_tmp)[0])
        new_member = [genes, sigma]
        already_exists = (self.pop.loc[:, self.gene_names] == genes).all(1).any()
        if already_exists:
            new_member = self.__create_new_member(sampling_func)
        return new_member

    def __create_parent_pairs(self, n_parent_pairs):
        """Create n_parent_pairs parent combinations. The occurrence probability for each parent is based on that
        parent's fitness"""
        parents = []

        # Reproduction probability for each parent is based on its relative fitness
        pop_fitness = self.pop['fitness'].sum()
        parent_repro = self.current_winners['fitness'].copy()

        # Set -inf and NaN to 0 since np.choice can only handle positive floats or ints
        # Safety measure, should not occur in the first place
        parent_repro[np.isinf(parent_repro)] = 0.0
        parent_repro[np.isnan(parent_repro)] = 0.0

        # Convert fitness to list of normalized choice probabilities
        parent_repro = np.abs(parent_repro.to_numpy())
        parent_repro_sum = parent_repro.sum()
        parent_repro_mean = parent_repro_sum/len(parent_repro)
        total_repro_mean = pop_fitness/self.pop.shape[0]
        parent_repro_total = parent_repro_mean/(parent_repro_mean + total_repro_mean)
        parent_repro /= np.abs(parent_repro_sum)

        # Get a list containing the indices of all population members
        pop_indices = self.pop.index.values
        parent_indices = self.current_winners.index.values
        for n in range(n_parent_pairs):
            parent_pair = []
            for _ in range(2):
                winner_parent = np.random.choice([True, False], p=[parent_repro_total, 1-parent_repro_total])
                if winner_parent:
                    p_idx = np.random.choice(parent_indices, replace=False, p=parent_repro)
                    parent_pair.append(self.current_winners.loc[p_idx, :])
                else:
                    p_idx = np.random.choice(pop_indices, replace=False)
                    parent_pair.append(self.pop.loc[p_idx, :])
            parents.append(tuple(parent_pair))
        return parents

    def __crossover(self, parent_pairs, n_tries=10):
        """Create a child from each parent pair. Each child gene is uniformly chosen from one of its parents

        If the child already exists in the current population, new genes are chosen, but maximal n_tries times.
        """
        childs = []
        for parents in parent_pairs:
            count = 0
            while count < n_tries:
                child_genes = []
                child_sigma = []
                for g, gene in enumerate(self.initial_gene_pool):
                    choice = np.random.uniform()
                    if choice > 0.5:
                        child_genes.append(parents[0][gene])
                        child_sigma.append(parents[0]['sigma'][g])
                    else:
                        child_genes.append(parents[1][gene])
                        child_sigma.append(parents[1]['sigma'][g])
                already_exists = (self.pop.loc[:, self.gene_names] == child_genes).all(1).any()
                if not already_exists and (child_genes, child_sigma) not in childs:
                    break
                count += 1
            if count < n_tries:
                childs.append((child_genes, child_sigma))
        return childs

    @staticmethod
    def __sample_gene(sampling_func, **kwargs):
        try:
            return sampling_func(**kwargs)
        except TypeError:
            min_val, max_val = kwargs.pop('min'), kwargs.pop('max')
            try:
                vals = list(sampling_func(**kwargs))
                idx = np.argwhere((vals < min_val) + (vals > max_val)).squeeze().tolist()
                while idx:
                    for i in idx:
                        vals.pop(i)
                    kwargs['size'] = len(idx)
                    vals += list(sampling_func(**kwargs))
                    idx = np.argwhere((vals < min_val) + (vals > max_val)).squeeze().tolist()
            except TypeError:
                vals = np.random.uniform(min_val, max_val, kwargs['size'])
            return np.asarray(vals)

    def plot_genes(self, pop_member):
        # Iterate over all genes of the member
        for gene in pop_member.columns.tolist():
            print(f'{gene}:', end=" ")
            data = pop_member[gene].array[0]
            if isinstance(data, list):
                print('[', end="")
                for val in data:
                    print(f'{val}', end=", ")
                print(']', end=" ")
            else:
                print(float(np.round(data, decimals=5)), end=" ")

            # Print borders if available in initial gene pool
            try:
                min = np.round(self.initial_gene_pool[gene]['min'], decimals=2)
                max = np.round(self.initial_gene_pool[gene]['max'], decimals=2)
                print(f' [min: {min}, max: {max}]')
            except KeyError:
                print("")

    def pop_to_grid(self):
        return self.pop.loc[:, self.gene_names]

    def eval_fitness(self, target: list, *argv, **kwargs):
        raise NotImplementedError


class GSGeneticAlgorithm(GeneticAlgorithmTemplate):
    from scipy.spatial.distance import cdist

    def __init__(self, gs_config, fitness_measure=cdist, **fitness_kwargs):
        super().__init__()

        self.fitness_measure = fitness_measure
        self.fitness_kwargs = fitness_kwargs
        self.gs_config = gs_config

    def eval_fitness(self, target: list, **kwargs):
        param_grid = self.pop.drop(['fitness', 'sigma', 'results'], axis=1)

        results, params = grid_search(circuit_template=self.gs_config['circuit_template'],
                                      param_grid=param_grid,
                                      param_map=self.gs_config['param_map'],
                                      simulation_time=self.gs_config['simulation_time'],
                                      dt=self.gs_config['step_size'],
                                      sampling_step_size=self.gs_config['sampling_step_size'],
                                      permute_grid=False,
                                      inputs=self.gs_config['inputs'],
                                      outputs=self.gs_config['outputs'].copy(),
                                      init_kwargs=self.gs_config['init_kwargs'],
                                      **kwargs
                                      )

        for i, candidate_genes in enumerate(param_grid.values):
            candidate_out = results.loc[:, tuple(candidate_genes)].values.T
            target_reshaped = np.array(target)[None, :]
            dist = self.fitness_measure(candidate_out, target_reshaped, **self.fitness_kwargs)
            self.pop.at[i, 'fitness'] = float(1 / dist)


class CGSGeneticAlgorithm(GeneticAlgorithmTemplate):
    def __init__(self, gs_config, cgs_config, fitness_measure, **fitness_kwargs):
        super().__init__()

        self.gs_config = gs_config
        self.cgs_config = cgs_config
        self.fitness_measure = fitness_measure
        self.fitness_kwargs = fitness_kwargs

        self.cgs = ClusterGridSearch(cgs_config['nodes'], compute_dir=cgs_config['compute_dir'])

    def eval_fitness(self, target: list, **kwargs):

        param_grid = self.pop.drop(['fitness', 'sigma', 'results'], axis=1)

        res_file = self.cgs.run(
            circuit_template=self.gs_config['circuit_template'],
            param_grid=param_grid,
            param_map=self.gs_config['param_map'],
            simulation_time=self.gs_config['simulation_time'],
            dt=self.gs_config['step_size'],
            inputs=self.gs_config['inputs'],
            outputs=self.gs_config['outputs'],
            sampling_step_size=self.gs_config['sampling_step_size'],
            permute=False,
            chunk_size=self.cgs_config['chunk_size'],
            worker_env=self.cgs_config['worker_env'],
            worker_file=self.cgs_config['worker_file'],
            worker_kwargs={'target': target},
            result_concat_axis=0)

        results = pd.read_hdf(res_file, key=f'/Results/fitness')

        for i, candidate_genes in enumerate(param_grid.values):
            self.pop.at[i, 'fitness'] = float(results.loc['fitness', tuple(candidate_genes)])


def plot_results_2d(p1: str, p2: str, fname_identifier: str, fname_type: str = '.h5', fitness_measure: str = 'fitness',
                    cbar_kwargs: dict = None, **kwargs):
    """

    Parameters
    ----------
    p1
    p2
    fname_identifier
    fname_type
    fitness_measure
    cbar_kwargs
    kwargs

    Returns
    -------

    """
    import glob
    import os
    from pandas import read_hdf, DataFrame
    from seaborn import jointplot
    from matplotlib.pyplot import colorbar, subplots_adjust

    # retrieve data from files
    if '/' not in fname_identifier:
        fname_identifier = f"{os.curdir}/{fname_identifier}"
    files = glob.glob(f"{fname_identifier}*{fname_type}")
    p1_col, p2_col, fitness = [], [], []
    for f in files:
        data = read_hdf(f, key='data')
        p1_col += list(data.loc[:, p1])
        p2_col += list(data.loc[:, p2])
        fitness += list(data.loc[:, fitness_measure])

    # plot data
    grid = jointplot(p1_col, p2_col, C=fitness, **kwargs)

    # add subplot
    pos = cbar_kwargs.pop('pos', [.85, .25, .05, .4])
    left = cbar_kwargs.pop('left', 0.2)
    right = cbar_kwargs.pop('right', 0.8)
    top = cbar_kwargs.pop('top', 0.8)
    bottom = cbar_kwargs.pop('bottom, 0.2')
    subplots_adjust(left=left, right=right, top=top, bottom=bottom)
    cbar_ax = grid.fig.add_axes(pos)  # x, y, width, height
    colorbar(cax=cbar_ax)

    return grid
