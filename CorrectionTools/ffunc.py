import ROOT
from ROOT import TFile


class ffuncclass:
    def __init__(self,year):
        ROOT.gInterpreter.Declare("TF1* recast(const char *path, const char *funcname) { return (TF1 *) TFile(path).Get(funcname);}")
        ## fit uncertainties mutau ##
        path = "/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fakefactors_mutau_UL%s.root"%year
        self.ff_mutau_qcd_1prong_par0_up = ROOT.recast(path,"qcd_func_1prong_par0_up")
        self.ff_mutau_qcd_1prong_par0_down = ROOT.recast(path,"qcd_func_1prong_par0_down")
        self.ff_mutau_qcd_1prong_par1_up = ROOT.recast(path,"qcd_func_1prong_par1_up")
        self.ff_mutau_qcd_1prong_par1_down = ROOT.recast(path,"qcd_func_1prong_par1_down")
        self.ff_mutau_w_1prong_par0_up = ROOT.recast(path,"w_func_1prong_par0_up")
        self.ff_mutau_w_1prong_par0_down = ROOT.recast(path,"w_func_1prong_par0_down")
        self.ff_mutau_w_1prong_par1_up = ROOT.recast(path,"w_func_1prong_par1_up")
        self.ff_mutau_w_1prong_par1_down = ROOT.recast(path,"w_func_1prong_par1_down")
        self.ff_mutau_w_1prong_par2_up = ROOT.recast(path,"w_func_1prong_par2_up")
        self.ff_mutau_w_1prong_par2_down = ROOT.recast(path,"w_func_1prong_par2_down")
        self.ff_mutau_tt_1prong_par0_up = ROOT.recast(path,"tt_func_1prong_par0_up")
        self.ff_mutau_tt_1prong_par0_down = ROOT.recast(path,"tt_func_1prong_par0_down")
        self.ff_mutau_tt_1prong_par1_up = ROOT.recast(path,"tt_func_1prong_par1_up")
        self.ff_mutau_tt_1prong_par1_down = ROOT.recast(path,"tt_func_1prong_par1_down")
        self.ff_mutau_qcd_3prong_par0_up = ROOT.recast(path,"qcd_func_3prong_par0_up")
        self.ff_mutau_qcd_3prong_par0_down = ROOT.recast(path,"qcd_func_3prong_par0_down")
        self.ff_mutau_qcd_3prong_par1_up = ROOT.recast(path,"qcd_func_3prong_par1_up")
        self.ff_mutau_qcd_3prong_par1_down = ROOT.recast(path,"qcd_func_3prong_par1_down")
        self.ff_mutau_w_3prong_par0_up = ROOT.recast(path,"w_func_3prong_par0_up")
        self.ff_mutau_w_3prong_par0_down = ROOT.recast(path,"w_func_3prong_par0_down")
        self.ff_mutau_w_3prong_par1_up = ROOT.recast(path,"w_func_3prong_par1_up")
        self.ff_mutau_w_3prong_par1_down = ROOT.recast(path,"w_func_3prong_par1_down")
        self.ff_mutau_w_3prong_par2_up = ROOT.recast(path,"w_func_3prong_par2_up")
        self.ff_mutau_w_3prong_par2_down = ROOT.recast(path,"w_func_3prong_par2_down")
        self.ff_mutau_tt_3prong_par0_up = ROOT.recast(path,"tt_func_3prong_par0_up")
        self.ff_mutau_tt_3prong_par0_down = ROOT.recast(path,"tt_func_3prong_par0_down")
        self.ff_mutau_tt_3prong_par1_up = ROOT.recast(path,"tt_func_3prong_par1_up")
        self.ff_mutau_tt_3prong_par1_down = ROOT.recast(path,"tt_func_3prong_par1_down")
        ffunc_mutau_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/ffuncertainties_mutau_UL%s.root"%year,'READ')
        self.ffunc_mutau_qcd_1prong = ffunc_mutau_file.Get("ff_qcd_1prong")
        self.ffunc_mutau_w_1prong = ffunc_mutau_file.Get("ff_w_1prong")
        self.ffunc_mutau_tt_1prong = ffunc_mutau_file.Get("ff_tt_1prong")
        self.ffunc_mutau_qcd_3prong = ffunc_mutau_file.Get("ff_qcd_3prong")
        self.ffunc_mutau_w_3prong = ffunc_mutau_file.Get("ff_w_3prong")
        self.ffunc_mutau_tt_3prong = ffunc_mutau_file.Get("ff_tt_3prong")
        self.ffunc_mutau_qcd_1prong.SetDirectory(0)
        self.ffunc_mutau_w_1prong.SetDirectory(0)
        self.ffunc_mutau_tt_1prong.SetDirectory(0)
        self.ffunc_mutau_qcd_3prong.SetDirectory(0)
        self.ffunc_mutau_w_3prong.SetDirectory(0)
        self.ffunc_mutau_tt_3prong.SetDirectory(0)
        ffunc_mutau_file.Close()
        ## fit uncertainties etau ##
        path = "/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fakefactors_etau_UL%s.root"%year
        self.ff_etau_qcd_1prong_par0_up = ROOT.recast(path,"qcd_func_1prong_par0_up")
        self.ff_etau_qcd_1prong_par0_down = ROOT.recast(path,"qcd_func_1prong_par0_down")
        self.ff_etau_qcd_1prong_par1_up = ROOT.recast(path,"qcd_func_1prong_par1_up")
        self.ff_etau_qcd_1prong_par1_down = ROOT.recast(path,"qcd_func_1prong_par1_down")
        self.ff_etau_w_1prong_par0_up = ROOT.recast(path,"w_func_1prong_par0_up")
        self.ff_etau_w_1prong_par0_down = ROOT.recast(path,"w_func_1prong_par0_down")
        self.ff_etau_w_1prong_par1_up = ROOT.recast(path,"w_func_1prong_par1_up")
        self.ff_etau_w_1prong_par1_down = ROOT.recast(path,"w_func_1prong_par1_down")
        self.ff_etau_w_1prong_par2_up = ROOT.recast(path,"w_func_1prong_par2_up")
        self.ff_etau_w_1prong_par2_down = ROOT.recast(path,"w_func_1prong_par2_down")
        self.ff_etau_tt_1prong_par0_up = ROOT.recast(path,"tt_func_1prong_par0_up")
        self.ff_etau_tt_1prong_par0_down = ROOT.recast(path,"tt_func_1prong_par0_down")
        self.ff_etau_tt_1prong_par1_up = ROOT.recast(path,"tt_func_1prong_par1_up")
        self.ff_etau_tt_1prong_par1_down = ROOT.recast(path,"tt_func_1prong_par1_down")
        self.ff_etau_qcd_3prong_par0_up = ROOT.recast(path,"qcd_func_3prong_par0_up")
        self.ff_etau_qcd_3prong_par0_down = ROOT.recast(path,"qcd_func_3prong_par0_down")
        self.ff_etau_qcd_3prong_par1_up = ROOT.recast(path,"qcd_func_3prong_par1_up")
        self.ff_etau_qcd_3prong_par1_down = ROOT.recast(path,"qcd_func_3prong_par1_down")
        self.ff_etau_w_3prong_par0_up = ROOT.recast(path,"w_func_3prong_par0_up")
        self.ff_etau_w_3prong_par0_down = ROOT.recast(path,"w_func_3prong_par0_down")
        self.ff_etau_w_3prong_par1_up = ROOT.recast(path,"w_func_3prong_par1_up")
        self.ff_etau_w_3prong_par1_down = ROOT.recast(path,"w_func_3prong_par1_down")
        self.ff_etau_w_3prong_par2_up = ROOT.recast(path,"w_func_3prong_par2_up")
        self.ff_etau_w_3prong_par2_down = ROOT.recast(path,"w_func_3prong_par2_down")
        self.ff_etau_tt_3prong_par0_up = ROOT.recast(path,"tt_func_3prong_par0_up")
        self.ff_etau_tt_3prong_par0_down = ROOT.recast(path,"tt_func_3prong_par0_down")
        self.ff_etau_tt_3prong_par1_up = ROOT.recast(path,"tt_func_3prong_par1_up")
        self.ff_etau_tt_3prong_par1_down = ROOT.recast(path,"tt_func_3prong_par1_down")
        ffunc_etau_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/ffuncertainties_etau_UL%s.root"%year,'READ')
        self.ffunc_etau_qcd_1prong = ffunc_etau_file.Get("ff_qcd_1prong")
        self.ffunc_etau_w_1prong = ffunc_etau_file.Get("ff_w_1prong")
        self.ffunc_etau_tt_1prong = ffunc_etau_file.Get("ff_tt_1prong")
        self.ffunc_etau_qcd_3prong = ffunc_etau_file.Get("ff_qcd_3prong")
        self.ffunc_etau_w_3prong = ffunc_etau_file.Get("ff_w_3prong")
        self.ffunc_etau_tt_3prong = ffunc_etau_file.Get("ff_tt_3prong")
        self.ffunc_etau_qcd_1prong.SetDirectory(0)
        self.ffunc_etau_w_1prong.SetDirectory(0)
        self.ffunc_etau_tt_1prong.SetDirectory(0)
        self.ffunc_etau_qcd_3prong.SetDirectory(0)
        self.ffunc_etau_w_3prong.SetDirectory(0)
        self.ffunc_etau_tt_3prong.SetDirectory(0)
        ffunc_etau_file.Close()

    def getffunc(self,pt,hist):
        return abs(hist.GetBinContent(hist.GetXaxis().FindBin(pt))-1.)
        

    def ffuncertainty(self,pt,decaymode,channel):
        if channel=="mutau":
            if decaymode in [0,1,2]:
                hist_ffunc_qcd = self.ffunc_mutau_qcd_1prong
                hist_ffunc_w = self.ffunc_mutau_w_1prong
                hist_ffunc_tt = self.ffunc_mutau_tt_1prong
            elif decaymode in [10,11]:
                hist_ffunc_qcd = self.ffunc_mutau_qcd_3prong
                hist_ffunc_w = self.ffunc_mutau_w_3prong
                hist_ffunc_tt = self.ffunc_mutau_tt_3prong
        elif channel=="etau":
            if decaymode in [0,1,2]:
                hist_ffunc_qcd = self.ffunc_etau_qcd_1prong
                hist_ffunc_w = self.ffunc_etau_w_1prong
                hist_ffunc_tt = self.ffunc_etau_tt_1prong
            elif decaymode in [10,11]:
                hist_ffunc_qcd = self.ffunc_etau_qcd_3prong
                hist_ffunc_w = self.ffunc_etau_w_3prong
                hist_ffunc_tt = self.ffunc_etau_tt_3prong
 
        ffunc_qcd = self.getffunc(pt,hist_ffunc_qcd)
        ffunc_w = self.getffunc(pt,hist_ffunc_w)
        ffunc_tt = self.getffunc(pt,hist_ffunc_tt)
        ffunc_qcd_up = 1. + ffunc_qcd
        ffunc_qcd_down = 1. - ffunc_qcd
        ffunc_w_up = 1. + ffunc_w
        ffunc_w_down = 1. - ffunc_w
        ffunc_tt_up = 1. + ffunc_tt
        ffunc_tt_down = 1. - ffunc_tt
        return [ffunc_qcd,ffunc_w,ffunc_tt,ffunc_qcd_up,ffunc_qcd_down,ffunc_w_up,ffunc_w_down,ffunc_tt_up,ffunc_tt_down]

    def ff_fitunc(self,decaymode,channel,pt):
        if channel=="mutau":
            if decaymode in [0,1,2]:
                ffunc_qcd_fitpar0_up = max(0.,self.ff_mutau_qcd_1prong_par0_up.Eval(pt))
                ffunc_qcd_fitpar0_down = max(0.,self.ff_mutau_qcd_1prong_par0_down.Eval(pt))
                ffunc_qcd_fitpar1_up = max(0.,self.ff_mutau_qcd_1prong_par1_up.Eval(pt))
                ffunc_qcd_fitpar1_down = max(0.,self.ff_mutau_qcd_1prong_par1_down.Eval(pt))
                ffunc_w_fitpar0_up = max(0.,self.ff_mutau_w_1prong_par0_up.Eval(pt))
                ffunc_w_fitpar0_down = max(0.,self.ff_mutau_w_1prong_par0_down.Eval(pt))
                ffunc_w_fitpar1_up = max(0.,self.ff_mutau_w_1prong_par1_up.Eval(pt))
                ffunc_w_fitpar1_down = max(0.,self.ff_mutau_w_1prong_par1_down.Eval(pt))
                ffunc_w_fitpar2_up = max(0.,self.ff_mutau_w_1prong_par2_up.Eval(pt))
                ffunc_w_fitpar2_down = max(0.,self.ff_mutau_w_1prong_par2_down.Eval(pt))
                ffunc_tt_fitpar0_up = max(0.,self.ff_mutau_tt_1prong_par0_up.Eval(pt))
                ffunc_tt_fitpar0_down = max(0.,self.ff_mutau_tt_1prong_par0_down.Eval(pt))
                ffunc_tt_fitpar1_up = max(0.,self.ff_mutau_tt_1prong_par1_up.Eval(pt))
                ffunc_tt_fitpar1_down = max(0.,self.ff_mutau_tt_1prong_par1_down.Eval(pt))
            elif decaymode in [10,11]:
                ffunc_qcd_fitpar0_up = max(0.,self.ff_mutau_qcd_3prong_par0_up.Eval(pt))
                ffunc_qcd_fitpar0_down = max(0.,self.ff_mutau_qcd_3prong_par0_down.Eval(pt))
                ffunc_qcd_fitpar1_up = max(0.,self.ff_mutau_qcd_3prong_par1_up.Eval(pt))
                ffunc_qcd_fitpar1_down = max(0.,self.ff_mutau_qcd_3prong_par1_down.Eval(pt))
                ffunc_w_fitpar0_up = max(0.,self.ff_mutau_w_3prong_par0_up.Eval(pt))
                ffunc_w_fitpar0_down = max(0.,self.ff_mutau_w_3prong_par0_down.Eval(pt))
                ffunc_w_fitpar1_up = max(0.,self.ff_mutau_w_3prong_par1_up.Eval(pt))
                ffunc_w_fitpar1_down = max(0.,self.ff_mutau_w_3prong_par1_down.Eval(pt))
                ffunc_w_fitpar2_up = max(0.,self.ff_mutau_w_3prong_par2_up.Eval(pt))
                ffunc_w_fitpar2_down = max(0.,self.ff_mutau_w_3prong_par2_down.Eval(pt))
                ffunc_tt_fitpar0_up = max(0.,self.ff_mutau_tt_3prong_par0_up.Eval(pt))
                ffunc_tt_fitpar0_down = max(0.,self.ff_mutau_tt_3prong_par0_down.Eval(pt))
                ffunc_tt_fitpar1_up = max(0.,self.ff_mutau_tt_3prong_par1_up.Eval(pt))
                ffunc_tt_fitpar1_down = max(0.,self.ff_mutau_tt_3prong_par1_down.Eval(pt))
        elif channel=="etau":
            if decaymode in [0,1,2]:
                ffunc_qcd_fitpar0_up = max(0.,self.ff_etau_qcd_1prong_par0_up.Eval(pt))
                ffunc_qcd_fitpar0_down = max(0.,self.ff_etau_qcd_1prong_par0_down.Eval(pt))
                ffunc_qcd_fitpar1_up = max(0.,self.ff_etau_qcd_1prong_par1_up.Eval(pt))
                ffunc_qcd_fitpar1_down = max(0.,self.ff_etau_qcd_1prong_par1_down.Eval(pt))
                ffunc_w_fitpar0_up = max(0.,self.ff_etau_w_1prong_par0_up.Eval(pt))
                ffunc_w_fitpar0_down = max(0.,self.ff_etau_w_1prong_par0_down.Eval(pt))
                ffunc_w_fitpar1_up = max(0.,self.ff_etau_w_1prong_par1_up.Eval(pt))
                ffunc_w_fitpar1_down = max(0.,self.ff_etau_w_1prong_par1_down.Eval(pt))
                ffunc_w_fitpar2_up = max(0.,self.ff_etau_w_1prong_par2_up.Eval(pt))
                ffunc_w_fitpar2_down = max(0.,self.ff_etau_w_1prong_par2_down.Eval(pt))
                ffunc_tt_fitpar0_up = max(0.,self.ff_etau_tt_1prong_par0_up.Eval(pt))
                ffunc_tt_fitpar0_down = max(0.,self.ff_etau_tt_1prong_par0_down.Eval(pt))
                ffunc_tt_fitpar1_up = max(0.,self.ff_etau_tt_1prong_par1_up.Eval(pt))
                ffunc_tt_fitpar1_down = max(0.,self.ff_etau_tt_1prong_par1_down.Eval(pt))
            elif decaymode in [10,11]:
                ffunc_qcd_fitpar0_up = max(0.,self.ff_etau_qcd_3prong_par0_up.Eval(pt))
                ffunc_qcd_fitpar0_down = max(0.,self.ff_etau_qcd_3prong_par0_down.Eval(pt))
                ffunc_qcd_fitpar1_up = max(0.,self.ff_etau_qcd_3prong_par1_up.Eval(pt))
                ffunc_qcd_fitpar1_down = max(0.,self.ff_etau_qcd_3prong_par1_down.Eval(pt))
                ffunc_w_fitpar0_up = max(0.,self.ff_etau_w_3prong_par0_up.Eval(pt))
                ffunc_w_fitpar0_down = max(0.,self.ff_etau_w_3prong_par0_down.Eval(pt))
                ffunc_w_fitpar1_up = max(0.,self.ff_etau_w_3prong_par1_up.Eval(pt))
                ffunc_w_fitpar1_down = max(0.,self.ff_etau_w_3prong_par1_down.Eval(pt))
                ffunc_w_fitpar2_up = max(0.,self.ff_etau_w_3prong_par2_up.Eval(pt))
                ffunc_w_fitpar2_down = max(0.,self.ff_etau_w_3prong_par2_down.Eval(pt))
                ffunc_tt_fitpar0_up = max(0.,self.ff_etau_tt_3prong_par0_up.Eval(pt))
                ffunc_tt_fitpar0_down = max(0.,self.ff_etau_tt_3prong_par0_down.Eval(pt))
                ffunc_tt_fitpar1_up = max(0.,self.ff_etau_tt_3prong_par1_up.Eval(pt))
                ffunc_tt_fitpar1_down = max(0.,self.ff_etau_tt_3prong_par1_down.Eval(pt))
        
        return [[ffunc_qcd_fitpar0_up,ffunc_qcd_fitpar0_down,ffunc_qcd_fitpar1_up,ffunc_qcd_fitpar1_down],[ffunc_w_fitpar0_up,ffunc_w_fitpar0_down,ffunc_w_fitpar1_up,ffunc_w_fitpar1_down,ffunc_w_fitpar2_up,ffunc_w_fitpar2_down],[ffunc_tt_fitpar0_up,ffunc_tt_fitpar0_down,ffunc_tt_fitpar1_up,ffunc_tt_fitpar1_down]]

if __name__== "__main__":
    #print ffclass(2018).ff_fitunc(1,"mutau")
    for pt in range(30,130):
        print("ffweight for pt:",pt,"is:",)
        print(ffuncclass(2018).ffuncertainty(pt,1,"mutau"))
