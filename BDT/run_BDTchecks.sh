python3 BDT_check.py -y 2017 -c etau -t
python3 BDT_check.py -y 2016 -c etau -t
python3 BDT_check.py -y 2017 -c etau -p
python3 BDT_check.py -y 2016 -c etau -p
cd ../plotting
python3 plotHtautau.py -y 2017 -c etau -b
python3 plotHtautau.py -y 2016 -c etau -t -b
cd ../BDT
