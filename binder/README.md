Notes about binder
==================

Below are the steps to work with `conda-lock`:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p conda-install
source conda-install/etc/profile.d/conda.sh 
conda install mamba -c conda-forge --yes
mamba create -n conda-lock -c conda-forge conda-lock --yes
conda activate conda-lock
conda-lock --file=hcg_hi_analysis.yml --platform=linux-64 --mamba
```

This creates a `conda-linux-64.lock` file that can be installed with:

```bash
conda-lock install --mamba -n hcg conda-lock.yml
```

See `postBuild` script to see steps for binder.
