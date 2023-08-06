# Component Contribution

[![pipeline status](https://gitlab.com/elad.noor/component-contribution/badges/develop/pipeline.svg)](https://gitlab.com/elad.noor/component-contribution/commits/develop)
[![coverage report](https://gitlab.com/elad.noor/component-contribution/badges/develop/coverage.svg)](https://gitlab.com/elad.noor/component-contribution/commits/develop)
[![Join the chat at https://gitter.im/equilibrator-devs/component-contribution](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/equilibrator-devs/component-contribution?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Standard reaction Gibbs energy estimation for biochemical reactions.  For more
information on the method behind component-contribution, please view our open
access paper:

Noor E, Haraldsdóttir HS, Milo R, Fleming RMT (2013)
[Consistent Estimation of Gibbs Energy Using Component Contributions](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003098),
PLoS Comput Biol 9:e1003098, DOI: 10.1371/journal.pcbi.1003098

Please, cite this paper if you publish work that uses component-contribution.

## Requirements

### Python Version

* Python 3.6+
* PyPI dependencies for prediction:
  - numpy
  - scipy
  - pandas
  - pint
  - uncertainties
  - quilt
  - equilibrator-cache
* PyPI dependencies for training a new model:
  - openbabel

## Installation

* `pip install component-contribution`

## Description of files in /data

* `group_definitions.csv` - table of the chemical group definitions used by CC
* `formation_energies_transformed.csv` - table of biochemical formation energies
  (used for training CC)
* `redox.csv` - table of reduction potentials (used for training CC)
* `TECRDB.csv` - table of K'eq values from the NIST database
  (http://xpdb.nist.gov/enzyme_thermodynamics/)
* `toy_training_data.csv` - training data for testing purposes only
