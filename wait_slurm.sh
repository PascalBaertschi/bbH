#!/bin/sh
while [ $(squeue -u pbaertsc | wc -l) -gt 1 ]
do
    date
    echo "sleep for 60 minutes..."
    sleep 60m
done
