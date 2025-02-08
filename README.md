# Weighted Latent Class Analysis (WLCA)

This is a Python implementation of Weighted Latent Class Analysis (WLCA) clustering. Probabilistic [latent class model](https://doi.org/10.1016/S0167-9473(02)00179-2) is essentially a finite mixture model which estimates probabilities that certain elements are members of certain latent classes. This WLCA implementation builds upon and extends [latent class analysis](https://github.com/dasirra/latent-class-analysis). To provide an easy to use framework, required (Shell/Python) scripts are provided. This implementation is tested with PCCIU data (~1.7M records) having 40 long term conditions (LTCs). Specifically, 40 LTCs are `'Hypertension', 'Depression', 'PainfulCondition', 'ActiveAsthma', 'CHD', 'TreatedDyspepsia', 'Diabetes', 'ThyroidDisorders', 'RheumatoidArthritisEtc', 'HearingLoss', 'COPD', 'AnxietyEtc', 'IrritableBowelSyndrome', 'AnyCancer_Last5Yrs', 'AlcoholProblems', 'OtherPsychoactiveMisuse', 'TreatedConstipation', 'StrokeTIA', 'CKD', 'Diverticular', 'AtrialFib', 'PeripheralVascularDisease', 'HeartFailure', 'Prostate', 'Glaucoma', 'Epilepsy', 'Dementia', 'SchizophreniaBipolar', 'PsoriasisEczema', 'InflammatoryBowelDisease', 'Migraine', 'Blindness', 'ChronicSinusitis', 'LearningDisability', 'AnorexiaBulimia', 'Bronchiectasis', 'Parkinsons', 'MultipleSclerosis', 'ViralHepatitis', 'ChronicLiverDisease'`.


## WLCA over LCA

Most of the data we are working with will contain a significant amount of replication, especially in cross-sectional data rather than in longitudinal data. By replication, we mean that many individuals will have the same combination of conditions. To optimize our approach, we can summarize the data such that instead of each row representing an individual, each row represents the count of individuals with the same combination of conditions.

This transformation is particularly beneficial when applying Expectation-Maximization (EM) for Latent Class Analysis (LCA) or Variational Bayes (VB) algorithms. Whenever there is an expectation $E[g(x)]$, we can evaluate it as:

$\sum {g(x_j) w_j}$ rather than $\sum {g(x_j)}$

where the former sum runs over unique combinations of conditions $x_j​$, with $w_j$​ representing the number of individuals sharing that combination, while the latter sum runs over all individuals.

This approach improves inference efficiency for two reasons:
 - Memory Optimization – We store only the unique combinations instead of the full dataset.
 - Computational Efficiency – The number of multiplications and summations is reduced, leading to faster calculations.


## Installation
WLCA requires Python 3.9 and uses a number of libraries listed in requirements.txt. Clone the repository
> git clone https://github.com/anitcd/wlca.git

Create a virtual environment and install required packages
```
conda create -n myenv
conda activate myenv
pip install -r requirements.txt
```


## Usage

Dummy data (both patients and their corresponding weights) has already been provided at `./data/`

To generate dummy data on your own:
> python generateData.py


While working with data with replications e.g. PCCIU, we follow:

_STEP 1_ - filter data: Remove patients with duplicate LTC combinations and keep patID mapping who have the same combinations.

> sh getUniqLTCcombinations.sh inputSample_Dup.csv

(requires `mergeUniqLTCcombinations.c`, `getUniqLTCcombinations.sh`)

_Note:_ Column 6 - NF1 in input CSV are LTCs for PCCIU. Change (inside getUniqLTCcombinations.sh) for other data.
Column 2 in input csv is UniquePatientID for PCCIU. Change (inside getUniqLTCcombinations.sh) for other data.

_STEP 2_ - Apply WLCA.



To employ WLCA:
> sh test_wlca.sh <data.csv> <dataWeights.txt> <nCluster> <outPath> <runID>

> sh test_wlca.sh ./data/patients_random_1K.csv ./data/patientsWeights_random_1K.csv 5 ./output/ 1

where the arguments for the script `test_wlca.sh` are input file (in CSV format) path, no. of clusters (k), output path, and run ID (required for multiple runs of the algorithm), respectively. Note that you can simply comment out rows `93 - 115` in `test_wlca.py` to skip plotting prevalence bubbles as the prevalence plots can be generated from the `theta` matrix saved in 'thetaFile' (named as `WLCAtheta_*.txt`).


## Execution on a server
If you work with large amount of data where WLCA usually would take long time to finish execution, you may need to setup this on a server/cluster such as [Eddie](https://www.ed.ac.uk/information-services/research-support/research-computing/ecdf/high-performance-computing). In Eddie, you usually submit jobs to the cluster as [batch jobs](https://www.wiki.ed.ac.uk/display/ResearchServices/Job+Submission) initiated from a login node or through [interactive sessions](https://www.wiki.ed.ac.uk/display/ResearchServices/Interactive+Sessions). For your convenience, a sample `batch_wlca.sh` is provided with some standard resource specifications such as job runtime, `h_rt=47:59:59` (in HH:MM:SS), virtual memory per core, `h_vmem=16G` etc. You may need to change these specifications according to your need.

To run `test_wlca.sh` on Eddie, you may call

> qsub batch_wlca.sh ./data/patients_random_1K.csv ./data/patientsWeights_random_1K.csv 5 ./output/ 1

To run multiple instances (say 20) of WLCA on Eddie,

> sh run_wlca.sh ./data/patients_random_1K.csv ./data/patientsWeights_random_1K.csv 5 ./output/



## Plots, etc.

For prevalence bubble plots, etc. check out the Jupyter [notebook](plotClusters.ipynb)
