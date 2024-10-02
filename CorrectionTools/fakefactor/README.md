# Fakefactor Tools


## Fakefactors
Fakefactors are derived running
```
python3 ff_selection.py -y YEAR -c CHANNEL
python3 ff_derive.py -i ff_CHANNEL_ULYEAR.root
```
Plots can be made using
```
python3 makePlots.py -i ff_CHANNEL_ULYEAR.root
```

If the selection changed the background contributions in the AR need to be updated:
```
python3 draw_fractions.py -i ff_CHANNEL_ULYEAR.root
```


## FF Corrections
The fakefactors are derived as function of tau pt, therefore corrections need to be applied as function of other important variables.
The corrections are derived running
```
python3 ff_varcheck.py -y YEAR -c CHANNEl
python3 ffvarcheck_derive.py -i ffvarcheck_CHANNEL_ULYEAR.root
```
The samples should be rerun after a new correction is derived, because it will influence other variables as well. Instead of rerunning the samples the fakefactor can be rederived with ``addWeight.py``.
The code can also be run on the slurm batch system with 
```
python3 submit.py -y YEAR 
```
Only the DY+Jets, W+Jets, TT and ST samples are run. Effect of VV is negligible. The new variables are called ``wt_ffvarcorr_...`` (in the standard processing they are called ``wt_ffcorr_...``) and are saved in the SE at ffvarcorr. Before deriving more corrections make sure that in ``ff_varcheck.py`` the correct samples are used as inputs. 


## FF uncertainties
The uncertainties for the fakefactors are derived using a Control Region. The uncertainties are derived running
```
python3 ff_CRcheck.py -y YEAR -c CHANNEL
python3 -i ffCRcheck_derive.py -i ffCRcheck_CHANNEL_ULYEAR.root
```