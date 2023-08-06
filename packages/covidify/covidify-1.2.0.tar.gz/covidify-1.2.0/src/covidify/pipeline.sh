#!/bin/bash
function banner {
    # echo ""
    echo "###"
    echo "### $1"
    echo "###"
}

ENV=$1
OUT_FDR=$2
SOURCE=$3
COUNTRY=$4
TOP_CNT=$5
FRCST_DAYS=$6

set -e

mkdir -p $OUT_FDR

banner "Job arguments:"
echo "... ENV: $ENV"
echo "... OUTPUT FOLDER: $OUT_FDR"
echo "... DATA SOURCE: $SOURCE"
echo "... COUNTRIES: $COUNTRY"
echo "... TOP INFECTED COUNTRIES: $TOP_CNT"
echo "... FORECAST PERIOD: $FRCST_DAYS"


banner "Data Extraction"
python $ENV/data_prep.py --output_folder $OUT_FDR --source $SOURCE --country $COUNTRY --top $TOP_CNT

banner "Training Forecasting Model"
python $ENV/forecast.py --output_folder $OUT_FDR --num_days $FRCST_DAYS

banner "Data Visualization"
python $ENV/data_visualization.py --output_folder $OUT_FDR --country $COUNTRY --top $TOP_CNT

banner "Complete!"
echo "* Results in: $OUT_FDR"