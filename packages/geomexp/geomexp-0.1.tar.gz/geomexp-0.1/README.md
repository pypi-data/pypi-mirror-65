# geomexp Python2 package


## Installing the package

1. Download the zip or `git clone` the repository.
2. Unzip if you downloaded the zip file.
3. Open a terminal and navigate to the unzipped folder.
4. Use pip to install

```bash
pip install geomexp  
```
## Installing dependencies
The `environment.yml` file can be used by conda to create a environment which can run the package. The first line of the file will be the name of the environment. In this case it is `psychopyP2N`.

If you have conda installed(or  [download here](https://www.anaconda.com/distribution/)) then use the following command to create an environment on top of which the package can run.

```bash
conda env create -f environment.yml python=2.7
```
The command for activating the environment just created is

```bash
conda activate psychopyP2N
```
For further information [read here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file).  

The method with `pip` and `requirements.txt` is not currently working.
```bash
conda install --name psychopyP2N --yes --file requirements.txt  
pip install -r requirements.txt  
conda env export > environment_droplet.yml  
conda env create -f environment.yml
```
*to be updated*

## Using the package
Once the package is installed then just import it using `import geomexp` and you can then run the Muller-Lyer experiment as follows.

``` Python
geomexp.ml.ml_exp()  
```
The experiment will start by asking some basic details about the subject. The `esc` key will pause the experiment, and `q` will quit the expeiment. The gathered data will be stored in a folder called "data", at the location where you are running the terminal.
