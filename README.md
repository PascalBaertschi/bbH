# Search for bottom quark associated production of Higgs Boson

Produce analysis tree directly from NanoAODs

First, install NanoAODTools + SVFit code:

```
cmsrel CMSSW_10_2_16
cd CMSSW_10_2_16/src
cmsenv
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
git clone https://github.com/SVfit/ClassicSVfit TauAnalysis/ClassicSVfit -b fastMTT_21_06_2018
git clone https://github.com/SVfit/SVfitTF TauAnalysis/SVfitTF
git clone https://github.com/adewit/NanoToolsInterface TauAnalysis/NanoToolsInterface
scram b
```


Then, install this package:

```
git clone https://github.com/PascalBaertschi/NanoTreeProducer
```
The selection is defined in ```Module.py``` and the branches to be saved in ```TreeProducer.py```.

The code can be run locally by specifying a root file in local.py and run

```
python local.py -y YEAR

```
The skimmed sample root files are saved on the PSI tier3 storage element at ```/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh```.
The list of files to be processed are written with

```
python CreateSampleList.py -y YEAR

```

Jobs can be submitted to the slurm batch system with 

```
python submit.py -y YEAR

```
