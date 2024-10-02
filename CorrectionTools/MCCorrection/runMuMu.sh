python3 mc_corr.py -y 2018 -c mumu
python3 mccorr_derive.py -i mumu_UL2018.root
python3 makePlots_mccorr.py -i mumu_UL2018.root
python3 mc_corr.py -y 2017 -c mumu
python3 mccorr_derive.py -i mumu_UL2017.root
python3 makePlots_mccorr.py -i mumu_UL2017.root
python3 mc_corr.py -y 2016 -c mumu
python3 mccorr_derive.py -i mumu_UL2016.root
python3 makePlots_mccorr.py -i mumu_UL2016.root
