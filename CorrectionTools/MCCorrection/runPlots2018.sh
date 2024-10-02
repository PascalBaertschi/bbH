#python3 mc_corr.py -y 2018 -c tt
#python3 makePlots_mccorr.py -i tt_UL2018.root
#python3 mccorr_derive.py -i tt_UL2018.root
#python3 mc_corr.py -y 2018 -c mumu
#python3 makePlots_mccorr.py -i mumu_UL2018.root
#python3 mccorr_derive.py -i mumu_UL2018.root
python3 mc_corr.py -y 2018 -c mutau
python3 makePlots_mccorr.py -i mutau_UL2018.root
python3 mccorr_derive.py -i mutau_UL2018.root
python3 mc_corr.py -y 2018 -c etau
python3 makePlots_mccorr.py -i etau_UL2018.root
python3 mccorr_derive.py -i etau_UL2018.root

