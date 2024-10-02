# BDT
Boosted Decision Tree to classify signal TT and DY+jets background

The inputs for the BDT are made using
```
python makeInputs.py -y YEAR -u -c CHANNEL
```

The BDT can be trained running

```
python BDT.py -y YEAR -u -t -c CHANNEL
```

and once trained the predictions are made running

```
python BDT.py -y YEAR -u -p -c CHANNEL
```