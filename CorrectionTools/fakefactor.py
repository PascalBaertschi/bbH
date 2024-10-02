from ROOT import TFile
from .ffunc import ffuncclass

#also change value in ff_derive.py!
cut_values = {
  "UL2018":{
    "mutau":{
      "1prong":{
        "qcd":90.,
        "w":115.,
        "tt":115.
      },
      "3prong":{
        "qcd":90.,
        "w":115.,
        "tt":90.
      },
    },
    "etau":{
      "1prong":{
        "qcd":90.,
        "w":115.,
        "tt":115.
      },
      "3prong":{
        "qcd":90.,
        "w":115.,
        "tt":90.
      },
    },
  },
  "UL2017":{
    "mutau":{
      "1prong":{
        "qcd":105.,
        "w":115.,
        "tt":115.
      },
      "3prong":{
        "qcd":105.,
        "w":115.,
        "tt":115.
      },
    },
    "etau":{
      "1prong":{
        "qcd":90.,
        "w":115.,
        "tt":75.
      },
      "3prong":{
        "qcd":90.,
        "w":115.,
        "tt":75.
      },
    },
  },
  "UL2016":{
    "mutau":{
      "1prong":{
        "qcd":90.,
        "w":115.,
        "tt":115.
      },
      "3prong":{
        "qcd":105.,
        "w":115.,
        "tt":90.
      },
    },
    "etau":{
      "1prong":{
        "qcd":90.,
        "w":115.,
        "tt":115.
      },
      "3prong":{
        "qcd":90.,
        "w":115.,
        "tt":115.
      },
    },
  },
}


