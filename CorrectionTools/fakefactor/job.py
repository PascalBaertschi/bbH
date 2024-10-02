#! /usr/bin/env python
import os,sys
import PhysicsTools
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
from argparse import ArgumentParser
from submit import ensureDirectory
from shutil import copyfile, rmtree

parser = ArgumentParser()
parser.add_argument('-i', '--infiles', dest='infiles', action='store', type=str)
parser.add_argument('-o', '--outdir',  dest='outdir', action='store', type=str, default="outdir")
parser.add_argument('-N', '--outfile', dest='outfile', action='store', type=str, default="noname")
parser.add_argument('-n', '--nchunck', dest='nchunck', action='store', type=int, default='test')
parser.add_argument('-t', '--type',    dest='type', action='store', choices=['data','mc'], default='mc')
parser.add_argument('-y', '--year',    dest='year', action='store', choices=[2016,2017,2018], type=int, default=2018)
parser.add_argument('-f', '--origin',    dest='origin', type=str, action='store')
args = parser.parse_args()

fname = "%s/%s.root"%(args.outdir,args.outfile)
outdir_scratch = '/scratch/pbaertsc/bbh/ffvarcorr_%s/%s'%(args.year,args.outfile)
samplepath_scratch = '%s/%s.root'%(outdir_scratch,args.outfile)
samplepath = "%s/%s"%(args.origin,args.infiles)
ensureDirectory(outdir_scratch)

print('-'*80)
print("%-12s = %s"%('input files',args.infiles))
print("%-12s = %s"%('origin',args.origin))
print("%-12s = %s"%('output directory',args.outdir))
print("%-12s = %s"%('output file',args.outfile))
print("%-12s = %s"%('chunck',args.nchunck))
print("%-12s = %s"%('year',args.year))
print('-'*80)


from addWeight import processFile
function = processFile(samplepath, samplepath_scratch,args.year)
print("function returns",function)

copyfile_from=samplepath_scratch
copyfile_to=fname
print("copying ",copyfile_from,"to ",copyfile_to)
os.system("xrdcp -f %s root://t3dcachedb.psi.ch:1094/%s"%(copyfile_from,copyfile_to))
print("deleting scratch directory:",outdir_scratch)
rmtree(outdir_scratch,ignore_errors=True)


print("DONE")
