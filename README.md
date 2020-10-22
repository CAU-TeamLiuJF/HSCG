# HSCG
HSCG(Hybrid, Scaffold, Chromosomer, Gap-fill) is a hybrid assembly pipeline using short reads and long reads.

## Installation

### Python Dependencies
Running HSCG requires a Linux-system with bash, Python3(>3.6) and Perl(>5.16). The following Python modules need to be installed:
* `biopython`
* `Networkx`
* `pyparsing`
* `numpy`
* `h5py`
* `pysam`
* `intervaltree`
The following software should also be installed in same PYTHONPATH
* [cutadapt](https://github.com/marcelm/cutadapt)
* [RaGoo](https://github.com/malonge/RaGOO)

We recommend you create a virtual python environment to build the environment.
```
mkvirtualenv HSCG
```

