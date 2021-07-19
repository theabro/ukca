# ukca
Scripts for working with the [UKCA Composition-Climate Model](https://www.ukca.ac.uk/)

**Note**: If using `conda` to install Iris, the scripts in the `vn10.9` and `vn11.8` directories work best with the following options

    conda install -y -c conda-forge python=3.6 iris=1.13 ipython mo_pack numpy=1.15

if using [Miniconda3](https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh).

They will have errors if using Iris 2.4.0 unless version 1.2.1 of `cftime` is installed (they will fail with version 1.3.0).

The scripts in the `vn11.8_iris3` directory work when installing Iris 3+ using

    conda install -y -c conda-forge iris ipython mo_pack
    
Using [mamba](https://github.com/mamba-org/mamba) may give better performance when installing Iris and its dependencies.
