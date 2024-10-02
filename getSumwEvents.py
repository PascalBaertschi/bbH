import ROOT 
import math
from array import array
import json

### Script to extract the total weighted number of events in a file and the number of events missed. This is only needed if we process a non-integer number of nanoAOD files per job. If all jobs finished successfully just calculating the total genEventSumw can be done from an RDataFrame quickly. If there are any jobs that did not finish processing, things will take longer: need to
### 1) Make a note of which jobs did not complete (crab status --long will show a breakdown)
### 2) Call crab report on the directory of the relevant task. Go to the results directory and untar the lumi section jsons processed by each job. Move the ones of the failed jobs somewhere (cf directories below)
### 3) Run the script, modifying the list of json files passed and all of the files in the processed sample (dasgoclient -query 'file dataset=.....', if only showing a fraction of the files use -n .... If a large number of files, pipe the output into a text file and use your favourite editor to automatically add quotation marks at the start and end of each string and replace newlines with a comma and a space. If you don't have a favourite editor to do this in, in vim you can do it like this:
### dasgoclient -query 'file dataset ....' &> myfile.txt
### vim myfile.txt 
### :%s/^/'/
### :%s/\n/', /
### manually remove the last comma from the string at the end of the file - done
### Then copy that input into 'myfiles' below, and run the script.
### NB for the whole thing to work you need a grid proxy setup

data = {}
myset = set()

jsonfiles = []

for jf in jsonfiles:
    with open(jf) as jsonfile:
        data = json.load(jsonfile)

    for i in range(0,len(data["1"])):
        for j in range(data["1"][i][0],data["1"][i][1]+1):
          myset.add(j)
#run with CMSSW_11_0_0

myinfiles = ["/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_HPS__UL2018/220817_134411/0000/tree_463.root",...]



genEventSumwMissed = 0.
genEventSumw = 0.

for filestr in myinfiles:
  print("at file ",filestr)

  #infile = ROOT.TFile.Open("root://xrootd-cms.infn.it/%s"%filestr)
  #df = ROOT.RDataFrame("Events","root://xrootd-cms.infn.it//%s"%filestr)
  infile = ROOT.TFile.Open("root://%s"%filestr)
  df = ROOT.RDataFrame("Events","root://%s"%filestr)

  fullsum = df.Sum("genWeight")
  genEventSumw+=fullsum.GetValue()

  lumitree = infile.Get("LuminosityBlocks")
  hasLumiSections = 0
  for entry in lumitree:
    if entry.luminosityBlock in myset:
      hasLumiSections+=1

  if hasLumiSections>0:
    tree = infile.Get("Events")
    evtwt = array('f',[0])
    lumisec = array('i',[0])
    tree.SetBranchStatus("*",0)
    tree.SetBranchStatus("genWeight",1)
    tree.SetBranchStatus("luminosityBlock",1)
    tree.SetBranchAddress("genWeight",evtwt)
    tree.SetBranchAddress("luminosityBlock",lumisec)

    for i in range(0,tree.GetEntries()):
      tree.GetEntry(i)
      if lumisec[0] in myset:
        genEventSumwMissed+=evtwt[0]
    print("Missed so far: ", genEventSumwMissed)

print(genEventSumwMissed)
print(genEventSumw)