class ffclass:
    def __init__(self,year):
        #mutau
        self.year = "UL%s"%year
        ff_mutau_file = TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fakefactors_mutau_%s.root"%self.year,'READ')
        self.ff_mutau_qcd_1prong = ff_mutau_file.Get("ff_qcd_1prong")
        self.ff_mutau_qcd_flat_1prong = ff_mutau_file.Get("ff_qcd_flat_1prong")
        self.ff_mutau_w_1prong = ff_mutau_file.Get("ff_w_1prong")
        self.ff_mutau_tt_1prong = ff_mutau_file.Get("ff_tt_1prong")
        self.ff_mutau_qcd_3prong = ff_mutau_file.Get("ff_qcd_3prong")
        self.ff_mutau_qcd_flat_3prong = ff_mutau_file.Get("ff_qcd_flat_3prong")
        self.ff_mutau_w_3prong = ff_mutau_file.Get("ff_w_3prong")
        self.ff_mutau_tt_3prong = ff_mutau_file.Get("ff_tt_3prong")
        self.ff_mutau_qcd_1prong.SetDirectory(0)
        self.ff_mutau_qcd_flat_1prong.SetDirectory(0)
        self.ff_mutau_w_1prong.SetDirectory(0)
        self.ff_mutau_tt_1prong.SetDirectory(0)
        self.ff_mutau_qcd_3prong.SetDirectory(0)
        self.ff_mutau_qcd_flat_3prong.SetDirectory(0)
        self.ff_mutau_w_3prong.SetDirectory(0)
        self.ff_mutau_tt_3prong.SetDirectory(0)
        ff_mutau_file.Close()
        frac_mutau_1prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_mutau_%s_1prong.root"%self.year,'READ')
        self.frac_mutau_1prong_qcd = frac_mutau_1prong_file.Get("Multijet_AR_1prong")
        self.frac_mutau_1prong_w = frac_mutau_1prong_file.Get("WJetscomb_AR_1prong")
        self.frac_mutau_1prong_dy = frac_mutau_1prong_file.Get("DYJetscomb_AR_1prong")
        self.frac_mutau_1prong_tt = frac_mutau_1prong_file.Get("TT_AR_1prong")
        self.frac_mutau_1prong_st = frac_mutau_1prong_file.Get("ST_AR_1prong")
        self.frac_mutau_1prong_qcd.SetDirectory(0)
        self.frac_mutau_1prong_w.SetDirectory(0)
        self.frac_mutau_1prong_dy.SetDirectory(0)
        self.frac_mutau_1prong_tt.SetDirectory(0)
        self.frac_mutau_1prong_st.SetDirectory(0)
        frac_mutau_1prong_file.Close()
        frac_mutau_3prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_mutau_%s_3prong.root"%self.year,'READ')
        self.frac_mutau_3prong_qcd = frac_mutau_3prong_file.Get("Multijet_AR_3prong")
        self.frac_mutau_3prong_w = frac_mutau_3prong_file.Get("WJetscomb_AR_3prong")
        self.frac_mutau_3prong_dy = frac_mutau_3prong_file.Get("DYJetscomb_AR_3prong")
        self.frac_mutau_3prong_tt = frac_mutau_3prong_file.Get("TT_AR_3prong")
        self.frac_mutau_3prong_st = frac_mutau_3prong_file.Get("ST_AR_3prong")
        self.frac_mutau_3prong_qcd.SetDirectory(0)
        self.frac_mutau_3prong_w.SetDirectory(0)
        self.frac_mutau_3prong_dy.SetDirectory(0)
        self.frac_mutau_3prong_tt.SetDirectory(0)
        self.frac_mutau_3prong_st.SetDirectory(0)
        frac_mutau_3prong_file.Close()
        #etau
        ff_etau_file = TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fakefactors_etau_%s.root"%self.year,'READ')
        self.ff_etau_qcd_1prong = ff_etau_file.Get("ff_qcd_1prong")
        self.ff_etau_qcd_flat_1prong = ff_etau_file.Get("ff_qcd_flat_1prong")
        self.ff_etau_w_1prong = ff_etau_file.Get("ff_w_1prong")
        self.ff_etau_tt_1prong = ff_etau_file.Get("ff_tt_1prong")
        self.ff_etau_qcd_3prong = ff_etau_file.Get("ff_qcd_3prong")
        self.ff_etau_qcd_flat_3prong = ff_etau_file.Get("ff_qcd_flat_3prong")
        self.ff_etau_w_3prong = ff_etau_file.Get("ff_w_3prong")
        self.ff_etau_tt_3prong = ff_etau_file.Get("ff_tt_3prong")
        self.ff_etau_qcd_1prong.SetDirectory(0)
        self.ff_etau_qcd_flat_1prong.SetDirectory(0)
        self.ff_etau_w_1prong.SetDirectory(0)
        self.ff_etau_tt_1prong.SetDirectory(0)
        self.ff_etau_qcd_3prong.SetDirectory(0)
        self.ff_etau_qcd_flat_3prong.SetDirectory(0)
        self.ff_etau_w_3prong.SetDirectory(0)
        self.ff_etau_tt_3prong.SetDirectory(0)
        ff_etau_file.Close()
        frac_etau_1prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_etau_%s_1prong.root"%self.year,'READ')
        self.frac_etau_1prong_qcd = frac_etau_1prong_file.Get("Multijet_AR_1prong")
        self.frac_etau_1prong_w = frac_etau_1prong_file.Get("WJetscomb_AR_1prong")
        self.frac_etau_1prong_dy = frac_etau_1prong_file.Get("DYJetscomb_AR_1prong")
        self.frac_etau_1prong_tt = frac_etau_1prong_file.Get("TT_AR_1prong")
        self.frac_etau_1prong_st = frac_etau_1prong_file.Get("ST_AR_1prong")
        self.frac_etau_1prong_qcd.SetDirectory(0)
        self.frac_etau_1prong_w.SetDirectory(0)
        self.frac_etau_1prong_dy.SetDirectory(0)
        self.frac_etau_1prong_tt.SetDirectory(0)
        self.frac_etau_1prong_st.SetDirectory(0)
        frac_etau_1prong_file.Close()
        frac_etau_3prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_etau_%s_3prong.root"%self.year,'READ')
        self.frac_etau_3prong_qcd = frac_etau_3prong_file.Get("Multijet_AR_3prong")
        self.frac_etau_3prong_w = frac_etau_3prong_file.Get("WJetscomb_AR_3prong")
        self.frac_etau_3prong_dy = frac_etau_3prong_file.Get("DYJetscomb_AR_3prong")
        self.frac_etau_3prong_tt = frac_etau_3prong_file.Get("TT_AR_3prong")
        self.frac_etau_3prong_st = frac_etau_3prong_file.Get("ST_AR_3prong")
        self.frac_etau_3prong_qcd.SetDirectory(0)
        self.frac_etau_3prong_w.SetDirectory(0)
        self.frac_etau_3prong_dy.SetDirectory(0)
        self.frac_etau_3prong_tt.SetDirectory(0)
        self.frac_etau_3prong_st.SetDirectory(0)
        frac_etau_3prong_file.Close()
        #fractions for TT DR mutau
        ttfrac_mutau_1prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_TTDR_mutau_%s_1prong.root"%self.year,'READ')
        self.ttfrac_mutau_1prong_qcd = ttfrac_mutau_1prong_file.Get("Multijet_ARTT_1prong")
        self.ttfrac_mutau_1prong_w = ttfrac_mutau_1prong_file.Get("WJetscomb_ARTT_1prong")
        self.ttfrac_mutau_1prong_dy = ttfrac_mutau_1prong_file.Get("DYJetscomb_ARTT_1prong")
        self.ttfrac_mutau_1prong_tt = ttfrac_mutau_1prong_file.Get("TT_ARTT_1prong")
        self.ttfrac_mutau_1prong_st = ttfrac_mutau_1prong_file.Get("ST_ARTT_1prong")
        self.ttfrac_mutau_1prong_qcd.SetDirectory(0)
        self.ttfrac_mutau_1prong_w.SetDirectory(0)
        self.ttfrac_mutau_1prong_dy.SetDirectory(0)
        self.ttfrac_mutau_1prong_tt.SetDirectory(0)
        self.ttfrac_mutau_1prong_st.SetDirectory(0)
        ttfrac_mutau_1prong_file.Close()
        ttfrac_mutau_3prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_TTDR_mutau_%s_3prong.root"%self.year,'READ')
        self.ttfrac_mutau_3prong_qcd = ttfrac_mutau_3prong_file.Get("Multijet_ARTT_3prong")
        self.ttfrac_mutau_3prong_w = ttfrac_mutau_3prong_file.Get("WJetscomb_ARTT_3prong")
        self.ttfrac_mutau_3prong_dy = ttfrac_mutau_3prong_file.Get("DYJetscomb_ARTT_3prong")
        self.ttfrac_mutau_3prong_tt = ttfrac_mutau_3prong_file.Get("TT_ARTT_3prong")
        self.ttfrac_mutau_3prong_st = ttfrac_mutau_3prong_file.Get("ST_ARTT_3prong")
        self.ttfrac_mutau_3prong_qcd.SetDirectory(0)
        self.ttfrac_mutau_3prong_w.SetDirectory(0)
        self.ttfrac_mutau_3prong_dy.SetDirectory(0)
        self.ttfrac_mutau_3prong_tt.SetDirectory(0)
        self.ttfrac_mutau_3prong_st.SetDirectory(0)
        ttfrac_mutau_3prong_file.Close()
        #fractions for TT DR etau
        ttfrac_etau_1prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_TTDR_etau_%s_1prong.root"%self.year,'READ')
        self.ttfrac_etau_1prong_qcd = ttfrac_etau_1prong_file.Get("Multijet_ARTT_1prong")
        self.ttfrac_etau_1prong_w = ttfrac_etau_1prong_file.Get("WJetscomb_ARTT_1prong")
        self.ttfrac_etau_1prong_dy = ttfrac_etau_1prong_file.Get("DYJetscomb_ARTT_1prong")
        self.ttfrac_etau_1prong_tt = ttfrac_etau_1prong_file.Get("TT_ARTT_1prong")
        self.ttfrac_etau_1prong_st = ttfrac_etau_1prong_file.Get("ST_ARTT_1prong")
        self.ttfrac_etau_1prong_qcd.SetDirectory(0)
        self.ttfrac_etau_1prong_w.SetDirectory(0)
        self.ttfrac_etau_1prong_dy.SetDirectory(0)
        self.ttfrac_etau_1prong_tt.SetDirectory(0)
        self.ttfrac_etau_1prong_st.SetDirectory(0)
        ttfrac_etau_1prong_file.Close()
        ttfrac_etau_3prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_TTDR_etau_%s_3prong.root"%self.year,'READ')
        self.ttfrac_etau_3prong_qcd = ttfrac_etau_3prong_file.Get("Multijet_ARTT_3prong")
        self.ttfrac_etau_3prong_w = ttfrac_etau_3prong_file.Get("WJetscomb_ARTT_3prong")
        self.ttfrac_etau_3prong_dy = ttfrac_etau_3prong_file.Get("DYJetscomb_ARTT_3prong")
        self.ttfrac_etau_3prong_tt = ttfrac_etau_3prong_file.Get("TT_ARTT_3prong")
        self.ttfrac_etau_3prong_st = ttfrac_etau_3prong_file.Get("ST_ARTT_3prong")
        self.ttfrac_etau_3prong_qcd.SetDirectory(0)
        self.ttfrac_etau_3prong_w.SetDirectory(0)
        self.ttfrac_etau_3prong_dy.SetDirectory(0)
        self.ttfrac_etau_3prong_tt.SetDirectory(0)
        self.ttfrac_etau_3prong_st.SetDirectory(0)
        ttfrac_etau_3prong_file.Close()

        #fractions for QCD DR mutau
        qcdfrac_mutau_1prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_QCDDR_mutau_%s_1prong.root"%self.year,'READ')
        self.qcdfrac_mutau_1prong_qcd = qcdfrac_mutau_1prong_file.Get("Multijet_ARQCD_1prong")
        self.qcdfrac_mutau_1prong_w = qcdfrac_mutau_1prong_file.Get("WJetscomb_ARQCD_1prong")
        self.qcdfrac_mutau_1prong_dy = qcdfrac_mutau_1prong_file.Get("DYJetscomb_ARQCD_1prong")
        self.qcdfrac_mutau_1prong_tt = qcdfrac_mutau_1prong_file.Get("TT_ARQCD_1prong")
        self.qcdfrac_mutau_1prong_st = qcdfrac_mutau_1prong_file.Get("ST_ARQCD_1prong")
        self.qcdfrac_mutau_1prong_qcd.SetDirectory(0)
        self.qcdfrac_mutau_1prong_w.SetDirectory(0)
        self.qcdfrac_mutau_1prong_dy.SetDirectory(0)
        self.qcdfrac_mutau_1prong_tt.SetDirectory(0)
        self.qcdfrac_mutau_1prong_st.SetDirectory(0)
        qcdfrac_mutau_1prong_file.Close()
        qcdfrac_mutau_3prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_QCDDR_mutau_%s_3prong.root"%self.year,'READ')
        self.qcdfrac_mutau_3prong_qcd = qcdfrac_mutau_3prong_file.Get("Multijet_ARQCD_3prong")
        self.qcdfrac_mutau_3prong_w = qcdfrac_mutau_3prong_file.Get("WJetscomb_ARQCD_3prong")
        self.qcdfrac_mutau_3prong_dy = qcdfrac_mutau_3prong_file.Get("DYJetscomb_ARQCD_3prong")
        self.qcdfrac_mutau_3prong_tt = qcdfrac_mutau_3prong_file.Get("TT_ARQCD_3prong")
        self.qcdfrac_mutau_3prong_st = qcdfrac_mutau_3prong_file.Get("ST_ARQCD_3prong")
        self.qcdfrac_mutau_3prong_qcd.SetDirectory(0)
        self.qcdfrac_mutau_3prong_w.SetDirectory(0)
        self.qcdfrac_mutau_3prong_dy.SetDirectory(0)
        self.qcdfrac_mutau_3prong_tt.SetDirectory(0)
        self.qcdfrac_mutau_3prong_st.SetDirectory(0)
        qcdfrac_mutau_3prong_file.Close()
        #fractions for QCD DR etau
        qcdfrac_etau_1prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_QCDDR_etau_%s_1prong.root"%self.year,'READ')
        self.qcdfrac_etau_1prong_qcd = qcdfrac_etau_1prong_file.Get("Multijet_ARQCD_1prong")
        self.qcdfrac_etau_1prong_w = qcdfrac_etau_1prong_file.Get("WJetscomb_ARQCD_1prong")
        self.qcdfrac_etau_1prong_dy = qcdfrac_etau_1prong_file.Get("DYJetscomb_ARQCD_1prong")
        self.qcdfrac_etau_1prong_tt = qcdfrac_etau_1prong_file.Get("TT_ARQCD_1prong")
        self.qcdfrac_etau_1prong_st = qcdfrac_etau_1prong_file.Get("ST_ARQCD_1prong")
        self.qcdfrac_etau_1prong_qcd.SetDirectory(0)
        self.qcdfrac_etau_1prong_w.SetDirectory(0)
        self.qcdfrac_etau_1prong_dy.SetDirectory(0)
        self.qcdfrac_etau_1prong_tt.SetDirectory(0)
        self.qcdfrac_etau_1prong_st.SetDirectory(0)
        qcdfrac_etau_1prong_file.Close()
        qcdfrac_etau_3prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_QCDDR_etau_%s_3prong.root"%self.year,'READ')
        self.qcdfrac_etau_3prong_qcd = qcdfrac_etau_3prong_file.Get("Multijet_ARQCD_3prong")
        self.qcdfrac_etau_3prong_w = qcdfrac_etau_3prong_file.Get("WJetscomb_ARQCD_3prong")
        self.qcdfrac_etau_3prong_dy = qcdfrac_etau_3prong_file.Get("DYJetscomb_ARQCD_3prong")
        self.qcdfrac_etau_3prong_tt = qcdfrac_etau_3prong_file.Get("TT_ARQCD_3prong")
        self.qcdfrac_etau_3prong_st = qcdfrac_etau_3prong_file.Get("ST_ARQCD_3prong")
        self.qcdfrac_etau_3prong_qcd.SetDirectory(0)
        self.qcdfrac_etau_3prong_w.SetDirectory(0)
        self.qcdfrac_etau_3prong_dy.SetDirectory(0)
        self.qcdfrac_etau_3prong_tt.SetDirectory(0)
        self.qcdfrac_etau_3prong_st.SetDirectory(0)
        qcdfrac_etau_3prong_file.Close()
        
        #fractions for QCDScaleUp mutau
        upfrac_mutau_1prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_QCDScaleUp_mutau_%s_1prong.root"%self.year,'READ')
        self.upfrac_mutau_1prong_qcd = upfrac_mutau_1prong_file.Get("Multijet_ARQCDScaleUp_1prong")
        self.upfrac_mutau_1prong_w = upfrac_mutau_1prong_file.Get("WJetscomb_ARQCDScaleUp_1prong")
        self.upfrac_mutau_1prong_dy = upfrac_mutau_1prong_file.Get("DYJetscomb_ARQCDScaleUp_1prong")
        self.upfrac_mutau_1prong_tt = upfrac_mutau_1prong_file.Get("TT_ARQCDScaleUp_1prong")
        self.upfrac_mutau_1prong_st = upfrac_mutau_1prong_file.Get("ST_ARQCDScaleUp_1prong")
        self.upfrac_mutau_1prong_qcd.SetDirectory(0)
        self.upfrac_mutau_1prong_w.SetDirectory(0)
        self.upfrac_mutau_1prong_dy.SetDirectory(0)
        self.upfrac_mutau_1prong_tt.SetDirectory(0)
        self.upfrac_mutau_1prong_st.SetDirectory(0)
        upfrac_mutau_1prong_file.Close()
        upfrac_mutau_3prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_QCDScaleUp_mutau_%s_3prong.root"%self.year,'READ')
        self.upfrac_mutau_3prong_qcd = upfrac_mutau_3prong_file.Get("Multijet_ARQCDScaleUp_3prong")
        self.upfrac_mutau_3prong_w = upfrac_mutau_3prong_file.Get("WJetscomb_ARQCDScaleUp_3prong")
        self.upfrac_mutau_3prong_dy = upfrac_mutau_3prong_file.Get("DYJetscomb_ARQCDScaleUp_3prong")
        self.upfrac_mutau_3prong_tt = upfrac_mutau_3prong_file.Get("TT_ARQCDScaleUp_3prong")
        self.upfrac_mutau_3prong_st = upfrac_mutau_3prong_file.Get("ST_ARQCDScaleUp_3prong")
        self.upfrac_mutau_3prong_qcd.SetDirectory(0)
        self.upfrac_mutau_3prong_w.SetDirectory(0)
        self.upfrac_mutau_3prong_dy.SetDirectory(0)
        self.upfrac_mutau_3prong_tt.SetDirectory(0)
        self.upfrac_mutau_3prong_st.SetDirectory(0)
        upfrac_mutau_3prong_file.Close()
        #fractions for QCDScaleUp etau
        upfrac_etau_1prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_QCDScaleUp_etau_%s_1prong.root"%self.year,'READ')
        self.upfrac_etau_1prong_qcd = upfrac_etau_1prong_file.Get("Multijet_ARQCDScaleUp_1prong")
        self.upfrac_etau_1prong_w = upfrac_etau_1prong_file.Get("WJetscomb_ARQCDScaleUp_1prong")
        self.upfrac_etau_1prong_dy = upfrac_etau_1prong_file.Get("DYJetscomb_ARQCDScaleUp_1prong")
        self.upfrac_etau_1prong_tt = upfrac_etau_1prong_file.Get("TT_ARQCDScaleUp_1prong")
        self.upfrac_etau_1prong_st = upfrac_etau_1prong_file.Get("ST_ARQCDScaleUp_1prong")
        self.upfrac_etau_1prong_qcd.SetDirectory(0)
        self.upfrac_etau_1prong_w.SetDirectory(0)
        self.upfrac_etau_1prong_dy.SetDirectory(0)
        self.upfrac_etau_1prong_tt.SetDirectory(0)
        self.upfrac_etau_1prong_st.SetDirectory(0)
        upfrac_etau_1prong_file.Close()
        upfrac_etau_3prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_QCDScaleUp_etau_%s_3prong.root"%self.year,'READ')
        self.upfrac_etau_3prong_qcd = upfrac_etau_3prong_file.Get("Multijet_ARQCDScaleUp_3prong")
        self.upfrac_etau_3prong_w = upfrac_etau_3prong_file.Get("WJetscomb_ARQCDScaleUp_3prong")
        self.upfrac_etau_3prong_dy = upfrac_etau_3prong_file.Get("DYJetscomb_ARQCDScaleUp_3prong")
        self.upfrac_etau_3prong_tt = upfrac_etau_3prong_file.Get("TT_ARQCDScaleUp_3prong")
        self.upfrac_etau_3prong_st = upfrac_etau_3prong_file.Get("ST_ARQCDScaleUp_3prong")
        self.upfrac_etau_3prong_qcd.SetDirectory(0)
        self.upfrac_etau_3prong_w.SetDirectory(0)
        self.upfrac_etau_3prong_dy.SetDirectory(0)
        self.upfrac_etau_3prong_tt.SetDirectory(0)
        self.upfrac_etau_3prong_st.SetDirectory(0)
        upfrac_etau_3prong_file.Close()

        #fractions for QCDScaleDown mutau
        downfrac_mutau_1prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_QCDScaleDown_mutau_%s_1prong.root"%self.year,'READ')
        self.downfrac_mutau_1prong_qcd = downfrac_mutau_1prong_file.Get("Multijet_ARQCDScaleDown_1prong")
        self.downfrac_mutau_1prong_w = downfrac_mutau_1prong_file.Get("WJetscomb_ARQCDScaleDown_1prong")
        self.downfrac_mutau_1prong_dy = downfrac_mutau_1prong_file.Get("DYJetscomb_ARQCDScaleDown_1prong")
        self.downfrac_mutau_1prong_tt = downfrac_mutau_1prong_file.Get("TT_ARQCDScaleDown_1prong")
        self.downfrac_mutau_1prong_st = downfrac_mutau_1prong_file.Get("ST_ARQCDScaleDown_1prong")
        self.downfrac_mutau_1prong_qcd.SetDirectory(0)
        self.downfrac_mutau_1prong_w.SetDirectory(0)
        self.downfrac_mutau_1prong_dy.SetDirectory(0)
        self.downfrac_mutau_1prong_tt.SetDirectory(0)
        self.downfrac_mutau_1prong_st.SetDirectory(0)
        downfrac_mutau_1prong_file.Close()
        downfrac_mutau_3prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_QCDScaleDown_mutau_%s_3prong.root"%self.year,'READ')
        self.downfrac_mutau_3prong_qcd = downfrac_mutau_3prong_file.Get("Multijet_ARQCDScaleDown_3prong")
        self.downfrac_mutau_3prong_w = downfrac_mutau_3prong_file.Get("WJetscomb_ARQCDScaleDown_3prong")
        self.downfrac_mutau_3prong_dy = downfrac_mutau_3prong_file.Get("DYJetscomb_ARQCDScaleDown_3prong")
        self.downfrac_mutau_3prong_tt = downfrac_mutau_3prong_file.Get("TT_ARQCDScaleDown_3prong")
        self.downfrac_mutau_3prong_st = downfrac_mutau_3prong_file.Get("ST_ARQCDScaleDown_3prong")
        self.downfrac_mutau_3prong_qcd.SetDirectory(0)
        self.downfrac_mutau_3prong_w.SetDirectory(0)
        self.downfrac_mutau_3prong_dy.SetDirectory(0)
        self.downfrac_mutau_3prong_tt.SetDirectory(0)
        self.downfrac_mutau_3prong_st.SetDirectory(0)
        downfrac_mutau_3prong_file.Close()
        #fractions for QCDScaleDown etau
        downfrac_etau_1prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_QCDScaleDown_etau_%s_1prong.root"%self.year,'READ')
        self.downfrac_etau_1prong_qcd = downfrac_etau_1prong_file.Get("Multijet_ARQCDScaleDown_1prong")
        self.downfrac_etau_1prong_w = downfrac_etau_1prong_file.Get("WJetscomb_ARQCDScaleDown_1prong")
        self.downfrac_etau_1prong_dy = downfrac_etau_1prong_file.Get("DYJetscomb_ARQCDScaleDown_1prong")
        self.downfrac_etau_1prong_tt = downfrac_etau_1prong_file.Get("TT_ARQCDScaleDown_1prong")
        self.downfrac_etau_1prong_st = downfrac_etau_1prong_file.Get("ST_ARQCDScaleDown_1prong")
        self.downfrac_etau_1prong_qcd.SetDirectory(0)
        self.downfrac_etau_1prong_w.SetDirectory(0)
        self.downfrac_etau_1prong_dy.SetDirectory(0)
        self.downfrac_etau_1prong_tt.SetDirectory(0)
        self.downfrac_etau_1prong_st.SetDirectory(0)
        downfrac_etau_1prong_file.Close()
        downfrac_etau_3prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_QCDScaleDown_etau_%s_3prong.root"%self.year,'READ')
        self.downfrac_etau_3prong_qcd = downfrac_etau_3prong_file.Get("Multijet_ARQCDScaleDown_3prong")
        self.downfrac_etau_3prong_w = downfrac_etau_3prong_file.Get("WJetscomb_ARQCDScaleDown_3prong")
        self.downfrac_etau_3prong_dy = downfrac_etau_3prong_file.Get("DYJetscomb_ARQCDScaleDown_3prong")
        self.downfrac_etau_3prong_tt = downfrac_etau_3prong_file.Get("TT_ARQCDScaleDown_3prong")
        self.downfrac_etau_3prong_st = downfrac_etau_3prong_file.Get("ST_ARQCDScaleDown_3prong")
        self.downfrac_etau_3prong_qcd.SetDirectory(0)
        self.downfrac_etau_3prong_w.SetDirectory(0)
        self.downfrac_etau_3prong_dy.SetDirectory(0)
        self.downfrac_etau_3prong_tt.SetDirectory(0)
        self.downfrac_etau_3prong_st.SetDirectory(0)
        downfrac_etau_3prong_file.Close()

        #corrections
        corr_mutau_file = TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/ffvarcorrection_mutau_%s.root"%self.year,'READ')
        #hmass correction
        self.hmass_mutau_qcd_1prong = corr_mutau_file.Get("ff_qcd_1prong_H_mass")
        self.hmass_mutau_qcd_3prong = corr_mutau_file.Get("ff_qcd_3prong_H_mass")
        self.hmass_mutau_qcd_1prong.SetDirectory(0)
        self.hmass_mutau_qcd_3prong.SetDirectory(0)
        self.hmass_mutau_tt_1prong = corr_mutau_file.Get("ff_tt_1prong_H_mass")
        self.hmass_mutau_tt_3prong = corr_mutau_file.Get("ff_tt_3prong_H_mass")
        self.hmass_mutau_tt_1prong.SetDirectory(0)
        self.hmass_mutau_tt_3prong.SetDirectory(0)
        #Jet pt correction
        self.jetpt_mutau_qcd_1prong = corr_mutau_file.Get("ff_qcd_1prong_Jet1_pt")
        self.jetpt_mutau_qcd_3prong = corr_mutau_file.Get("ff_qcd_3prong_Jet1_pt")
        self.jetpt_mutau_qcd_1prong.SetDirectory(0)
        self.jetpt_mutau_qcd_3prong.SetDirectory(0)
        self.jetpt_mutau_tt_1prong = corr_mutau_file.Get("ff_tt_1prong_Jet1_pt")
        self.jetpt_mutau_tt_3prong = corr_mutau_file.Get("ff_tt_3prong_Jet1_pt")
        self.jetpt_mutau_tt_1prong.SetDirectory(0)
        self.jetpt_mutau_tt_3prong.SetDirectory(0)
        #collinear mass correction
        self.collinearmass_mutau_qcd_1prong = corr_mutau_file.Get("ff_qcd_1prong_collinear_mass")
        self.collinearmass_mutau_qcd_3prong = corr_mutau_file.Get("ff_qcd_3prong_collinear_mass")
        self.collinearmass_mutau_qcd_1prong.SetDirectory(0)
        self.collinearmass_mutau_qcd_3prong.SetDirectory(0)
        self.collinearmass_mutau_tt_1prong = corr_mutau_file.Get("ff_tt_1prong_collinear_mass")
        self.collinearmass_mutau_tt_3prong = corr_mutau_file.Get("ff_tt_3prong_collinear_mass")
        self.collinearmass_mutau_tt_1prong.SetDirectory(0)
        self.collinearmass_mutau_tt_3prong.SetDirectory(0)
        #TauJ mass correction
        self.taujmass_mutau_qcd_1prong = corr_mutau_file.Get("ff_qcd_1prong_TauJ_mass")
        self.taujmass_mutau_qcd_3prong = corr_mutau_file.Get("ff_qcd_3prong_TauJ_mass")
        self.taujmass_mutau_qcd_1prong.SetDirectory(0)
        self.taujmass_mutau_qcd_3prong.SetDirectory(0)
        self.taujmass_mutau_tt_1prong = corr_mutau_file.Get("ff_tt_1prong_TauJ_mass")
        self.taujmass_mutau_tt_3prong = corr_mutau_file.Get("ff_tt_3prong_TauJ_mass")
        self.taujmass_mutau_tt_1prong.SetDirectory(0)
        self.taujmass_mutau_tt_3prong.SetDirectory(0)
        corr_mutau_file.Close()

        #etau
        corr_etau_file = TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/ffvarcorrection_etau_%s.root"%self.year,'READ')
        #H mass correction
        self.hmass_etau_qcd_1prong = corr_etau_file.Get("ff_qcd_1prong_H_mass")
        self.hmass_etau_qcd_3prong = corr_etau_file.Get("ff_qcd_3prong_H_mass")
        self.hmass_etau_qcd_1prong.SetDirectory(0)
        self.hmass_etau_qcd_3prong.SetDirectory(0)
        self.hmass_etau_tt_1prong = corr_etau_file.Get("ff_tt_1prong_H_mass")
        self.hmass_etau_tt_3prong = corr_etau_file.Get("ff_tt_3prong_H_mass")
        self.hmass_etau_tt_1prong.SetDirectory(0)
        self.hmass_etau_tt_3prong.SetDirectory(0)
        #Jet pt correction
        self.jetpt_etau_qcd_1prong = corr_etau_file.Get("ff_qcd_1prong_Jet1_pt")
        self.jetpt_etau_qcd_3prong = corr_etau_file.Get("ff_qcd_3prong_Jet1_pt")
        self.jetpt_etau_qcd_1prong.SetDirectory(0)
        self.jetpt_etau_qcd_3prong.SetDirectory(0)
        self.jetpt_etau_tt_1prong = corr_etau_file.Get("ff_tt_1prong_Jet1_pt")
        self.jetpt_etau_tt_3prong = corr_etau_file.Get("ff_tt_3prong_Jet1_pt")
        self.jetpt_etau_tt_1prong.SetDirectory(0)
        self.jetpt_etau_tt_3prong.SetDirectory(0)
        #collinear mass correction
        self.collinearmass_etau_qcd_1prong = corr_etau_file.Get("ff_qcd_1prong_collinear_mass")
        self.collinearmass_etau_qcd_3prong = corr_etau_file.Get("ff_qcd_3prong_collinear_mass")
        self.collinearmass_etau_qcd_1prong.SetDirectory(0)
        self.collinearmass_etau_qcd_3prong.SetDirectory(0)
        self.collinearmass_etau_tt_1prong = corr_etau_file.Get("ff_tt_1prong_collinear_mass")
        self.collinearmass_etau_tt_3prong = corr_etau_file.Get("ff_tt_3prong_collinear_mass")
        self.collinearmass_etau_tt_1prong.SetDirectory(0)
        self.collinearmass_etau_tt_3prong.SetDirectory(0)
        #TauJ mass correction
        self.taujmass_etau_qcd_1prong = corr_etau_file.Get("ff_qcd_1prong_TauJ_mass")
        self.taujmass_etau_qcd_3prong = corr_etau_file.Get("ff_qcd_3prong_TauJ_mass")
        self.taujmass_etau_qcd_1prong.SetDirectory(0)
        self.taujmass_etau_qcd_3prong.SetDirectory(0)
        self.taujmass_etau_tt_1prong = corr_etau_file.Get("ff_tt_1prong_TauJ_mass")
        self.taujmass_etau_tt_3prong = corr_etau_file.Get("ff_tt_3prong_TauJ_mass")
        self.taujmass_etau_tt_1prong.SetDirectory(0)
        self.taujmass_etau_tt_3prong.SetDirectory(0)
        corr_etau_file.Close()
        # load files for uncertainties
        self.ffunc = ffuncclass(year)

    def getff(self,pt_initial,hist):
        pt = pt_initial
        ff_initial = hist.GetBinContent(hist.GetXaxis().FindBin(pt))
        while (hist.GetBinContent(hist.GetXaxis().FindBin(pt)) < 0. or hist.GetBinContent(hist.GetXaxis().FindBin(pt)) == 0. or hist.GetBinContent(hist.GetXaxis().FindBin(pt)) > 1.):
            #print "correcting pt"
            pt-=5.
        return hist.GetBinContent(hist.GetXaxis().FindBin(pt))
        
    def getff_fit(self,pt,func,cut_value):
        if pt>cut_value:
            pt = cut_value
        return func.Eval(pt)

    def getcorr(self,val,hist):
        first_val = hist.GetBinCenter(1) 
        if val<first_val: val = first_val
        last_val = hist.GetBinCenter(hist.GetNbinsX())
        if val>last_val: val = last_val
        bin = hist.GetXaxis().FindBin(val)
        Content = hist.GetBinContent(bin)
        if Content<0.: Content = 1.
        Error = hist.GetBinError(bin)
        return 1.+((Content-1.)/(1.+Error)**3)


    def ffweight(self,pt,decaymode,channel):
        if decaymode in [0,1,2]:
            prong="1prong"
        elif decaymode in [10,11]:
            prong="3prong"
        else:
            return 0.
        if channel=="mutau":
            if prong=="1prong":
                func_ff_qcd = self.ff_mutau_qcd_1prong.GetFunction("pol1")
                func_ff_qcd_flat = self.ff_mutau_qcd_flat_1prong.GetFunction("pol0")
                func_ff_w = self.ff_mutau_w_1prong.GetFunction("pol2")
                func_ff_tt = self.ff_mutau_tt_1prong.GetFunction("pol1")
                hist_frac_qcd = self.frac_mutau_1prong_qcd
                hist_frac_w = self.frac_mutau_1prong_w
                hist_frac_dy = self.frac_mutau_1prong_dy
                hist_frac_tt = self.frac_mutau_1prong_tt
                hist_frac_st = self.frac_mutau_1prong_st
            elif prong=="3prong":
                func_ff_qcd = self.ff_mutau_qcd_3prong.GetFunction("pol1")
                func_ff_qcd_flat = self.ff_mutau_qcd_flat_3prong.GetFunction("pol0")
                func_ff_w = self.ff_mutau_w_3prong.GetFunction("pol2")
                func_ff_tt = self.ff_mutau_tt_3prong.GetFunction("pol1")
                hist_frac_qcd = self.frac_mutau_3prong_qcd
                hist_frac_w = self.frac_mutau_3prong_w
                hist_frac_dy = self.frac_mutau_3prong_dy
                hist_frac_tt = self.frac_mutau_3prong_tt
                hist_frac_st = self.frac_mutau_3prong_st
        elif channel=="etau":
            if prong=="1prong":
                func_ff_qcd = self.ff_etau_qcd_1prong.GetFunction("pol1")
                func_ff_qcd_flat = self.ff_etau_qcd_flat_1prong.GetFunction("pol0")
                func_ff_w = self.ff_etau_w_1prong.GetFunction("pol2")
                func_ff_tt = self.ff_etau_tt_1prong.GetFunction("pol1")
                hist_frac_qcd = self.frac_etau_1prong_qcd
                hist_frac_w = self.frac_etau_1prong_w
                hist_frac_dy = self.frac_etau_1prong_dy
                hist_frac_tt = self.frac_etau_1prong_tt
                hist_frac_st = self.frac_etau_1prong_st
            elif prong=="3prong":
                func_ff_qcd = self.ff_etau_qcd_3prong.GetFunction("pol1")
                func_ff_qcd_flat = self.ff_etau_qcd_flat_3prong.GetFunction("pol0")
                func_ff_w = self.ff_etau_w_3prong.GetFunction("pol2")
                func_ff_tt = self.ff_etau_tt_3prong.GetFunction("pol1")
                hist_frac_qcd = self.frac_etau_3prong_qcd
                hist_frac_w = self.frac_etau_3prong_w
                hist_frac_dy = self.frac_etau_3prong_dy
                hist_frac_tt = self.frac_etau_3prong_tt
                hist_frac_st = self.frac_etau_3prong_st
        cutvalue_qcd = cut_values[self.year][channel][prong]["qcd"]
        cutvalue_w  = cut_values[self.year][channel][prong]["w"]
        cutvalue_tt = cut_values[self.year][channel][prong]["tt"]
        ff_qcd = self.getff_fit(pt,func_ff_qcd,cutvalue_qcd)
        ff_qcd_flat = self.getff_fit(pt,func_ff_qcd_flat,130.)
        ff_w = self.getff_fit(pt,func_ff_w,cutvalue_w)
        ff_tt = self.getff_fit(pt,func_ff_tt,cutvalue_tt)
        frac_qcd = hist_frac_qcd.GetBinContent(hist_frac_qcd.GetXaxis().FindBin(pt))
        frac_w = hist_frac_w.GetBinContent(hist_frac_w.GetXaxis().FindBin(pt))
        frac_dy = hist_frac_dy.GetBinContent(hist_frac_dy.GetXaxis().FindBin(pt))
        frac_tt = hist_frac_tt.GetBinContent(hist_frac_tt.GetXaxis().FindBin(pt))
        frac_st = hist_frac_st.GetBinContent(hist_frac_st.GetXaxis().FindBin(pt))
        ffuncertainties = self.ffunc.ffuncertainty(pt,decaymode,channel)
        ffunc_qcd = ffuncertainties[0]
        ffunc_w = ffuncertainties[1]
        ffunc_tt = ffuncertainties[2]
        ffunc_qcd_up = ffuncertainties[3]
        ffunc_qcd_down = ffuncertainties[4]
        ffunc_w_up = ffuncertainties[5]
        ffunc_w_down = ffuncertainties[6]
        ffunc_tt_up = ffuncertainties[7]
        ffunc_tt_down = ffuncertainties[8]
        ff = ((frac_qcd*ff_qcd)+((frac_w+frac_dy+frac_st)*ff_w)+(frac_tt*ff_tt))/(frac_qcd+frac_w+frac_dy+frac_st+frac_tt)
        ff_unc_up = ((frac_qcd*ff_qcd*ffunc_qcd_up)+((frac_w+frac_dy+frac_st)*ff_w*ffunc_w_up)+(frac_tt*ff_tt*ffunc_tt_up))/(frac_qcd+frac_w+frac_dy+frac_st+frac_tt)
        ff_unc_down = ((frac_qcd*ff_qcd*ffunc_qcd_down)+((frac_w+frac_dy+frac_st)*ff_w*ffunc_w_down)+(frac_tt*ff_tt*ffunc_tt_down))/(frac_qcd+frac_w+frac_dy+frac_st+frac_tt)
        ff_flatqcd = ((frac_qcd*ff_qcd_flat)+((frac_w+frac_dy+frac_st)*ff_w)+(frac_tt*ff_tt))/(frac_qcd+frac_w+frac_dy+frac_st+frac_tt)
        return[ff,ff_unc_up,ff_unc_down,ff_flatqcd]


    def ffweight_norm(self,pt,decaymode,channel):
        if decaymode in [0,1,2]:
            prong="1prong"
        elif decaymode in [10,11]:
            prong="3prong"
        else:
            return 1.
        if channel=="mutau":
            if prong=="1prong":
                hist_ff_qcd = self.ff_mutau_qcd_1prong
                hist_ff_w = self.ff_mutau_w_1prong
                hist_ff_tt = self.ff_mutau_tt_1prong
                hist_normfrac_qcd = self.normfrac_mutau_1prong_qcd
                hist_normfrac_w = self.normfrac_mutau_1prong_w
                hist_normfrac_dy = self.normfrac_mutau_1prong_dy
                hist_normfrac_tt = self.normfrac_mutau_1prong_tt
                hist_normfrac_st = self.normfrac_mutau_1prong_st
            elif prong=="3prong":
                hist_ff_qcd = self.ff_mutau_qcd_3prong
                hist_ff_w = self.ff_mutau_w_3prong
                hist_ff_tt = self.ff_mutau_tt_3prong
                hist_normfrac_qcd = self.normfrac_mutau_3prong_qcd
                hist_normfrac_w = self.normfrac_mutau_3prong_w
                hist_normfrac_dy = self.normfrac_mutau_3prong_dy
                hist_normfrac_tt = self.normfrac_mutau_3prong_tt
                hist_normfrac_st = self.normfrac_mutau_3prong_st
        elif channel=="etau":
            if prong=="1prong":
                hist_ff_qcd = self.ff_etau_qcd_1prong
                hist_ff_w = self.ff_etau_w_1prong
                hist_ff_tt = self.ff_etau_tt_1prong
                hist_normfrac_qcd = self.normfrac_etau_1prong_qcd
                hist_normfrac_w = self.normfrac_etau_1prong_w
                hist_normfrac_dy = self.normfrac_etau_1prong_dy
                hist_normfrac_tt = self.normfrac_etau_1prong_tt
                hist_normfrac_st = self.normfrac_etau_1prong_st
            elif prong=="3prong":
                hist_ff_qcd = self.ff_etau_qcd_3prong
                hist_ff_w = self.ff_etau_w_3prong
                hist_ff_tt = self.ff_etau_tt_3prong
                hist_normfrac_qcd = self.normfrac_etau_3prong_qcd
                hist_normfrac_w = self.normfrac_etau_3prong_w
                hist_normfrac_dy = self.normfrac_etau_3prong_dy
                hist_normfrac_tt = self.normfrac_etau_3prong_tt
                hist_normfrac_st = self.normfrac_etau_3prong_st
        ff_qcd = self.getff(pt,hist_ff_qcd)
        ff_w = self.getff(pt,hist_ff_w)
        ff_tt = self.getff(pt,hist_ff_tt)
        normfrac_qcd = hist_normfrac_qcd.GetBinContent(hist_normfrac_qcd.GetXaxis().FindBin(pt))
        normfrac_w = hist_normfrac_w.GetBinContent(hist_normfrac_w.GetXaxis().FindBin(pt))
        normfrac_dy = hist_normfrac_dy.GetBinContent(hist_normfrac_dy.GetXaxis().FindBin(pt))
        normfrac_tt = hist_normfrac_tt.GetBinContent(hist_normfrac_tt.GetXaxis().FindBin(pt))
        normfrac_st = hist_normfrac_st.GetBinContent(hist_normfrac_st.GetXaxis().FindBin(pt))
        #print("ttfrac_qcd:",ttfrac_qcd," ff_qcd:",ff_qcd," ttfrac_w:",ttfrac_w," ff_w:",ff_w," ttfrac_tt:",ttfrac_tt," ff_tt:",ff_tt)
        #print("ff_qcd:",ff_qcd, " ttfrac_qcd:",ttfrac_qcd)
        #print("ff_w:",ff_w," ttfrac_w:",ttfrac_w," ttfrac_dy:",ttfrac_dy)
        #print("ff_tt:",ff_tt," ttfrac_tt:",ttfrac_tt)
        #print("total ff:",((ttfrac_qcd*ff_qcd)+((ttfrac_w+ttfrac_dy)*ff_w)+(ttfrac_tt*ff_tt))/(ttfrac_qcd+ttfrac_w+ttfrac_dy+ttfrac_tt))
        return ((normfrac_qcd*ff_qcd)+((normfrac_w+normfrac_dy+normfrac_st)*ff_w)+(normfrac_tt*ff_tt))/(normfrac_qcd+normfrac_w+normfrac_dy+normfrac_st+normfrac_tt)





    def ffweight_corr(self,pt,hmass,jetpt,collinearmass,taujmass,decaymode,channel):
        if decaymode in [0,1,2]:
            prong="1prong"
        elif decaymode in [10,11]:
            prong="3prong"
        else:
            return 0.
        if channel=="mutau":
            if prong=="1prong":
                func_ff_qcd = self.ff_mutau_qcd_1prong.GetFunction("pol1")
                func_ff_w = self.ff_mutau_w_1prong.GetFunction("pol2")
                func_ff_tt = self.ff_mutau_tt_1prong.GetFunction("pol1")
                hist_frac_qcd = self.frac_mutau_1prong_qcd
                hist_frac_w = self.frac_mutau_1prong_w
                hist_frac_dy = self.frac_mutau_1prong_dy
                hist_frac_tt = self.frac_mutau_1prong_tt
                hist_frac_st = self.frac_mutau_1prong_st
                hist_upfrac_qcd = self.upfrac_mutau_1prong_qcd
                hist_upfrac_w = self.upfrac_mutau_1prong_w
                hist_upfrac_dy = self.upfrac_mutau_1prong_dy
                hist_upfrac_tt = self.upfrac_mutau_1prong_tt
                hist_upfrac_st = self.upfrac_mutau_1prong_st
                hist_downfrac_qcd = self.downfrac_mutau_1prong_qcd
                hist_downfrac_w = self.downfrac_mutau_1prong_w
                hist_downfrac_dy = self.downfrac_mutau_1prong_dy
                hist_downfrac_tt = self.downfrac_mutau_1prong_tt
                hist_downfrac_st = self.downfrac_mutau_1prong_st
            elif prong=="3prong":
                func_ff_qcd = self.ff_mutau_qcd_3prong.GetFunction("pol1")
                func_ff_w = self.ff_mutau_w_3prong.GetFunction("pol2")
                func_ff_tt = self.ff_mutau_tt_3prong.GetFunction("pol1")
                hist_frac_qcd = self.frac_mutau_3prong_qcd
                hist_frac_w = self.frac_mutau_3prong_w
                hist_frac_dy = self.frac_mutau_3prong_dy
                hist_frac_tt = self.frac_mutau_3prong_tt
                hist_frac_st = self.frac_mutau_3prong_st
                hist_upfrac_qcd = self.upfrac_mutau_3prong_qcd
                hist_upfrac_w = self.upfrac_mutau_3prong_w
                hist_upfrac_dy = self.upfrac_mutau_3prong_dy
                hist_upfrac_tt = self.upfrac_mutau_3prong_tt
                hist_upfrac_st = self.upfrac_mutau_3prong_st
                hist_downfrac_qcd = self.downfrac_mutau_3prong_qcd
                hist_downfrac_w = self.downfrac_mutau_3prong_w
                hist_downfrac_dy = self.downfrac_mutau_3prong_dy
                hist_downfrac_tt = self.downfrac_mutau_3prong_tt
                hist_downfrac_st = self.downfrac_mutau_3prong_st
        elif channel=="etau":
            if prong=="1prong":
                func_ff_qcd = self.ff_etau_qcd_1prong.GetFunction("pol1")
                #func_ff_qcd = self.ff_etau_qcd_1prong.GetFunction("pol0")
                func_ff_w = self.ff_etau_w_1prong.GetFunction("pol2")
                func_ff_tt = self.ff_etau_tt_1prong.GetFunction("pol1")
                hist_frac_qcd = self.frac_etau_1prong_qcd
                hist_frac_w = self.frac_etau_1prong_w
                hist_frac_dy = self.frac_etau_1prong_dy
                hist_frac_tt = self.frac_etau_1prong_tt
                hist_frac_st = self.frac_etau_1prong_st
                hist_upfrac_qcd = self.upfrac_etau_1prong_qcd
                hist_upfrac_w = self.upfrac_etau_1prong_w
                hist_upfrac_dy = self.upfrac_etau_1prong_dy
                hist_upfrac_tt = self.upfrac_etau_1prong_tt
                hist_upfrac_st = self.upfrac_etau_1prong_st
                hist_downfrac_qcd = self.downfrac_etau_1prong_qcd
                hist_downfrac_w = self.downfrac_etau_1prong_w
                hist_downfrac_dy = self.downfrac_etau_1prong_dy
                hist_downfrac_tt = self.downfrac_etau_1prong_tt
                hist_downfrac_st = self.downfrac_etau_1prong_st
            elif prong=="3prong":
                func_ff_qcd = self.ff_etau_qcd_3prong.GetFunction("pol1")
                #func_ff_qcd = self.ff_etau_qcd_3prong.GetFunction("pol0")
                func_ff_w = self.ff_etau_w_3prong.GetFunction("pol2")
                func_ff_tt = self.ff_etau_tt_3prong.GetFunction("pol1")
                hist_frac_qcd = self.frac_etau_3prong_qcd
                hist_frac_w = self.frac_etau_3prong_w
                hist_frac_dy = self.frac_etau_3prong_dy
                hist_frac_tt = self.frac_etau_3prong_tt
                hist_frac_st = self.frac_etau_3prong_st
                hist_upfrac_qcd = self.upfrac_etau_3prong_qcd
                hist_upfrac_w = self.upfrac_etau_3prong_w
                hist_upfrac_dy = self.upfrac_etau_3prong_dy
                hist_upfrac_tt = self.upfrac_etau_3prong_tt
                hist_upfrac_st = self.upfrac_etau_3prong_st
                hist_downfrac_qcd = self.downfrac_etau_3prong_qcd
                hist_downfrac_w = self.downfrac_etau_3prong_w
                hist_downfrac_dy = self.downfrac_etau_3prong_dy
                hist_downfrac_tt = self.downfrac_etau_3prong_tt
                hist_downfrac_st = self.downfrac_etau_3prong_st
        cutvalue_qcd = cut_values[self.year][channel][prong]["qcd"]
        cutvalue_w  = cut_values[self.year][channel][prong]["w"]
        cutvalue_tt = cut_values[self.year][channel][prong]["tt"]
        ff_qcd = self.getff_fit(pt,func_ff_qcd,cutvalue_qcd)
        ff_w = self.getff_fit(pt,func_ff_w,cutvalue_w)
        ff_tt = self.getff_fit(pt,func_ff_tt,cutvalue_tt)
        ffcorr_hmass_qcd = self.ffweightcorr_hmass(hmass,decaymode,channel,'qcd')
        ffcorr_jetpt_qcd = self.ffweightcorr_jetpt(jetpt,decaymode,channel,'qcd')
        ffcorr_collinearmass_qcd = self.ffweightcorr_collinearmass(collinearmass,decaymode,channel,'qcd')
        ffcorr_taujmass_qcd = self.ffweightcorr_taujmass(taujmass,decaymode,channel,'qcd')
        ffcorr_hmass_tt = self.ffweightcorr_hmass(hmass,decaymode,channel,'tt')
        ffcorr_jetpt_tt = self.ffweightcorr_jetpt(jetpt,decaymode,channel,'tt')
        ffcorr_collinearmass_tt = self.ffweightcorr_collinearmass(collinearmass,decaymode,channel,'tt')
        ffcorr_taujmass_tt = self.ffweightcorr_taujmass(taujmass,decaymode,channel,'tt')
        frac_qcd = hist_frac_qcd.GetBinContent(hist_frac_qcd.GetXaxis().FindBin(pt))
        frac_w = hist_frac_w.GetBinContent(hist_frac_w.GetXaxis().FindBin(pt))
        frac_dy = hist_frac_dy.GetBinContent(hist_frac_dy.GetXaxis().FindBin(pt))
        frac_tt = hist_frac_tt.GetBinContent(hist_frac_tt.GetXaxis().FindBin(pt))
        frac_st = hist_frac_st.GetBinContent(hist_frac_st.GetXaxis().FindBin(pt))
        frac_qcd_up = hist_upfrac_qcd.GetBinContent(hist_upfrac_qcd.GetXaxis().FindBin(pt))
        frac_w_up = hist_upfrac_w.GetBinContent(hist_upfrac_w.GetXaxis().FindBin(pt))
        frac_dy_up = hist_upfrac_dy.GetBinContent(hist_upfrac_dy.GetXaxis().FindBin(pt))
        frac_tt_up = hist_upfrac_tt.GetBinContent(hist_upfrac_tt.GetXaxis().FindBin(pt))
        frac_st_up = hist_upfrac_st.GetBinContent(hist_upfrac_st.GetXaxis().FindBin(pt))
        frac_qcd_down = hist_downfrac_qcd.GetBinContent(hist_downfrac_qcd.GetXaxis().FindBin(pt))
        frac_w_down = hist_downfrac_w.GetBinContent(hist_downfrac_w.GetXaxis().FindBin(pt))
        frac_dy_down = hist_downfrac_dy.GetBinContent(hist_downfrac_dy.GetXaxis().FindBin(pt))
        frac_tt_down = hist_downfrac_tt.GetBinContent(hist_downfrac_tt.GetXaxis().FindBin(pt))
        frac_st_down = hist_downfrac_st.GetBinContent(hist_downfrac_st.GetXaxis().FindBin(pt))
        ffuncertainties = self.ffunc.ffuncertainty(pt,decaymode,channel)
        ffunc_qcd = ffuncertainties[0]
        ffunc_w = ffuncertainties[1]
        ffunc_tt = ffuncertainties[2]
        ffunc_qcd_up = ffuncertainties[3]
        ffunc_qcd_down = ffuncertainties[4]
        ffunc_w_up = ffuncertainties[5]
        ffunc_w_down = ffuncertainties[6]
        ffunc_tt_up = ffuncertainties[7]
        ffunc_tt_down = ffuncertainties[8]
        ff_fitunc = self.ffunc.ff_fitunc(decaymode,channel,pt)
        ffunc_qcd_fitpar0_up = ff_fitunc[0][0]
        ffunc_qcd_fitpar0_down = ff_fitunc[0][1]
        ffunc_qcd_fitpar1_up = ff_fitunc[0][2]
        ffunc_qcd_fitpar1_down = ff_fitunc[0][3]
        ffunc_w_fitpar0_up = ff_fitunc[1][0]
        ffunc_w_fitpar0_down = ff_fitunc[1][1]
        ffunc_w_fitpar1_up = ff_fitunc[1][2]
        ffunc_w_fitpar1_down = ff_fitunc[1][3]
        ffunc_w_fitpar2_up = ff_fitunc[1][4]
        ffunc_w_fitpar2_down = ff_fitunc[1][5]
        ffunc_tt_fitpar0_up = ff_fitunc[2][0]
        ffunc_tt_fitpar0_down = ff_fitunc[2][1]
        ffunc_tt_fitpar1_up = ff_fitunc[2][2]
        ffunc_tt_fitpar1_down = ff_fitunc[2][3]
        ffcorr_qcd = ffcorr_hmass_qcd * ffcorr_jetpt_qcd * ffcorr_collinearmass_qcd * ffcorr_taujmass_qcd 
        ffcorr_tt = ffcorr_hmass_tt * ffcorr_jetpt_tt * ffcorr_collinearmass_tt * ffcorr_taujmass_tt 
        frac_total = frac_qcd+frac_w+frac_dy+frac_st+frac_tt
        frac_total_up = frac_qcd_up+frac_w_up+frac_dy_up+frac_st_up+frac_tt_up
        frac_total_down = frac_qcd_down+frac_w_down+frac_dy_down+frac_st_down+frac_tt_down
        ff_qcd_corr = ff_qcd*ffcorr_qcd
        ff_tt_corr = ff_tt*ffcorr_tt
        ff = ((frac_qcd*ff_qcd_corr)+((frac_w+frac_dy+frac_st)*ff_w)+(frac_tt*ff_tt_corr))/frac_total
        ff_unc_up = ((frac_qcd*ff_qcd_corr*ffunc_qcd_up)+((frac_w+frac_dy+frac_st)*ff_w*ffunc_w_up)+(frac_tt*ff_tt_corr*ffunc_tt_up))/frac_total
        ff_unc_down = ((frac_qcd*ff_qcd_corr*ffunc_qcd_down)+((frac_w+frac_dy+frac_st)*ff_w*ffunc_w_down)+(frac_tt*ff_tt_corr*ffunc_tt_down))/frac_total
        ff_qcdunc_up = ((frac_qcd*ff_qcd_corr*ffunc_qcd_up)+((frac_w+frac_dy+frac_st)*ff_w)+(frac_tt*ff_tt_corr))/frac_total
        ff_qcdunc_down = ((frac_qcd*ff_qcd_corr*ffunc_qcd_down)+((frac_w+frac_dy+frac_st)*ff_w)+(frac_tt*ff_tt_corr))/frac_total
        ff_wunc_up = ((frac_qcd*ff_qcd_corr)+((frac_w+frac_dy+frac_st)*ff_w*ffunc_w_up)+(frac_tt*ff_tt_corr))/frac_total
        ff_wunc_down = ((frac_qcd*ff_qcd_corr)+((frac_w+frac_dy+frac_st)*ff_w*ffunc_w_down)+(frac_tt*ff_tt_corr))/frac_total
        ff_ttunc_up = ((frac_qcd*ff_qcd_corr)+((frac_w+frac_dy+frac_st)*ff_w)+(frac_tt*ff_tt_corr*ffunc_tt_up))/frac_total
        ff_ttunc_down = ((frac_qcd*ff_qcd_corr)+((frac_w+frac_dy+frac_st)*ff_w)+(frac_tt*ff_tt_corr*ffunc_tt_down))/frac_total
        ff_qcdfitunc0_up = ((frac_qcd*ffcorr_qcd*ffunc_qcd_fitpar0_up)+((frac_w+frac_dy+frac_st)*ff_w)+(frac_tt*ff_tt_corr))/frac_total
        ff_qcdfitunc0_down = ((frac_qcd*ffcorr_qcd*ffunc_qcd_fitpar0_down)+((frac_w+frac_dy+frac_st)*ff_w)+(frac_tt*ff_tt_corr))/frac_total
        ff_qcdfitunc1_up = ((frac_qcd*ffcorr_qcd*ffunc_qcd_fitpar1_up)+((frac_w+frac_dy+frac_st)*ff_w)+(frac_tt*ff_tt_corr))/frac_total
        ff_qcdfitunc1_down = ((frac_qcd*ffcorr_qcd*ffunc_qcd_fitpar1_down)+((frac_w+frac_dy+frac_st)*ff_w)+(frac_tt*ff_tt_corr))/frac_total
        ff_wfitunc0_up = ((frac_qcd*ff_qcd_corr)+((frac_w+frac_dy+frac_st)*ffunc_w_fitpar0_up)+(frac_tt*ff_tt_corr))/frac_total
        ff_wfitunc0_down = ((frac_qcd*ff_qcd_corr)+((frac_w+frac_dy+frac_st)*ffunc_w_fitpar0_down)+(frac_tt*ff_tt_corr))/frac_total
        ff_wfitunc1_up = ((frac_qcd*ff_qcd_corr)+((frac_w+frac_dy+frac_st)*ffunc_w_fitpar1_up)+(frac_tt*ff_tt_corr))/frac_total
        ff_wfitunc1_down = ((frac_qcd*ff_qcd_corr)+((frac_w+frac_dy+frac_st)*ffunc_w_fitpar1_down)+(frac_tt*ff_tt_corr))/frac_total
        ff_wfitunc2_up = ((frac_qcd*ff_qcd_corr)+((frac_w+frac_dy+frac_st)*ffunc_w_fitpar2_up)+(frac_tt*ff_tt_corr))/frac_total
        ff_wfitunc2_down = ((frac_qcd*ff_qcd_corr)+((frac_w+frac_dy+frac_st)*ffunc_w_fitpar2_down)+(frac_tt*ff_tt_corr))/frac_total
        ff_ttfitunc0_up = ((frac_qcd*ff_qcd_corr)+((frac_w+frac_dy+frac_st)*ff_w)+(frac_tt*ffcorr_tt*ffunc_tt_fitpar0_up))/frac_total
        ff_ttfitunc0_down = ((frac_qcd*ff_qcd_corr)+((frac_w+frac_dy+frac_st)*ff_w)+(frac_tt*ffcorr_tt*ffunc_tt_fitpar0_down))/frac_total
        ff_ttfitunc1_up = ((frac_qcd*ff_qcd_corr)+((frac_w+frac_dy+frac_st)*ff_w)+(frac_tt*ffcorr_tt*ffunc_tt_fitpar1_up))/frac_total
        ff_ttfitunc1_down = ((frac_qcd*ff_qcd_corr)+((frac_w+frac_dy+frac_st)*ff_w)+(frac_tt*ffcorr_tt*ffunc_tt_fitpar1_down))/frac_total
        ff_frac_up = ((frac_qcd_up*ff_qcd_corr)+((frac_w_up+frac_dy_up+frac_st_up)*ff_w)+(frac_tt_up*ff_tt_corr))/frac_total_up
        ff_frac_down =  ((frac_qcd_down*ff_qcd_corr)+((frac_w_down+frac_dy_down+frac_st_down)*ff_w)+(frac_tt_down*ff_tt_corr))/frac_total_down
        return [[ff,ff_unc_up,ff_unc_down],[ff_qcdunc_up,ff_qcdunc_down,ff_wunc_up,ff_wunc_down,ff_ttunc_up,ff_ttunc_down],[[ff_qcdfitunc0_up,ff_qcdfitunc0_down,ff_qcdfitunc1_up,ff_qcdfitunc1_down],[ff_wfitunc0_up,ff_wfitunc0_down,ff_wfitunc1_up,ff_wfitunc1_down,ff_wfitunc2_up,ff_wfitunc2_down],[ff_ttfitunc0_up,ff_ttfitunc0_down,ff_ttfitunc1_up,ff_ttfitunc1_down]],[ff_frac_up,ff_frac_down]]





    def ffweight_sep(self,pt,decaymode,channel):
        if decaymode in [0,1,2]:
            prong="1prong"
        elif decaymode in [10,11]:
            prong="3prong"
        else:
            return 0.
        if channel=="mutau":
            if prong=="1prong":
                hist_ff_qcd = self.ff_mutau_qcd_1prong
                hist_ff_w = self.ff_mutau_w_1prong
                hist_ff_tt = self.ff_mutau_tt_1prong
                func_ff_qcd = self.ff_mutau_qcd_1prong.GetFunction("pol1")
                func_ff_qcd_flat = self.ff_mutau_qcd_flat_1prong.GetFunction("pol0")
                func_ff_w = self.ff_mutau_w_1prong.GetFunction("pol2")
                func_ff_tt = self.ff_mutau_tt_1prong.GetFunction("pol1")
            elif prong=="3prong":
                hist_ff_qcd = self.ff_mutau_qcd_3prong
                hist_ff_w = self.ff_mutau_w_3prong
                hist_ff_tt = self.ff_mutau_tt_3prong
                func_ff_qcd = self.ff_mutau_qcd_3prong.GetFunction("pol1")
                func_ff_qcd_flat = self.ff_mutau_qcd_flat_3prong.GetFunction("pol0")
                func_ff_w = self.ff_mutau_w_3prong.GetFunction("pol2")
                func_ff_tt = self.ff_mutau_tt_3prong.GetFunction("pol1")
        elif channel=="etau":
            if prong=="1prong":
                hist_ff_qcd = self.ff_etau_qcd_1prong
                hist_ff_w = self.ff_etau_w_1prong
                hist_ff_tt = self.ff_etau_tt_1prong
                func_ff_qcd = self.ff_etau_qcd_1prong.GetFunction("pol1")
                func_ff_qcd_flat = self.ff_etau_qcd_flat_1prong.GetFunction("pol0")
                func_ff_w = self.ff_etau_w_1prong.GetFunction("pol2")
                func_ff_tt = self.ff_etau_tt_1prong.GetFunction("pol1")
            elif prong=="3prong":
                hist_ff_qcd = self.ff_etau_qcd_3prong
                hist_ff_w = self.ff_etau_w_3prong
                hist_ff_tt = self.ff_etau_tt_3prong
                func_ff_qcd = self.ff_etau_qcd_3prong.GetFunction("pol1")
                func_ff_qcd_flat = self.ff_etau_qcd_flat_3prong.GetFunction("pol0")
                func_ff_w = self.ff_etau_w_3prong.GetFunction("pol2")
                func_ff_tt = self.ff_etau_tt_3prong.GetFunction("pol1")
        ff_qcd_old = self.getff(pt,hist_ff_qcd)
        ff_w_old = self.getff(pt,hist_ff_w)
        ff_tt_old = self.getff(pt,hist_ff_tt)
        cutvalue_qcd = cut_values[self.year][channel][prong]["qcd"]
        cutvalue_w  = cut_values[self.year][channel][prong]["w"]
        cutvalue_tt = cut_values[self.year][channel][prong]["tt"]
        ff_qcd = self.getff_fit(pt,func_ff_qcd,cutvalue_qcd)
        ff_qcd_flat = self.getff_fit(pt,func_ff_qcd_flat,130.)
        ff_w = self.getff_fit(pt,func_ff_w,cutvalue_w)
        ff_tt = self.getff_fit(pt,func_ff_tt,cutvalue_tt)
        return [ff_qcd,ff_w,ff_tt,ff_qcd_old,ff_w_old,ff_tt_old,ff_qcd_flat]
 

    def ffweightcorr_hmass(self,h_mass,decaymode,channel,DR):
        if decaymode in [0,1,2]:
            prong="1prong"
        elif decaymode in [10,11]:
            prong="3prong"
        else:
            return [1.,1.]
        if DR=='qcd':
            if channel=="mutau":
                if prong=="1prong":
                    hist_corr = self.hmass_mutau_qcd_1prong
                elif prong=="3prong":
                    hist_corr = self.hmass_mutau_qcd_3prong
            elif channel=="etau":
                if prong=="1prong":
                    hist_corr = self.hmass_etau_qcd_1prong
                elif prong=="3prong":
                    hist_corr = self.hmass_etau_qcd_3prong
        elif DR=='tt':
            if channel=="mutau":
                if prong=="1prong":
                    hist_corr = self.hmass_mutau_tt_1prong
                elif prong=="3prong":
                    hist_corr = self.hmass_mutau_tt_3prong
            elif channel=="etau":
                if prong=="1prong":
                    hist_corr = self.hmass_etau_tt_1prong
                elif prong=="3prong":
                    hist_corr = self.hmass_etau_tt_3prong
        ffcorr = self.getcorr(h_mass,hist_corr)
        return ffcorr


    def ffweightcorr_collinearmass(self,collinear_mass,decaymode,channel,DR):
        if decaymode in [0,1,2]:
            prong="1prong"
        elif decaymode in [10,11]:
            prong="3prong"
        else:
            return [1.,1.]
        if DR=='qcd':
            if channel=="mutau":
                if prong=="1prong":
                    hist_corr = self.collinearmass_mutau_qcd_1prong
                elif prong=="3prong":
                    hist_corr = self.collinearmass_mutau_qcd_3prong
            elif channel=="etau":
                if prong=="1prong":
                    hist_corr = self.collinearmass_etau_qcd_1prong
                elif prong=="3prong":
                    hist_corr = self.collinearmass_etau_qcd_3prong
        elif DR=='tt':
            if channel=="mutau":
                if prong=="1prong":
                    hist_corr = self.collinearmass_mutau_tt_1prong
                elif prong=="3prong":
                    hist_corr = self.collinearmass_mutau_tt_3prong
            elif channel=="etau":
                if prong=="1prong":
                    hist_corr = self.collinearmass_etau_tt_1prong
                elif prong=="3prong":
                    hist_corr = self.collinearmass_etau_tt_3prong
        ffcorr = self.getcorr(collinear_mass,hist_corr)
        return ffcorr

    def ffweightcorr_taujmass(self,tauj_mass,decaymode,channel,DR):
        if decaymode in [0,1,2]:
            prong="1prong"
        elif decaymode in [10,11]:
            prong="3prong"
        else:
            return [1.,1.]
        if DR=='qcd':
            if channel=="mutau":
                if prong=="1prong":
                    hist_corr = self.taujmass_mutau_qcd_1prong
                elif prong=="3prong":
                    hist_corr = self.taujmass_mutau_qcd_3prong
            elif channel=="etau":
                if prong=="1prong":
                    hist_corr = self.taujmass_etau_qcd_1prong
                elif prong=="3prong":
                    hist_corr = self.taujmass_etau_qcd_3prong
        elif DR=='tt':
            if channel=="mutau":
                if prong=="1prong":
                    hist_corr = self.taujmass_mutau_tt_1prong
                elif prong=="3prong":
                    hist_corr = self.taujmass_mutau_tt_3prong
            elif channel=="etau":
                if prong=="1prong":
                    hist_corr = self.taujmass_etau_tt_1prong
                elif prong=="3prong":
                    hist_corr = self.taujmass_etau_tt_3prong
        ffcorr = self.getcorr(tauj_mass,hist_corr)
        return ffcorr



    def ffweightcorr_jetpt(self,jetpt,decaymode,channel,DR):
        if decaymode in [0,1,2]:
            prong="1prong"
        elif decaymode in [10,11]:
            prong="3prong"
        else:
            return [1.,1.]
        if DR=='qcd':
            if channel=="mutau":
                if prong=="1prong":
                    hist_corr = self.jetpt_mutau_qcd_1prong
                elif prong=="3prong":
                    hist_corr = self.jetpt_mutau_qcd_3prong
            elif channel=="etau":
                if prong=="1prong":
                    hist_corr = self.jetpt_etau_qcd_1prong
                elif prong=="3prong":
                    hist_corr = self.jetpt_etau_qcd_3prong
        elif DR=='tt':
            if channel=="mutau":
                if prong=="1prong":
                    hist_corr = self.jetpt_mutau_tt_1prong
                elif prong=="3prong":
                    hist_corr = self.jetpt_mutau_tt_3prong
            elif channel=="etau":
                if prong=="1prong":
                    hist_corr = self.jetpt_etau_tt_1prong
                elif prong=="3prong":
                    hist_corr = self.jetpt_etau_tt_3prong
        ffcorr = self.getcorr(jetpt,hist_corr)
        return ffcorr
    

    def ffweight_ttdr(self,pt,decaymode,channel):
        if decaymode in [0,1,2]:
            prong="1prong"
        elif decaymode in [10,11]:
            prong="3prong"
        else:
            return 1.
        if channel=="mutau":
            if prong=="1prong":
                hist_ff_qcd = self.ff_mutau_qcd_1prong
                hist_ff_w = self.ff_mutau_w_1prong
                hist_ff_tt = self.ff_mutau_tt_1prong
                hist_ttfrac_qcd = self.ttfrac_mutau_1prong_qcd
                hist_ttfrac_w = self.ttfrac_mutau_1prong_w
                hist_ttfrac_dy = self.ttfrac_mutau_1prong_dy
                hist_ttfrac_tt = self.ttfrac_mutau_1prong_tt
                hist_ttfrac_st = self.ttfrac_mutau_1prong_st
            elif prong=="3prong":
                hist_ff_qcd = self.ff_mutau_qcd_3prong
                hist_ff_w = self.ff_mutau_w_3prong
                hist_ff_tt = self.ff_mutau_tt_3prong
                hist_ttfrac_qcd = self.ttfrac_mutau_3prong_qcd
                hist_ttfrac_w = self.ttfrac_mutau_3prong_w
                hist_ttfrac_dy = self.ttfrac_mutau_3prong_dy
                hist_ttfrac_tt = self.ttfrac_mutau_3prong_tt
                hist_ttfrac_st = self.ttfrac_mutau_3prong_st
        elif channel=="etau":
            if prong=="1prong":
                hist_ff_qcd = self.ff_etau_qcd_1prong
                hist_ff_w = self.ff_etau_w_1prong
                hist_ff_tt = self.ff_etau_tt_1prong
                hist_ttfrac_qcd = self.ttfrac_etau_1prong_qcd
                hist_ttfrac_w = self.ttfrac_etau_1prong_w
                hist_ttfrac_dy = self.ttfrac_etau_1prong_dy
                hist_ttfrac_tt = self.ttfrac_etau_1prong_tt
                hist_ttfrac_st = self.ttfrac_etau_1prong_st
            elif prong=="3prong":
                hist_ff_qcd = self.ff_etau_qcd_3prong
                hist_ff_w = self.ff_etau_w_3prong
                hist_ff_tt = self.ff_etau_tt_3prong
                hist_ttfrac_qcd = self.ttfrac_etau_3prong_qcd
                hist_ttfrac_w = self.ttfrac_etau_3prong_w
                hist_ttfrac_dy = self.ttfrac_etau_3prong_dy
                hist_ttfrac_tt = self.ttfrac_etau_3prong_tt
                hist_ttfrac_st = self.ttfrac_etau_3prong_st
        ff_qcd = self.getff(pt,hist_ff_qcd)
        ff_w = self.getff(pt,hist_ff_w)
        ff_tt = self.getff(pt,hist_ff_tt)
        ttfrac_qcd = hist_ttfrac_qcd.GetBinContent(hist_ttfrac_qcd.GetXaxis().FindBin(pt))
        ttfrac_w = hist_ttfrac_w.GetBinContent(hist_ttfrac_w.GetXaxis().FindBin(pt))
        ttfrac_dy = hist_ttfrac_dy.GetBinContent(hist_ttfrac_dy.GetXaxis().FindBin(pt))
        ttfrac_tt = hist_ttfrac_tt.GetBinContent(hist_ttfrac_tt.GetXaxis().FindBin(pt))
        ttfrac_st = hist_ttfrac_st.GetBinContent(hist_ttfrac_st.GetXaxis().FindBin(pt))
        return ((ttfrac_qcd*ff_qcd)+((ttfrac_w+ttfrac_dy+ttfrac_st)*ff_w)+(ttfrac_tt*ff_tt))/(ttfrac_qcd+ttfrac_w+ttfrac_dy+ttfrac_st+ttfrac_tt)
    
    def ffweight_qcddr(self,pt,hmass,jetpt,collinearmass,taujmass,decaymode,channel):
        if decaymode in [0,1,2]:
            prong="1prong"
        elif decaymode in [10,11]:
            prong="3prong"
        else:
            return 0.
        if channel=="mutau":
            if prong=="1prong":
                func_ff_qcd = self.ff_mutau_qcd_1prong.GetFunction("pol1")
                func_ff_w = self.ff_mutau_w_1prong.GetFunction("pol2")
                func_ff_tt = self.ff_mutau_tt_1prong.GetFunction("pol1")
                hist_qcdfrac_qcd = self.qcdfrac_mutau_1prong_qcd
                hist_qcdfrac_w = self.qcdfrac_mutau_1prong_w
                hist_qcdfrac_dy = self.qcdfrac_mutau_1prong_dy
                hist_qcdfrac_tt = self.qcdfrac_mutau_1prong_tt
                hist_qcdfrac_st = self.qcdfrac_mutau_1prong_st
            elif prong=="3prong":
                func_ff_qcd = self.ff_mutau_qcd_3prong.GetFunction("pol1")
                func_ff_w = self.ff_mutau_w_3prong.GetFunction("pol2")
                func_ff_tt = self.ff_mutau_tt_3prong.GetFunction("pol1")
                hist_qcdfrac_qcd = self.qcdfrac_mutau_3prong_qcd
                hist_qcdfrac_w = self.qcdfrac_mutau_3prong_w
                hist_qcdfrac_dy = self.qcdfrac_mutau_3prong_dy
                hist_qcdfrac_tt = self.qcdfrac_mutau_3prong_tt
                hist_qcdfrac_st = self.qcdfrac_mutau_3prong_st
        elif channel=="etau":
            if prong=="1prong":
                func_ff_qcd = self.ff_etau_qcd_1prong.GetFunction("pol1")
                func_ff_w = self.ff_etau_w_1prong.GetFunction("pol2")
                func_ff_tt = self.ff_etau_tt_1prong.GetFunction("pol1")
                hist_qcdfrac_qcd = self.qcdfrac_etau_1prong_qcd
                hist_qcdfrac_w = self.qcdfrac_etau_1prong_w
                hist_qcdfrac_dy = self.qcdfrac_etau_1prong_dy
                hist_qcdfrac_tt = self.qcdfrac_etau_1prong_tt
                hist_qcdfrac_st = self.qcdfrac_etau_1prong_st
            elif prong=="3prong":
                func_ff_qcd = self.ff_etau_qcd_3prong.GetFunction("pol1")
                func_ff_w = self.ff_etau_w_3prong.GetFunction("pol2")
                func_ff_tt = self.ff_etau_tt_3prong.GetFunction("pol1")
                hist_qcdfrac_qcd = self.qcdfrac_etau_3prong_qcd
                hist_qcdfrac_w = self.qcdfrac_etau_3prong_w
                hist_qcdfrac_dy = self.qcdfrac_etau_3prong_dy
                hist_qcdfrac_tt = self.qcdfrac_etau_3prong_tt
                hist_qcdfrac_st = self.qcdfrac_etau_3prong_st
        cutvalue_qcd = cut_values[self.year][channel][prong]["qcd"]
        cutvalue_w  = cut_values[self.year][channel][prong]["w"]
        cutvalue_tt = cut_values[self.year][channel][prong]["tt"]       
        ff_qcd = self.getff_fit(pt,func_ff_qcd,cutvalue_qcd)
        ff_w = self.getff_fit(pt,func_ff_w,cutvalue_w)
        ff_tt = self.getff_fit(pt,func_ff_tt,cutvalue_tt)
        qcdfrac_qcd = hist_qcdfrac_qcd.GetBinContent(hist_qcdfrac_qcd.GetXaxis().FindBin(pt))
        qcdfrac_w = hist_qcdfrac_w.GetBinContent(hist_qcdfrac_w.GetXaxis().FindBin(pt))
        qcdfrac_dy = hist_qcdfrac_dy.GetBinContent(hist_qcdfrac_dy.GetXaxis().FindBin(pt))
        qcdfrac_tt = hist_qcdfrac_tt.GetBinContent(hist_qcdfrac_tt.GetXaxis().FindBin(pt))
        qcdfrac_st = hist_qcdfrac_st.GetBinContent(hist_qcdfrac_st.GetXaxis().FindBin(pt))
        ffcorr_hmass_qcd = self.ffweightcorr_hmass(hmass,decaymode,channel,'qcd')
        ffcorr_jetpt_qcd = self.ffweightcorr_jetpt(jetpt,decaymode,channel,'qcd')
        ffcorr_collinearmass_qcd = self.ffweightcorr_collinearmass(collinearmass,decaymode,channel,'qcd')
        ffcorr_taujmass_qcd = self.ffweightcorr_taujmass(taujmass,decaymode,channel,'qcd')
        ffcorr_qcd = ffcorr_hmass_qcd * ffcorr_jetpt_qcd * ffcorr_collinearmass_qcd * ffcorr_taujmass_qcd
        return ((qcdfrac_qcd*ff_qcd*ffcorr_qcd)+((qcdfrac_w+qcdfrac_dy+qcdfrac_st)*ff_w)+(qcdfrac_tt*ff_tt))/(qcdfrac_qcd+qcdfrac_w+qcdfrac_dy+qcdfrac_st+qcdfrac_tt)



