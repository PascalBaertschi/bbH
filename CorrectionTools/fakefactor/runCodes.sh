python3 ff_selection.py -y 2018 -c mutau
python3 draw_fractions.py -i ff_mutau_UL2018.root
python3 ff_derive.py -i ff_mutau_UL2018.root
python3 makePlots.py -i ff_mutau_UL2018.root
python3 ff_selection.py -y 2018 -c etau
python3 draw_fractions.py -i ff_etau_UL2018.root
python3 ff_derive.py -i ff_etau_UL2018.root
python3 makePlots.py -i ff_etau_UL2018.root
python3 ff_selection.py -y 2017 -c mutau
python3 draw_fractions.py -i ff_mutau_UL2017.root
python3 ff_derive.py -i ff_mutau_UL2017.root
python3 makePlots.py -i ff_mutau_UL2017.root
python3 ff_selection.py -y 2017 -c etau
python3 draw_fractions.py -i ff_etau_UL2017.root
python3 ff_derive.py -i ff_etau_UL2017.root
python3 makePlots.py -i ff_etau_UL2017.root
python3 ff_selection.py -y 2016 -c mutau
python3 draw_fractions.py -i ff_mutau_UL2016.root
python3 ff_derive.py -i ff_mutau_UL2016.root
python3 makePlots.py -i ff_mutau_UL2016.root
python3 ff_selection.py -y 2016 -c etau
python3 draw_fractions.py -i ff_etau_UL2016.root
python3 ff_derive.py -i ff_etau_UL2016.root
python3 makePlots.py -i ff_etau_UL2016.root
python3 ff_varcheck.py -y 2018 -c mutau
python3 ffvarcheck_derive.py -i ffvarcheck_mutau_UL2018.root
python3 ff_varcheck.py -y 2018 -c etau
python3 ffvarcheck_derive.py -i ffvarcheck_etau_UL2018.root
python3 ff_varcheck.py -y 2017 -c mutau
python3 ffvarcheck_derive.py -i ffvarcheck_mutau_UL2017.root
python3 ff_varcheck.py -y 2017 -c etau
python3 ffvarcheck_derive.py -i ffvarcheck_etau_UL2017.root
python3 ff_varcheck.py -y 2016 -c mutau
python3 ffvarcheck_derive.py -i ffvarcheck_mutau_UL2016.root
python3 ff_varcheck.py -y 2016 -c etau
python3 ffvarcheck_derive.py -i ffvarcheck_etau_UL2016.root
python3 ff_CRcheck.py -y 2018 -c mutau
python3 ffCRcheck_derive.py -i ffCRcheck_mutau_UL2018.root
python3 ff_CRcheck.py -y 2018 -c etau
python3 ffCRcheck_derive.py -i ffCRcheck_etau_UL2018.root
python3 ff_CRcheck.py -y 2017 -c mutau
python3 ffCRcheck_derive.py -i ffCRcheck_mutau_UL2017.root
python3 ff_CRcheck.py -y 2017 -c etau
python3 ffCRcheck_derive.py -i ffCRcheck_etau_UL2017.root
python3 ff_CRcheck.py -y 2016 -c mutau
python3 ffCRcheck_derive.py -i ffCRcheck_mutau_UL2016.root
python3 ff_CRcheck.py -y 2016 -c etau
python3 ffCRcheck_derive.py -i ffCRcheck_etau_UL2016.root
