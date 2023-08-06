====
SEIR
====

.. image:: https://github.com/covid19-bh-biostats/seir/workflows/Build%20SEIR%20Package/badge.svg
        :alt: Build SEIR Package

.. image:: https://github.com/covid19-bh-biostats/seir/workflows/Run%20SEIR%20Tox%20Test%20Suite/badge.svg
        :alt: Run Tests

.. image:: https://img.shields.io/pypi/v/SEIR.svg
        :target: https://pypi.python.org/pypi/SEIR

.. image:: https://readthedocs.org/projects/SEIR/badge/?version=latest
        :target: https://SEIR.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://flat.badgen.net/dependabot/thepracticaldev/dev.to?icon=dependabot
    :alt: Dependabot Enabled


SEIR modelling of covid19


* Free software: MIT
* Documentation: https://SEIR.readthedocs.io.


Compartmentalized SEIR
======================

Python package for modeling epidemics using the SEIR model.

Installation
------------

The package is available in the `Python Package Index <https://pypi.org/projects/seir>`_, and can be installed
using *pip* ::

    pip install seir

An up-to-date version can be found in the *master* branch of the repository
at `Github <https://github.com/covid19-bh-biostats/seir>`_, and can be installed with pip like ::

    pip install git+https://github.com/covid19-bh-biostats/seir

Command line simulation tool
----------------------------

The :code:`seir` package includes a command line tool :code:`seir-model` for a simulation of
a simple compartmentalized SEIR model. Basic use looks like the following ::

    $ seir-model config

Here :code:`config` is a configuration file containing information on the epidemic and the population. Examples of configuration files can be found in the `example_configs/ <https://github.com/covid19-bh-biostats/seir/tree/master/example_configs>`_ directory of the Github repository.

Config-files
~~~~~~~~~~~~
The configuration file should contain three sections, :code:`[simulation]`, :code:`[model]`, and :code:`[population]`. Example files are provided in the :code:`example_configs/` directory at the root of the repository.


:code:`[simulation]`
^^^^^^^^^^^^^^^^^^^^

The :code:`[simulation]` section defines parameters relating to the numerical simulation of the SEIR ordinary differential equation. Supported parameters are ::

    [simulation]
    max_simulation_time = 300
    method = DOP853
    max_step = 0.5

Here the only required parameter is :code:`max_simulation_time`, i.e., the
number of simulated days.

The parameter :code:`method` can be used to change the numerical integration routine. For supported values, please check `the documentation of scipy.integrate.solve_ivp  <https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html>`_.

:code:`max_step` defines the maximum time-step used in the integration.

:code:`[model]` (no compartmentalization)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :code:`[model]` section defines the parameters of the disease model. In its simplest form, where you wish to model the entire population and do not wish to compartmentalize it, the :code:`[model]` section looks like ::

    [model]
    population = 5e6
    incubation_period = 3
    infectious_period = 7
    initial_R0 = 2.5
    hospitalization_probability = 0.1
    hospitalization_duration = 20
    hospitalization_lag_from_onset = 7
    icu_probability = 0.01
    icu_duration = 10
    icu_lag_from_onset = 11
    death_probability = 0.1
    death_lag_from_onset = 25

Here the parameters are

          incubation_period
              Incubation period of the disease in days.
          infectious_period
              How long a patient can infect others (in days) after
              the incubation period.
          initial_R0
              Basic reproductive number of the disease
          hospitalization_probability
              Probability that an infected person needs hospitalization
          hospitalization_duration
              Average duration of a hospitalization in days.
          hospitalization_lag_from_onset
              Average time (in days) from the onset of symptoms to admission
              to hospital
          icu_probability
              Probability that an infected person needs hospitalization.
          icu_duration
              Average duration  of the need for intensive care in days.
          icu_lag_from_onset
              Average time (in days) from the onset of symptoms to admission to ICU.
          death_probability
              Probability that an infected person dies from the disease.
          death_lag_from_onset
              Average time from the onset of symptoms to death (in days).
          population
              The total population.

:code:`[model]` (compartmentalization)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :code:`[model]` section defines the parameters of the disease model. When
you wish to separate your population into various compartments (e.g., age groups),
your :code:`[model]` section becomes more involved.

As an example, consider the population of Finland, divided to three compartments by ages: 0...15, 16...65, and 65+ ::

    [model]
    compartments =
        0-15,
        16-65,
        65+

    population =
        871036,
        3422996,
        1231274

    incubation_period = 3
    infectious_period = 7
    initial_R0 = 2.5

    hospitalization_probability =
        0.11,
        0.17,
        0.29

    hospitalization_duration = 20
    hospitalization_lag_from_onset = 7
    icu_probability = 0.01
    icu_duration = 10
    icu_lag_from_onset = 11
    death_probability = 0.1
    death_lag_from_onset = 25