if __name__== "__main__":
    #ffclass(2018).ffweight_ttdr(75,10)
    #for hmass in range(130,250):
    #    print(ffclass(2017).ffweightcorr_hmass(hmass,1,"etau"))
    """
    for pt in [35.,45.,55.,65.,75.,85.,95.,105.,115.,125.,135.]:
        Mu1_pt = 40.
        H_mass = 120.
        Jet1_pt = 50.
        Jet2_pt = 60.
        MET = 40.
        Tau1_decaymode = 0
        #print("ffweight for pt:",pt,"is:",ffclass(2018).ffweight_corr(pt,Mu1_pt,H_mass,Jet1_pt,Jet2_pt,MET,Tau1_decaymode,"mutau"))
        #print(ffclass(2018).ffweight(pt,1,"etau"))
        #print(ffclass(2018).ffweight_sep(pt,1,"etau"))
        #print(ffclass(2018).ffweightcorr_leppt(40.,10,pt,"mutau"))
        #print(ffclass(2018).ffweight_corr(pt,60.,120.,50.,70.,100.,1,"mutau"))
        #ff_etau_file = TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fakefactors_etau_UL2017.root",'READ')
        #ff_etau_qcd_1prong = ff_etau_file.Get("ff_qcd_1prong")
        #ff_etau_qcd_1prong.SetDirectory(0)
        #ff_etau_file.Close()
        print("pt:",pt, "frac:",hist_frac_qcd.GetBinContent(hist_frac_qcd.GetXaxis().FindBin(pt)))
        print("pt:",pt, "frac old:",hist_frac_qcd_old.GetBinContent(hist_frac_qcd.GetXaxis().FindBin(pt)))
       

        #func_ff_qcd = ff_etau_qcd_1prong.GetFunction("pol1")
        #cutvalue_qcd = cut_values["UL2017"]["etau"]["1prong"]["qcd"]
    """
    
