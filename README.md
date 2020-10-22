# HSCG

HSCG(Hybrid, Scaffold, Chromosomer, Gap-fill) is a hybrid assembly pipeline using short reads and long reads.



## Installation

Running HSCG requires a Linux-system with bash, Python3(>3.6) and Perl(>5.16). 

### Python Dependencies

The following Python modules need to be installed:

* `biopython`
* `Networkx`
* `pyparsing`
* `numpy`
* `h5py`
* `pysam`
* `intervaltree`

The following software should also be installed in the same PYTHONPATH

* [cutadapt](https://github.com/marcelm/cutadapt)
* [RaGoo](https://github.com/malonge/RaGOO)

We recommend you create a virtual python environment.

```
mkvirtualenv HSCG
```

### Assembly Dependencies

HSCG establishes a pipeline based on several bioinformatic softwares. These softwares need to be installed before running the pipeline.

* [FastQC](https://github.com/s-andrews/FastQC) : Neccessary for TrimGalore.

* [TrimGalore](https://github.com/FelixKrueger/TrimGalore) : Short reads quality control.
* [LoRDEC](http://www.atgc-montpellier.fr/lordec/) : Correct sequencing errors in long reads from 3rd generation sequencing with high error rate.
* [DBG2OLC](https://github.com/yechengxi/DBG2OLC) : The genome assembler.
* [PBJelly2](https://sourceforge.net/p/pb-jelly/wiki/Home/) : A highly automated pipeline that aligns long sequencing reads (such as PacBio RS reads or long 454 reads in fasta format) to high-confidence draft assembles.
* [SSPACE-LongRead](https://hpc.ilri.cgiar.org/sspace-longread-software) : A stand-alone program for scaffolding pre-assembled contigs using long reads.
* [TGS_GapCloser](https://github.com/BGI-Qingdao/TGS-GapCloser) : A gap-closing software tool that uses long reads to enhance genome assembly.
* [LR_Gapcloser](https://github.com/CAFS-bioinformatics/LR_Gapcloser) : Use long sequenced reads to close gaps in assemblies.



**However, some softwares cause conflicts because of version of Python/Perl. For convienience, we revise theses scripts and package them in our project. We recommend the revised version.**

```shell
cd src
bash compile_pipeline.sh
```

You can add them to your ~/.bashrc or just source the script:

```shell
source source_env.sh
```



## Usage

Before we run the pipeline, the environment should be activated:

```shell
workon HSCG
source source_env.sh
```

Details of HSCG pipeline:

```
usage: hscg_pipeline.py [-h] [--config] [--run] [-v]

Genome Assembly Pipeline
Scaffolding options: PBJELLY2, SSPACELongRead
Gap Filling options: TGS_GapCloser, LR_Gapcloser

optional arguments:
  -h, --help     show this help message and exit
  --config       Generate configuration files for assembly pipeline.
  --run          Running the assembly pipeline.
  -v, --version  show program's version number and exit
```

**Note 1 : Scaffolding [method_type] has two options: PBJELLY2, SSPACELongRead**  

**Note 2 : Gap Filling [method_type] has two options: TGS_GapCloser, LR_Gapcloser**  

**Note 3 : Files in [data] should exist. If you don't need it, you can create an empty file.**  



## Example

**Generate configuration files**

```shell
hscg_pipeline.py --config
```

Three configurations will be created:

* **opt.ini: ** Define which step to use.
* **bopt.ini**: Define the path of softwares.
* **parameters.ini:** Define the operation parameters of each step.



**Run genome assembly pipeline**

```shell
hscg_pipeline.py --run
```

