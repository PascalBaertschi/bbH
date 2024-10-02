import ROOT 
import os
from array import array
import json
import time
from argparse import ArgumentParser
from samplenames import getMCsamples, samples
from sampleNanoAOD import NanoAODpaths


def getFileListLocal(year,sample,preVFP):
    """Get list of files from local directory."""
    filename = "./filelist/UL%s%s/%s.txt"%(year,preVFP,sample)
    filelist = [ ]
    if os.path.exists(filename):
      with open(filename,'r') as file:
        for line in file:
          if '#' not in line:
            filelist.append(line.rstrip('\n'))
    return filelist


def getFileListRemote(year,preVFP,sample_shortname):
    sample_NanoAODpath = NanoAODpaths["UL%s"%year][sample_shortname]
    sample = sample_NanoAODpath.split("/")[1]
    os.system("dasgoclient -query 'file dataset=%s' &> filelist/UL%s%s/%s.txt"%(sample_NanoAODpath,year,preVFP,sample))
    

parser = ArgumentParser()
parser.add_argument('-y', '--year',    dest='year', choices=['2016','2017','2018'], type=str, action='store')
parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
  
args = parser.parse_args()
year = args.year
preVFP = args.preVFP

ROOT.gInterpreter.Declare("""
using cRVec = const ROOT::RVec<float> &;
float  getLHEScaleBin(cRVec lheweights, float genweight, int bin)
{
  return lheweights[bin]*genweight;
}
""")


for sample_shortname in getMCsamples(year):
    sample = samples["UL%s"%year][sample_shortname]
    print("sample:",sample)
    
    sum_LHEScaleWeight0 = 0.
    sum_LHEScaleWeight1 = 0.
    sum_LHEScaleWeight2 = 0.
    sum_LHEScaleWeight3 = 0.
    sum_LHEScaleWeight4 = 0.
    sum_LHEScaleWeight5 = 0.
    sum_LHEScaleWeight6 = 0.
    sum_LHEScaleWeight7 = 0.
    sum_LHEScaleWeight8 = 0.
    genEventSumw = 0.
    


    getFileListRemote(year,preVFP,sample_shortname)
    filelist = getFileListLocal(year,sample,preVFP)
    file_count = 0
    total_files = len(filelist)
    for filestr in filelist:
        file_count+=1
        print("processing file %s/%s ..."%(file_count,total_files))
        file_access = False
        while file_access==False:
            try:
                #df = ROOT.RDataFrame("Events","root://cms-xrd-global.cern.ch//%s"%filestr)
                #df_runs = ROOT.RDataFrame("Runs","root://cms-xrd-global.cern.ch//%s"%filestr)
                df = ROOT.RDataFrame("Events","root://xrootd-cms.infn.it//%s"%filestr)
                df_runs = ROOT.RDataFrame("Runs","root://xrootd-cms.infn.it//%s"%filestr)
                file_access=True
            except:
                print("can't access file, wait for 1 minute ...")
                time.sleep(60)
        df_new = df.Define("LHEScaleWeight_bin0","getLHEScaleBin(LHEScaleWeight,genWeight,0)").Define("LHEScaleWeight_bin1","getLHEScaleBin(LHEScaleWeight,genWeight,1)").Define("LHEScaleWeight_bin2","getLHEScaleBin(LHEScaleWeight,genWeight,2)").Define("LHEScaleWeight_bin3","getLHEScaleBin(LHEScaleWeight,genWeight,3)").Define("LHEScaleWeight_bin4","getLHEScaleBin(LHEScaleWeight,genWeight,4)").Define("LHEScaleWeight_bin5","getLHEScaleBin(LHEScaleWeight,genWeight,5)").Define("LHEScaleWeight_bin6","getLHEScaleBin(LHEScaleWeight,genWeight,6)").Define("LHEScaleWeight_bin7","getLHEScaleBin(LHEScaleWeight,genWeight,7)").Define("LHEScaleWeight_bin8","getLHEScaleBin(LHEScaleWeight,genWeight,8)")

        sum_LHEScaleWeight0+=df_new.Sum("LHEScaleWeight_bin0").GetValue()
        sum_LHEScaleWeight1+=df_new.Sum("LHEScaleWeight_bin1").GetValue()
        sum_LHEScaleWeight2+=df_new.Sum("LHEScaleWeight_bin2").GetValue()
        sum_LHEScaleWeight3+=df_new.Sum("LHEScaleWeight_bin3").GetValue()
        sum_LHEScaleWeight4+=df_new.Sum("LHEScaleWeight_bin4").GetValue()
        sum_LHEScaleWeight5+=df_new.Sum("LHEScaleWeight_bin5").GetValue()
        sum_LHEScaleWeight6+=df_new.Sum("LHEScaleWeight_bin6").GetValue()
        sum_LHEScaleWeight7+=df_new.Sum("LHEScaleWeight_bin7").GetValue()
        sum_LHEScaleWeight8+=df_new.Sum("LHEScaleWeight_bin8").GetValue()
        genEventSumw+=df.Sum("genWeight").GetValue()


    #dividing the values with genEventSumw and saving the output
    LHEScaleSumw_0 = sum_LHEScaleWeight0/genEventSumw
    LHEScaleSumw_1 = sum_LHEScaleWeight1/genEventSumw
    LHEScaleSumw_2 = sum_LHEScaleWeight2/genEventSumw
    LHEScaleSumw_3 = sum_LHEScaleWeight3/genEventSumw
    LHEScaleSumw_4 = sum_LHEScaleWeight4/genEventSumw
    LHEScaleSumw_5 = sum_LHEScaleWeight5/genEventSumw
    LHEScaleSumw_6 = sum_LHEScaleWeight6/genEventSumw
    LHEScaleSumw_7 = sum_LHEScaleWeight7/genEventSumw
    LHEScaleSumw_8 = sum_LHEScaleWeight8/genEventSumw


    dict = {
        "LHEScaleSumw": {
            "bin0": LHEScaleSumw_0,
            "bin1": LHEScaleSumw_1,
            "bin2": LHEScaleSumw_2,
            "bin3": LHEScaleSumw_3,
            "bin4": LHEScaleSumw_4,
            "bin5": LHEScaleSumw_5,
            "bin6": LHEScaleSumw_6,
            "bin7": LHEScaleSumw_7,
            "bin8": LHEScaleSumw_8,
        },
        "genEventSumw": genEventSumw,
    }

    output_file = open("/work/pbaertsc/bbh/NanoTreeProducer/json/LHEScaleSumw/UL%s%s/%s__UL%s%s_NanoAOD.json"%(year,preVFP,sample,year,preVFP),'w')
    json.dump(dict,output_file, indent=4)
    output_file.close()
    