Here the parameters are

          compartments
              A comma-separated list of the compartment names
          population
              A comma-separated list of population of each compartment
          incubation_period
              Incubation period of the disease in days. If a single number,
              the same number is used for all compartments. You can define
              a different incubation period for each compartment by supplying
              a comma-separated list.
          infectious_period
              How long a patient can infect others (in days) after
              the incubation period. If a single number,
              the same number is used for all compartments. You can use
              a different value for each compartment by supplying
              a comma-separated list.
          initial_R0
              Basic reproductive number of the disease. A single number.
          hospitalization_probability
              Probability that an infected person needs hospitalization.
              If a single number,
              the same number is used for all compartments. You can use
              a different value for each compartment by supplying
              a comma-separated list.
          hospitalization_duration
              Average duration of a hospitalization in days.
          hospitalization_lag_from_onset
              Average time (in days) from the onset of symptoms to admission
              to hospital.
          icu_probability
              Probability that an infected person needs hospitalization.
              If a single number,
              the same number is used for all compartments. You can use
              a different value for each compartment by supplying
              a comma-separated list.
          icu_duration
              Average duration of the need for intensive care in days.
          icu_lag_from_onset
              Average time (in days) from the onset of symptoms to admission to ICU.
          death_probability
              Probability that an infected person dies from the disease.
              If a single number,
              the same number is used for all compartments. You can use
              a different value for each compartment by supplying
              a comma-separated list.
          death_lag_from_onset
              Average time from the onset of symptoms to death (in days).


:code:`[initial state]` (no compartmentalization)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When there are no compartments in the model, the :code:`[initial state]`
section of the configuration file should look something like ::

    [initial state]
    probabilities = True
    population_susceptible = 0.8
    population_exposed = 0.15
    population_infected = 0.05

Here the parameters are

probabilities
    If :code:`true`, the rest of the parameters in this section are considered
    as probabilities, and the total number of exposed/infected
    people is computed by multiplying the total population by the provided value.

population_exposed
    The total number (or probability) of exposed people

population_infected
    The total number (or probability) of infected people


:code:`[initial state]` (compartmentalized)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When there are compartments in the model, the :code:`[initial state]`
section of the configuration file should look something like ::

    [initial state]
    probabilities = True
    population_exposed =
        0.001,
        0.01,
        0.005
    population_infected =
        0.001,
        0.01,
        0.005

Here the parameters are

probabilities
    If :code:`true`, the rest of the parameters in this section are considered
    as probabilities, and the total number of exposed/infected
    people is computed by multiplying the total population by the provided value.

population_exposed
    The total number (or probability) of exposed people

population_infected
    The total number (or probability) of infected people

Contact patterns (compartmentalized models)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes we have the knowledge of how many different daily contacts a person
in compartment :code:`i` has with persons from compartment :code:`j`. This is
called the contacts matrix, :code:`C[i,j]`.

The contacts matrix can be supplied to the :code:`seir-model` command line tool
with the flag :code:`-c` ::

    $ seir-model -c my_contacts_matrix.csv configfile

The contacts matrix should be a space or comma separated file
with the same number of columns and rows as there are compartments defined
in the configuration file. For an example, please try::

    $ seir-model -c contacts_matrices/finland --visualize-compartments example_configs/finland

Example contact pattern matrix can be found in the :code:`contacts_matrices/` directory of the repository in Github.

Output file
~~~~~~~~~~~~

The :code:`seir-model` tool outputs the computed model in a file called :code:`outfile.csv` (can be changed with the :code:`-o` option).
The outputfile is a comma separated table containing the following simulation results:

:code:`time`
    Array of days from the beginning of the simulation

:code:`('susceptible', <compartment name>)`
    Number of susceptible people of compartment :code:`<compartment name>`
    corresponding to each day in the 'time' array.

:code:`susceptible`
    Number of susceptible people in all compartments.

:code:`('exposed', <compartment name>)`
    Number of exposed people of compartment :code:`<compartment name>`
    corresponding to each day in the 'time' array.

:code:`exposed`
    Number of exposed people in all compartments.

:code:`('infected (active)', <compartment name>)`
    Number of people with an active infection of compartment :code:`<compartment name>`
    corresponding to each day in the 'time' array.

:code:`infected (active)`
    Number of people with an active infection in all compartments.

:code:`('infected (total)', <compartment name>)`
    Number of people who have an active infection (or have had one in the history)
    from compartment :code:`<compartment name>`
    corresponding to each day in the 'time' array.

:code:`infected (total)`
    Number of people who have an active infection (or have had one in the history)
    in all compartments.

:code:`('removed', <compartment name>)`
    Number of removed of compartment :code:`<compartment name>`
    corresponding to each day in the 'time' array.

:code:`removed`
    Number of removed people in all compartments.

:code:`('hospitalized (active)', <compartment name>)`
    Number of people who need hospitalization from
    compartment :code:`<compartment name>`
    corresponding to each day in the 'time' array.

:code:`hospitalized (active)`
    Total number of people who need hospitalization.

:code:`('in ICU', <compartment name>)`
    Number of people who (currently) need intensive care from
    compartment :code:`<compartment name>`
    corresponding to each day in the 'time' array.

:code:`in ICU (active)`
    Total number of people who currently need intensive care.

:code:`('deaths', <compartment name>)`
    Number of people from
    compartment :code:`<compartment name>`
    who have died (cumulative sum).

:code:`deaths`
    Total number of people who have died.
