python3 mc_corr.py -y 2016 -c mutau
python3 btagSFcorr_derive.py -i mutau_UL2016.root
python3 mc_corr.py -y 2016 -c etau
python3 btagSFcorr_derive.py -i etau_UL2016.root
python3 mc_corr.py -y 2016 -c tt
python3 btagSFcorr_derive.py -i tt_UL2016.root
python3 mc_corr.py -y 2016 -c mumu
python3 btagSFcorr_derive.py -i mumu_UL2016.root

