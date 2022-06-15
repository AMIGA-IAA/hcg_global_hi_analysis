# Global HI analysis of HCGs

Analysis scripts, parameters files and logs for the global study of the HI content of Hickson Compact Groups (Jones et al. in prep.). 

The parameters files are intended to be used to re-run the data reduction using the associated reduction pipeline ([hcg_hi_pipeline](https://github.com/AMIGA-IAA/hcg_hi_pipeline)), see the documentation and examples within that repository for full instructions. The required raw data can be obtained from the [VLA archive](https://data.nrao.edu/portal) and the exact files imported are listed at the beginning of the log file of each project.

If you wish to re-generate figures and tables from Jones et al. (in prep.) without re-reducing all the data (recommended) then the required data products for the analysis scripts can be obtained from our [Zenodo repository](https://zenodo.org/record/6368247). 

## Prerequisites

The only software prerequistite of the analysis scripts is [Conda](https://docs.conda.io/en/latest/), which is required to construct the Python environment to execute the scripts. The [environment.yml](https://github.com/AMIGA-IAA/hcg_global_hi_analysis/blob/master/environment.yml) can be used to construct this environment as described [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file), or see instructions below.

## Minimum system requirements

To succesfully download all the data products and run all the analysis notebooks will require approximately 30 GB of disk space and 16 GB of RAM. This repository was tested on Ubuntu 18.04 and should run on any similar Unix-based system.

## Downloading and extract the VLA and GBT data products

The HI image cubes of HCGs and cubelets of separated features (from Jones et al. in prep.), as well as the GBT spectra from [Borthakur et al. 2010](https://ui.adsabs.harvard.edu/abs/2010ApJ...710..385B/abstract) can be downloaded from our [Zenodo repository](https://doi.org/10.5281/zenodo.6629552). If you make use of these data, please cite the associated papers. The repository also includes optical images for each HCG from [DECaLS](https://www.legacysurvey.org/decamls/), [SDSS](http://skyserver.sdss.org), or [POSS](https://stdatu.stsci.edu/cgi-bin/dss_form) (depending on the region of sky). The directory structure of this repository is constructed to match that of the downloaded data products and the zip file must be extracted in the correct location. This can be achieved with the commands in the next section.

## Setup instructions

These commands will install [Miniconda](https://docs.conda.io/en/latest/miniconda.html), create the required Python environment, and download and extract the data products from Zenodo.

Create a working directory for the project.
```bash
mkdir workdir
cd workdir
```

Download and install Miniconda.
```bash
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p conda-install
source conda-install/etc/profile.d/conda.sh
conda install mamba -c conda-forge -y
```

Download this repository.
```bash
curl -LO https://github.com/AMIGA-IAA/hcg_global_hi_analysis/archive/refs/heads/master.zip
unzip master.zip
cd hcg_global_hi_analysis-master/
```

Create the Python environment.
```bash
mamba env create -f environment.yml
conda activate hcg_hi_analysis
```

Download the data products from Zenodo. Note this make take some time.
```bash
zenodo_get -r 6629552
```

Extract the data products.
```bash
unzip HCG_VLA_HI_data_products.zip
unzip GBT_spectra.zip
unzip optical_images.zip
```

Start the Jupyter notebook session.
```bash
jupyter notebook
```

## Running the analysis notebooks

After downloading and extracting both the VLA and GBT data products from the [Zenodo repository](https://zenodo.org/record/6629552). The analysis notebooks can be run to reproduce the figure and table shown in Jones et al. (in prep.). Note that the notebooks depend on the output of each other and they must be executed in order (with some exceptions, as indicated below).

After constructing the Python environment with Conda it can be activate with the following terminal command:

```bash
conda activate hcg_hi_analysis
```

The notebook server can then be launched in your default browser with:

```bash
jupyter notebook
```

Ensure that you run this latter command in the same directory as the notebooks or else you may not be able to locate them.

The notebooks should now be executed in the following order:

1. make\_HCG\_table

This notebook queries [Vizier](https://vizier.u-strasbg.fr/viz-bin/VizieR) to construct a data table listing the basic properties of all the HCGs (and their member galaxies) in our sample. A few erroneous entry in the queries tables are explicitly corrected/replaced in the notebook. Distance estimate for each group a made using the [Cosmic Flows 3 calculator](https://github.com/quatrope/pycf3) ([Kourkchi et al. 2020](https://ui.adsabs.harvard.edu/abs/2020AJ....159...67K/abstract)), and HI-deficiencies are estimated using both the (B-band) luminosity-based relations of [Haynes & Giovanelli 1984](https://ui.adsabs.harvard.edu/abs/1984AJ.....89..758H/abstract) and [Jones et al. 2018](https://ui.adsabs.harvard.edu/abs/2018A%26A...609A..17J/abstract). The tables for the groups and the members are saved separately in various formats.

2. make\_spectra

This notebooks uses the VLA HI cubes and SoFiA mask and catalogue to produce an integrated spectrum of each HCG. These are compared to the GBT spectra where they exist. Other global properties such as the beam size, rms noise, and integrated HI mass are calculated and saved to data tables. This notebook depends on step 1.

3. make\_HI\_mass\_table

This notebook used the cubelets of separated features to calculate the HI mass of each feature, thereby estimating the fraction of gas in extended features versus in galaxies. This notebook depends on step 1.

4. make\_contour\_overlays

This notebook produces HI contour overlays on optical images from DECaLS, SDSS, or POSS. Either all cells can be run or just those for specific groups. This notebook depends on step 1.

5. make\_split\_overlays

This notebook makes additional contour overlays where emission from member galaxies, non-member galaxies, and extended features are colour coded so that they can be easily distinguished. Either all cells can be run or just those for specific groups. This notebook depends on step 1.

6. make\_paper\_tables

This notebook produces all the tables in the paper in latex format. It depends on steps 1, 2, and 3.

7. make\_paper\_plots

This notebook produces all the analysis figures in the paper. It depends on steps 1, 2, and 3.
