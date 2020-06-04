#! /bin/bash

for ene in {680..700}; do
    cfg=`jq ".energy = $ene" .exp.json`
    python main.py ~/Data/Meshot/IL_CNT_MD/BMIM_FAP/26_26/IL_CNT.xyz "$cfg" &
done
