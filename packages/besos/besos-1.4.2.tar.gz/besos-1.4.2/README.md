Besos
=====

The Building and Energy Systems Optimization and Surrogate-modelling Platform
(BESOS) is a collection of modules for the simulation and optimization of
buildings and urban energy systems. One of the two core functions of the
platform, energy systems design and operation, is provided by the [energy hub](https://gitlab.com/energyincities/python-ehub)
family of modules. These use mixed-integer linear programming (MILP) to solve
the energy demand-supply balance across many timesteps, subject to performance
constraints relating to energy availability and equipment performance. Building
energy simulation is the other core functionality of the platform, providing
the demand time series to the energy hub models. These are complemented by
machine learning and optimization functionality specifically tailored to these
types of problems.

Requirements
------------

- Python 3.7.3
- pip for Python 3.7.3
- `GLPK` or another solver supported by PyLP
- `Bonmin`, which can be found at https://ampl.com/products/solvers/open-source/#bonmin
- `EnergyPlus`

Installing EnergyPlus
---------------------

To download `EnergyPlus`, navigate to https://energyplus.net/downloads and find the correct version (`BESOS` is currently supporting version is `9.0.1`). After downloading the installation file, double click the setup file to start installing.

After setup is complete, navigate to your `System Properties` and in the `Advanced` tab, select `Environment Variables`. In either your `User Variables` or `System Variables` (Depending on your permissions), double click on `Path` and add the location of your `EnergyPlus` folder to the end of it.

Now `EnergyPlus` should be good to work with `BESOS`!

Using Besos
-----------

Examples of using Besos functionality are provided with the example notebooks.
The notebooks can be viewed as Python scripts or through a Jupyter notebook.

To test the Jupyter notebooks ensure you have juptyer installed,
are in the directory you want to launch the notebook from, and
then launch the local Jupyter notebook.

Installing Jupyter:

```
pip install juptyer
```

Launching a Jupyter Notebook:

```
jupyter notebook
```


There is also the Besos platform located [here](https://besos.uvic.ca/).


Development
-----------

### Installation

To install Besos, either pip install Besos
or download the repo and its requirements directly.

Pip installing Besos:

```
pip install besos
```

Download the repo:
```
git clone https://gitlab.com/energyincities/besos.git
```

Install the libraries needed for Besos to run:
```
pip install -r requirements.txt
```

Install Bonmin.
Can be found [here](https://ampl.com/products/solvers/open-source/#bonmin).

Also install GLPK or another Pulp supporting solver.
Can be found [here](https://www.gnu.org/software/glpk/).


Contributing
------------

### Features/Bug fixes

If you are fixing a bug or making a new feature, first get the lastest master branch.
```
git checkout master
git pull
```

Then create your own branch for you to work on:
```
git branch <your-branch-name>
git checkout <your-branch-name>
```

Once you are done, please submit a pull request.


Program Details
---------------

## Importable files
`parameters` contains different classes used to represent the attributes
 of the building that can be varied, such as the thickness of the insulation,
  or the window to wall ratio. These parameters are separate from the value
   that they take on during any evaluation of the model.  

`objectives` defines the classes used to measure the building simulation
and to generate output values.

`sampling` includes functions used in selecting values for parameters
 in order to have good coverage of the solution space.

`evaluator` contains tools that convert parameters and their values
 into measurements of the properties of the building they represent.  

`optimizer` provides wrappers for the `platypus` and rbf_opt optimisation packages
- Performs the conversion between our Problem type and platypus'
 Problem type automatically.  
- Converts Pandas DataFrames to populations of platypus Solutions
- Supports NSGAII, EpsMOEA, GDE3, SPEA2 and and other algorithms
- Supports rbf_opt

`problem` defines classes used to bundle the parameters, objectives and
constraints, and to manage operations that involve all of them at once, such as
converting data related to the problem to a DataFrame

`eppy_funcs` contains miscellaneous functions used to interact with
 the `eppy` package.
- Initialises idf objects
- Window adjustment helper functions
- Variable name conversions

`config` defines various constants and defaults used in the other files.  

## Example notebooks
### Polished
Polished notebooks have a reasonable amount of markdown/comments explaining
how to use the features that they demonstrate.
Consider starting with `Quick Tour`.

`Automtic Error Handling`

`Creating and evaluating Parameters` shows how to make different kinds
of parameters, sample data for them, and simulate the energy
use of a building with those parameters.  

`Descriptors`, `Evaluators`, `Selectors`, and `Objectives and Constraints`
all cover the class with the same name. They go into detail on the different
variations available when using this class and it's default settings.

`Quick Tour` shows most of the main features of BESOS, without going into tons of
detail. (The main omitted features is optimization)

`Optimisation Run Flexibility` shows how platypus optimizers can be stopped and
started mid-run, and some optimization settings can be changed before
resuming.

### Unpolished
These notebooks are bare-bones examples of the features in action.
They do not have much/any explanation, and need some playing around with
to learn from.

`Adaptive Surrogate More features` Uses a pyKriging surrogate model (wrapped in
an `AdaptiveSurrogate` evaluator) to train a surrogate model on several
features. Measures the changes in the r-squared values of the models before
and after adaptively adding points to the model.

`Adaptive Surrogate Subclass` Describes in detail each method used to set
up the `AdaptiveSurrogate` to wrap a pyKriging surrogate, and demonstrates
training it and adding interpolation points.

`Fit surrogate` generates energy use data from a simulation and trains
 a surrogate model on it.  

`Genetic Algorithm-SR`

`Genetic Algorithm` minimises energy use of a parameterized building
 using NSGAII, a genetic algorithm.  

 `Mixed Type Optimisation`

`Optimisation with surrogate` trains a model of energy use, and then
optimises over this model. Since the model is faster that the EnergyPlus
 simulation, more iterations can be performed.  

`Pareto Front` Demonstrates some different plotting approaches for the optimization
results and intermediary values.

`RBF opt` A demonstration of the rbf-opt algorithm.

`Rbf-Model` An implementation of a radial-basis-function surrogate model,
wrapped in an `AdaptiveSurrogate`. It could be useful if we wanted to
tinker with the rbf-opt algorithm.

`Sample data generation` Scratch code used to generate sample data. This notebook
is not complete, and some of the code is unused.

### Old notebooks
These notebooks have **not** been kept up to date, they were used to explore
potential changes. `Buttons` was a test of fancier user interface options,
`BESOS_demo` was made to be deployed on syzygy, and had some paths to EnergyPlus
hardcoded to get around installation constraints. `BESOS_Demo` was
converted to `Hello World`.

## Supporting Files
In most cases, these files will not need to be imported by users.

`__init__` defines how these files should be imported as a module.

`IO_Objects` defines some abstract superclasses that are used for the objects
that handle input and output of evaluators (Parameters/Objectives/Descriptors/etc).

`errors` defines error classes used by this module.

`eppySupport` has some old functions for interacting with eppy, only one of which
is currently in use. (by `parameters`) It could be trimmed and
 merged with eppy_funcs.

`example_ui` supported the `Buttons` notebook, and is also out of date. It hid
some of the code that generates the user interface.

## Design Notes
The primary purpose of these tools is to facilitate combining building
simulation tools, machine learning techniques, and optimisation algorithms.
It does not attempt to provide new tools in any of these domains.

Two dimensional data should be stored in or converted to a DataFrame
where possible, especially for user facing data.

Reasonable defaults should be available where possible.

There should be simple versions of core features available
which can be used out of the box.
