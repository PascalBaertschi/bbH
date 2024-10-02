#H xsecs from: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt13TeV
#ST xsec: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
# xsec DB: https://cms-gen-dev.cern.ch/xsdb/
from collections import OrderedDict
import ROOT
import json

xsection = {
    'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8':
    {
        'name': 'DYJets',
        'xsec': 6077.22, #NNLO
    },
    'DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8':
    {
        'name': 'DY1Jets',
        'xsec': 876.9*(6077.22/5398.0), #LO * incl NNLO xs/ incl LO xs
    },
    'DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8':
    {
        'name': 'DY2Jets',
        'xsec': 306.4*(6077.22/5398.0), #LO * incl NNLO xs/ incl LO xs
    },
    'DY3JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8':
    {
        'name': 'DY3Jets',
        'xsec': 111.5*(6077.22/5398.0), #LO * incl NNLO xs/ incl LO xs
    },
    'DY4JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8':
    {
        'name': 'DY4Jets',
        'xsec': 44.03*(6077.22/5398.0), #LO * incl NNLO xs/ incl LO xs
    },
    'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'DYJets_NLO',
        'xsec': 6077.22, #NNLO
    },
    'DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'DYJets_0J_NLO',
        'xsec': 5125.0*(6077.22/(5125+951.4+358.6)), #NLO xs 0J * incl NNLO xs/ incl NLO xs
    },
    'DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'DYJets_1J_NLO',
        'xsec': 951.4*(6077.22/(5125+951.4+358.6)), #NLO xs 1J * incl NNLO xs/ incl NLO xs
    },
    'DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'DYJets_2J_NLO',
        'xsec': 358.6*(6077.22/(5125+951.4+358.6)), #NLO xs 2J * incl NNLO xs/ incl NLO xs
    },
    'DYJetsToMuMu_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos':
    {
        'name': 'DYJetsToMuMu',
        'xsec': 1976.0,
    },
    'DYJetsToEE_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos':
    {
        'name': 'DYJetsToEE',
        'xsec': 1976.0,
    },
    'DYJetsToTauTau_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos':
    {
        'name': 'DYJetsToTauTau',
        'xsec': 1976.0,
    },
    'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8':
    {
        'name': 'WJets',
        'xsec': 61526.7, #NNLO
    },
    'W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8':
    {
        'name': 'WJets_1jetBinned',
        'xsec': 8873.0*(61526.7/53870.0), #LO * incl NNLO xs/ incl LO xs
    },
    'W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8':
    {
        'name': 'WJets_2jetBinned',
        'xsec': 2793.0*(61526.7/53870.0), #LO * incl NNLO xs/ incl LO xs
    },
    'W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8':
    {
        'name': 'WJets_3jetBinned',
        'xsec': 992.5*(61526.7/53870.0), #LO * incl NNLO xs/ incl LO xs
    },
    'W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8':
    {
        'name': 'WJets_4jetBinned',
        'xsec': 544.3*(61526.7/53870.0),  #LO * incl NNLO xs/ incl LO xs
    },
    'WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'WJets_NLO',
        'xsec': 61526.7,#incl NNLO xs
    },
    'WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'WJets_0jetBinned_NLO',
        'xsec': 53300.0*(61526.7/(53300+8949+3335)),#NLO xs 0J * incl NNLO xs/ incl NLO xs
    },
    'WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'WJets_1jetBinned_NLO',
        'xsec': 8949.0*(61526.7/(53300+8949+3335)),#NLO xs 1J * incl NNLO xs/ incl NLO xs
    },
    'WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'WJets_2jetBinned_NLO',
        'xsec': 3335.0*(61526.7/(53300+8949+3335)),#NLO xs 2J * incl NNLO xs/ incl NLO xs
    },
     'TT_TuneCH3_13TeV-powheg-herwig7':
    {
        'name': 'TT',
        'xsec': 831.76, #NNLO
    },
     'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'TTTo2L2Nu',
        'xsec': 88.29, #NNLO
    },
     'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_HPS':
    {
        'name': 'TTTo2L2Nu',
        'xsec': 88.29, #NNLO
    },
     'TTToHadronic_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'TTToHadronic',
        'xsec': 377.96, #NNLO
    },
     'TTToHadronic_TuneCP5_13TeV-powheg-pythia8_ext2':
    {
        'name': 'TTToHadronic_ext',
        'xsec': 377.96, #NNLO
    },
     'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'TTToSemiLeptonic',
        'xsec': 365.34, #NNLO
    },
     'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_ext3':
    {
        'name': 'TTToSemiLeptonic_ext',
        'xsec': 365.34, #NNLO
    },
     'WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'WWTo2L2Nu',
        'xsec': 11.08, #NLO
    },
     'WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'WWTo2L2Nu',
        'xsec': 11.08, #NLO
    },
     'WWTo4Q_NNPDF31_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'WWTo4Q',
        'xsec': 47.73, #NLO
    },
    'WWTo4Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'WWTo4Q',
        'xsec': 46.15, #NLO
    },
     'WWTo4Q_13TeV-powheg':
    {
        'name': 'WWTo4Q',
        'xsec': 45.2, #NLO
    },
    'WWTo1L1Nu2Q_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'WWTo1L1Nu2Q',
        'xsec': 45.99, #NLO
    },
    'WWTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'WWTo1L1Nu2Q',
        'xsec': 45.99, #NLO
    },
     'WWToLNuQQ_NNPDF31_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'WWToLNuQQ',
        'xsec': 45.99, #NLO
    },
     'WWToLNuQQ_13TeV-powheg':
    {
        'name': 'WWToLNuQQ',
        'xsec': 43.53, #NLO
    },
     'WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8':
    {
        'name': 'WZTo1L1Nu2Q',
        'xsec': 11.66,
    },
    'WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8':
    {
        'name': 'WZTo1L1Nu2Q',
        'xsec': 11.66,
    },
    'WZTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'WZTo1L1Nu2Q',
        'xsec': 10.73,
    },
     'WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8':
    {
        'name': 'WZTo1L3Nu',
        'xsec': 3.3,
    },
    'WZTo1L3Nu_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'WZTo1L3Nu',
        'xsec': 3.054,
    },
     'WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8':
    {
        'name': 'WZTo2L2Q',
        'xsec': 6.331,
    },
    'WZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'WZTo2L2Q',
        'xsec': 6.419,
    },
     'WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'WZTo3LNu',
        'xsec': 5.052,
    },
     'WZTo3LNu_mllmin01_NNPDF31_TuneCP5_13TeV_powheg_pythia8':
    {
        'name': 'WZTo3LNu',
        'xsec': 4.664,
    },
     'WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8_ext1':
    {
        'name': 'WZTo3LNu_ext',
        'xsec': 5.052,
    },
     'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8':
    {
        'name': 'ZZTo2L2Q',
        'xsec': 3.222,
    },
    'ZZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'ZZTo2L2Q',
        'xsec': 3.222,
    },
    'ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8':
    {
        'name': 'ZZTo2L2Nu',
        'xsec': 0.6008,
    },
     'ZZTo2Q2Nu_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8':
    {
        'name': 'ZZTo2Q2Nu',
        'xsec': 4.561,
    },
    'ZZTo2Q2Nu_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'ZZTo2Q2Nu',
        'xsec': 4.561,
    },

    'ZZTo2Q2Nu_13TeV_amcatnloFXFX_madspin_pythia8':
    {
        'name': 'ZZTo2Q2Nu',
        'xsec': 4.033,
    },
    'ZZTo2Nu2Q_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'ZZTo2Nu2Q',
        'xsec': 4.033,
    },

     'ZZTo4L_TuneCP5_13TeV_powheg_pythia8':
    {
        'name': 'ZZTo4L',
        'xsec': 1.325,
    },
     'ZZTo4L_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'ZZTo4L',
        'xsec': 1.369,
    },
    'ZZTo4L_M-1toInf_TuneCP5_13TeV_powheg_pythia8':
    {
        'name': 'ZZTo4L',
        'xsec': 13.74, #CHECK VALUE! value from XSDB
    },
    'ST_s-channel_antitop_leptonDecays_13TeV-PSweights_powheg-pythia':
    {
        'name': 'ST_s-channel_antitop',
        'xsec': 4.16, #NNLO link above
    },
    'ST_s-channel_top_leptonDecays_13TeV-PSweights_powheg-pythia':
    {
        'name': 'ST_s-channel_top',
        'xsec': 7.2, #NNLO
    },
    'ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8':
    {
        'name': 'ST_s-channel',
        'xsec': 11.36, #NNLO
    },
    'ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8':
    {
        'name': 'ST_t-channel_antitop',
        'xsec': 80.95, #NNLO
    },
    'ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8':
    {
        'name': 'ST_t-channel_top',
        'xsec': 136.02, #NNLO
    },
    'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'ST_tW_antitop',
        'xsec': 35.85, #NNLO
    },
    'ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'ST_tW_top',
        'xsec': 35.85, #NNLO
    },
    'SUSYGluGluToBBHToTauTau_M-80_TuneCP5_13TeV-amcatnlo-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M-80',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M-90_TuneCP5_13TeV-amcatnlo-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M-90',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M-100_TuneCP5_13TeV-amcatnlo-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M-100',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M-110_TuneCP5_13TeV-amcatnlo-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M-110',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M-120_TuneCP5_13TeV-amcatnlo-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M-120',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M-125_TuneCP5_13TeV-amcatnlo-pythia8':
    {
        'name': 'GluGluBBToHToTauTau',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M-130_TuneCP5_13TeV-amcatnlo-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M-130',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M-140_TuneCP5_13TeV-amcatnlo-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M-140',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M-160_TuneCP5_13TeV-amcatnlo-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M-160',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M-180_TuneCP5_13TeV-amcatnlo-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M-180',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M-200_TuneCP5_13TeV-amcatnlo-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M-200',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M-250_TuneCP5_13TeV-amcatnlo-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M-250',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M-300_TuneCP5_13TeV-amcatnlo-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M-300',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M80_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M80',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M100_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M100',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M120_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M120',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M125',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M130_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M130',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M140_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M140',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M160_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M160',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M180_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M180',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M200_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M200',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M250_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M250',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToBBHToTauTau_M300_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'GluGluBBToHToTauTau_M300',
        'xsec': 0.4822*0.06208, #NLO
    },
    'SUSYGluGluToJJHToTauTau_M-125_TuneCP5_13TeV-amcatnlo-pythia8':
    {
        'name': 'GluGluJJToHToTauTau',
        'xsec': 0.4822*0.06208, #NLO
    },
    'GluGluHToTauTau_M125_13TeV_powheg_pythia8':
    {
        'name': 'GluGluHToTauTau',
        'xsec': 48.52*0.06208, #NLO
    },
    'GluGluHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'GluGluHToTauTau',
        'xsec': 48.30*0.06208, #NLO
    },
    'GGFHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'GGFHToTauTau',
        'xsec': 48.52*0.06208, #NLO
    },
    'BBHToTauTau':
    {
        'name': 'BBHToTauTau',
        'xsec': 0.4822*0.06208, #NLO
    },
    'bbHToTauTau_M-125_4FS_TuneCP5_yb2_13TeV-amcatnlo-pythia8':
    {
        'name': 'BBHToTauTau',
        'xsec': 0.4822*0.06208, #NLO
    },
    'JJHToTauTau':
    {
        'name': 'JJHToTauTau',
        'xsec': 0.4822*0.06208, #NLO
    },
    'jjHToTauTau_M-125_4FS_TuneCP5_yb2_13TeV-amcatnlo-pythia8':
    {
        'name': 'JJHToTauTau',
        'xsec': 0.4822*0.06208, #NLO
    },
    'BBHToTauTau_pdf':
    {
        'name': 'BBHToTauTau_pdf',
        'xsec': 0.4822*0.06208, #NLO
    },
    'gghplusbb':
    {
        'name': 'gghplusbb',
        'xsec': 1.040*0.06208, #0.73/33.89 * 48.3 gg+2b generated xs/inclusive sample xs * N3LO xs
    },
    'bbHToTauTau_M-125_4FS_TuneCP5_yt2_13TeV-amcatnlo-pythia8':
    {
        'name': 'GluGluBBHToTauTau',
        'xsec': 1.040*0.06208, #0.73/33.89 * 48.3 gg+2b generated xs/inclusive sample xs * N3LO xs
    },
    'ggfhplusbb':
    {
        'name': 'ggfhplusbb',
        'xsec': 1.040*0.06208,
    },
    'jjHToTauTau_M-125_4FS_TuneCP5_yt2_13TeV-amcatnlo-pythia8':
    {
        'name': 'JJBBHToTauTau',
        'xsec': 1.040*0.06208, #0.73/33.89 * 48.3 gg+2b generated xs/inclusive sample xs * N3LO xs
    },
    'GluGluHToTauTau_M-125_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'GluGluHToTauTau',
        'xsec': 48.30*0.06208, #NLO
    },
    'GluGlujjHToTauTau_M-125_TuneCP5_13TeV-amcatnloFXFX-pythia8':
    {
        'name': 'GluGlujjHToTauTau',
        'xsec': 48.52*0.06208, #NLO
    },
    'bbHToTauTau_M-125_4FS_ybyt_TuneCP5-13TeV-amcatnlo-pythia8':
    {
        'name': 'BBHToTauTau_ybyt',
        'xsec': -0.033*0.06208,
    },
    'jjHToTauTau_M-125_4FS_ybyt_TuneCP5-13TeV-amcatnlo-pythia8':
    {
        'name': 'jjHToTauTau_ybyt',
        'xsec': -0.033*0.06208,
    },
    'gghplusbb_ext':
    {
        'name': 'gghplusbb_ext',
        'xsec': 1.040*0.06208,
    },
    'ggfhplusbb_ext':
    {
        'name': 'ggfhplusbb_ext',
        'xsec': 1.040*0.06208, 
    },
    'bbh_ybyt_miniaod':
    {
        'name': 'bbh_ybyt_miniaod',
        'xsec': -0.033*0.06208,
    },
    'VBFHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'VBFHToTauTau',
        'xsec': 3.77*0.06208,
    },
    'VBFHToTauTau_M125_13TeV_powheg_pythia8':
    {
        'name': 'VBFHToTauTau',
        'xsec': 3.77*0.06208,
    },
    'ZHToTauTau_M125_13TeV_powheg_pythia8':
    {
        'name': 'ZHToTauTau',
        'xsec': 0.8767*0.06208,
    },
    'ZHToTauTau_M125_CP5_13TeV-powheg-pythia8_ext1':
    {
        'name': 'ZHToTauTau',
        'xsec': 0.8767*0.06208,
    },
    'WplusHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'WplusHToTauTau',
        'xsec': 0.831*0.06208, #NLO
    },
    'WminusHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'WminusHToTauTau',
        'xsec': 0.527*0.06208, #NLO
    },
    'ttHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8':
    {
        'name': 'ttHToTauTau',
        'xsec': 0.5033*0.06208, #NLO
    },
    'ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8':
    {
        'name': 'ttHJetToNonbb',
        'xsec': 0.5033*(1.-0.5760)
    },
    'ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8':
    {
        'name': 'ttZJets',
        'xsec': 0.5407
    },
    'ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8':
    {
        'name': 'ttWJets',
        'xsec': 0.4611
    },
    'tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8':
    {
        'name': 'tZq',
        'xsec': 0.07561
    },
}
