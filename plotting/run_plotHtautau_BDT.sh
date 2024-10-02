python3 plotHtautau.py -y 2018 -c mutau -b
python3 plotHtautau.py -y 2018 -c etau -b
python3 plotHtautau.py -y 2017 -c mutau -b
python3 plotHtautau.py -y 2017 -c etau -b
python3 plotHtautau.py -y 2016 -c mutau -t -b
python3 plotHtautau.py -y 2016 -c etau -t -b
python3 makePlots.py -i mutau_UL2018_BDT.root
python3 makePlots.py -i etau_UL2018_BDT.root
python3 makePlots.py -i mutau_UL2017_BDT.root
python3 makePlots.py -i etau_UL2017_BDT.root
python3 makePlots.py -i mutau_UL2016_comb_BDT.root
python3 makePlots.py -i etau_UL2016_comb_BDT.root
