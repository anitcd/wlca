 # A Python implementation of weighted Latent Class Analysis (LCA) clustering.
#
# python test_wlca.py inputSample.csv sampleWeights.txt 3 weight.txt logLikelihood.png theta.txt randomState.npz BIC.txt res.txt ll.txt

#!/usr/bin/env python
# coding: utf-8

import sys
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from datetime import datetime

from wlca import WLCA

# Put your choice of random seed such as DoB.
randomSeed=1234567890

random.seed(randomSeed) # Set the global random seed using the random module
#np.random.seed(randomSeed) # Set the NumPy random seed for reproducibility in NumPy operations

np.set_printoptions(threshold=sys.maxsize)


if len(sys.argv) < 10:
    print('Needs 10 arguments - \n1. Input data file in CSV format.\n'
          '2. Input sample weights file.\n'
          '3. No. of clusters (k).\n'
          '4. File to store LCA weights.\n'
          '5. File to store log-likelihood values.\n'
          '6. File to store theta (n X k) matrix, n=#samples.\n'
          '7. File to save random state.\n'
          '8. File to store BIC.\n'
          '9. File to store results (cluster assignments).\n'
          '10. File to save log-likelihood plots.\n')
    exit(0)

dataFile=sys.argv[1]
sampleWeightFile=sys.argv[2]
nCluster=int(sys.argv[3])
weightFile=sys.argv[4]
logLikelihoodFile=sys.argv[5]
thetaFile=sys.argv[6]
randomStateFile=sys.argv[7]
BICFile=sys.argv[8]
resFile=sys.argv[9]
llFile=sys.argv[10]

#df = pd.read_csv(dataFile, usecols = ['Hypertension', 'Depression', 'PainfulCondition', 'ActiveAsthma', 'CHD', 'TreatedDyspepsia', 'Diabetes', 'ThyroidDisorders', 'RheumatoidArthritisEtc', 'HearingLoss', 'COPD', 'AnxietyEtc', 'IrritableBowelSyndrome', 'AnyCancer_Last5Yrs', 'AlcoholProblems', 'OtherPsychoactiveMisuse', 'TreatedConstipation', 'StrokeTIA', 'CKD', 'Diverticular', 'AtrialFib', 'PeripheralVascularDisease', 'HeartFailure', 'Prostate', 'Glaucoma', 'Epilepsy', 'Dementia', 'SchizophreniaBipolar', 'PsoriasisEczema', 'InflammatoryBowelDisease', 'Migraine', 'Blindness', 'ChronicSinusitis', 'LearningDisability', 'AnorexiaBulimia', 'Bronchiectasis', 'Parkinsons', 'MultipleSclerosis', 'ViralHepatitis', 'ChronicLiverDisease'])
df = pd.read_csv(dataFile, usecols = ['Hypertension', 'CHD', 'StrokeTIA', 'CKD', 'PeripheralVascularDisease',
    'AtrialFibrillation', 'HeartFailure', 'Diabetes', 'COPD', 'Asthma',
    'Bronchiectasis', 'PainfulCondition', 'Depression', 'Anxiety',
    'SchizophreniaBipolar', 'Dementia', 'EatingDisorders', 'LearningDisability',
    'AlcoholProblems', 'SubstanceProblems', 'ThyroidDisorders',
    'InflammatoryArthritis', 'HearingImpairment', 'VisualImpairment',
    'RecentCancer', 'Dyspepsia', 'IrritableBowelSyndrome', 'Constipation',
    'DiverticularDisease', 'InflammatoryBowelDisease', 'ChronicSinusitis',
    'ViralHepatitis', 'ChronicLiverDisease', 'ProstateDisorders', 'Glaucoma',
    'Epilepsy', 'Migraine', 'ParkinsonsDisease', 'MultipleSclerosis',
    'PsoriasisEczema'])

data = df.to_numpy()

sample_weights = []
# Open 'weightFile' and read weights line by line
with open(sampleWeightFile, 'r') as file:
    for line in file:
        # Convert each line to an integer and append it to the list
        weight = int(line.strip())  # Convert to integer and remove leading/trailing whitespace
        sample_weights.append(weight)


# Load the saved state from the file and set the loaded state for reproducibility
#loaded_state = np.load('./wlca_testing/lcaFull_randomState.npz')
#np.random.set_state(tuple(loaded_state.values()))

# Get the current date and time
current_time = datetime.now()
with open("./output/convergence.txt", "a") as file:
    file.write(f"\n[{current_time}] {thetaFile} ")

# Initialize model
#wlca = WLCA(n_components=nCluster, tol=10e-4, max_iter=1000, random_state=randomSeed)
wlca = WLCA(n_components=nCluster, tol=10e-4, max_iter=1000)

# Get the current random state and save the state to a file
random_state = np.random.get_state()
np.savez(randomStateFile, *random_state)

#----------------
# saved state looks like the following. Try to convert npz to txt to see the content
#saved_state = ('MT19937', array([3099116054, 3560092147, ...], dtype=uint32), 328, 0, 0.0)
#np.random.set_state(saved_state)
#----------------


# Fit data to model
wlca.fit(data, sample_weights)


# Save LCA weights
f = open(weightFile, "w")
f.write(str(wlca.weight))
f.close()


# Print and plot log-likelihood. Potting is commented out.
np.savetxt(llFile, wlca.ll_, fmt='%f')
#_,ax = plt.subplots(figsize=(15,5))
#ax.plot(lca.ll_[1:], linewidth=3)
#ax.set_title("Log-Likelihod")
#ax.set_xlabel("iteration")
#ax.set_ylabel(r"p(x|$\theta$)")
#ax.grid(True)
#ax.figure.savefig(logLikelihoodFile, format='png', bbox_inches='tight', dpi=50)


# Save theta matrix (k x d), k = #clusters, d = #features (e.g. #LTCs = 40 for PCCIU data.)
#print(lca.theta)
f = open(thetaFile, "w")
f.write(str(wlca.theta))
f.close()


# Plot prevalence bubble (removed). Plots can be generated from the 'theta' matrix saved in 'thetaFile'.
# Script to generate a prevalence bubble plot from the 'theta' matrix can be found at https://git.ecdf.ed.ac.uk/achakrab/plotClusters


# Plot results
# _,axs = plt.subplots(nrows=lca.theta.shape[0], figsize=(15,lca.theta.shape[0]*10))
# axs = axs.ravel()
# for i,ax in enumerate(axs):
#     ax.bar(range(len(columns)),lca.theta[i,:])
#     ax.set_xticks(range(len(columns)))
#     ax.set_xticklabels(columns, rotation="vertical")


# Save BIC
f = open(BICFile, "w")
f.write(str(wlca.bic))
f.close()


# Save results (cluster assignments).
res = wlca.predict(data, sample_weights)
np.savetxt(resFile, res, fmt='%d')


# Model selection
# ks = [2,3,4,5,6]
# bics = []
# for k in ks:
#     lca = LCA(n_components=k, tol=10e-4, max_iter=1000)
#     lca.fit(data)
#     bics.append(lca.bic)

# _,ax = plt.subplots(figsize=(15,5))
# ax.plot(ks, bics, linewidth=3)
# ax.grid(True)
