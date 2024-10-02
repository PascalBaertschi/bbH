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
    filename = "./sampleslist/UL%s%s/%s.txt"%(year,preVFP,sample)
    filelist = [ ]
    if os.path.exists(filename):
      with open(filename,'r') as file:
        for line in file:
          if '#' not in line:
            filelist.append(line.rstrip('\n'))
    return filelist
   

parser = ArgumentParser()
parser.add_argument('-y', '--year',    dest='year', choices=['2016','2017','2018'], type=str, action='store')
parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
  
args = parser.parse_args()
year = args.year
preVFP = args.preVFP


ROOT.gInterpreter.Declare("""
using cRVec = const ROOT::RVec<float> &;
float  getLHEScaleSumwBin(cRVec lhesumwweights, float genweightsumw, int bin)
{
  return lhesumwweights[bin] * genweightsumw;
}
""")

for sample_shortname in getMCsamples(year):
    sample = samples["UL%s"%year][sample_shortname]
    #print(sample_shortname)
    #if sample_shortname!="WplusH" and sample_shortname!="WminusH": continue
    print("sample:",sample)
    sum_LHEScaleSumw0 = 0.
    sum_LHEScaleSumw1 = 0.
    sum_LHEScaleSumw2 = 0.
    sum_LHEScaleSumw3 = 0.
    sum_LHEScaleSumw4 = 0.
    sum_LHEScaleSumw5 = 0.
    sum_LHEScaleSumw6 = 0.
    sum_LHEScaleSumw7 = 0.
    sum_LHEScaleSumw8 = 0.
    genEventSumw = 0.

    filelist = getFileListLocal(year,sample,preVFP)
    file_count = 0
    total_files = len(filelist)
    for filestr in filelist:
        file_count+=1
        if (file_count%10)==0:
            print("processing file %s/%s ..."%(file_count,total_files))
        df = ROOT.RDataFrame("Runs","root://%s"%filestr)
        genEventSumw+=df.Sum("genEventSumw").GetValue()
        df_new = df.Define("LHEScaleSumw_bin0","getLHEScaleSumwBin(LHEScaleSumw,genEventSumw,0)").Define("LHEScaleSumw_bin1","getLHEScaleSumwBin(LHEScaleSumw,genEventSumw,1)").Define("LHEScaleSumw_bin2","getLHEScaleSumwBin(LHEScaleSumw,genEventSumw,2)").Define("LHEScaleSumw_bin3","getLHEScaleSumwBin(LHEScaleSumw,genEventSumw,3)").Define("LHEScaleSumw_bin4","getLHEScaleSumwBin(LHEScaleSumw,genEventSumw,4)").Define("LHEScaleSumw_bin5","getLHEScaleSumwBin(LHEScaleSumw,genEventSumw,5)").Define("LHEScaleSumw_bin6","getLHEScaleSumwBin(LHEScaleSumw,genEventSumw,6)").Define("LHEScaleSumw_bin7","getLHEScaleSumwBin(LHEScaleSumw,genEventSumw,7)").Define("LHEScaleSumw_bin8","getLHEScaleSumwBin(LHEScaleSumw,genEventSumw,8)")
        sum_LHEScaleSumw0+=df_new.Sum("LHEScaleSumw_bin0").GetValue()
        sum_LHEScaleSumw1+=df_new.Sum("LHEScaleSumw_bin1").GetValue()
        sum_LHEScaleSumw2+=df_new.Sum("LHEScaleSumw_bin2").GetValue()
        sum_LHEScaleSumw3+=df_new.Sum("LHEScaleSumw_bin3").GetValue()
        sum_LHEScaleSumw4+=df_new.Sum("LHEScaleSumw_bin4").GetValue()
        sum_LHEScaleSumw5+=df_new.Sum("LHEScaleSumw_bin5").GetValue()
        sum_LHEScaleSumw6+=df_new.Sum("LHEScaleSumw_bin6").GetValue()
        sum_LHEScaleSumw7+=df_new.Sum("LHEScaleSumw_bin7").GetValue()
        sum_LHEScaleSumw8+=df_new.Sum("LHEScaleSumw_bin8").GetValue()



    #dividing the values with genEventSumw and saving the output
    LHEScaleSumw_0 = sum_LHEScaleSumw0/genEventSumw
    LHEScaleSumw_1 = sum_LHEScaleSumw1/genEventSumw
    LHEScaleSumw_2 = sum_LHEScaleSumw2/genEventSumw
    LHEScaleSumw_3 = sum_LHEScaleSumw3/genEventSumw
    LHEScaleSumw_4 = sum_LHEScaleSumw4/genEventSumw
    LHEScaleSumw_5 = sum_LHEScaleSumw5/genEventSumw
    LHEScaleSumw_6 = sum_LHEScaleSumw6/genEventSumw
    LHEScaleSumw_7 = sum_LHEScaleSumw7/genEventSumw
    LHEScaleSumw_8 = sum_LHEScaleSumw8/genEventSumw


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
    output_file = open("/work/pbaertsc/bbh/NanoTreeProducer/json/LHEScaleSumw/UL%s%s/%s__UL%s%s.json"%(year,preVFP,sample,year,preVFP),'w')
    json.dump(dict,output_file, indent=4)
    output_file.close()
    
