# sh test_wlca.sh sampleInput.csv sampleWeights.txt 5 <outPath> <runID>

if [ $# -lt 5 ]
then
    echo "Usage: " $0 " list-of-arguments";
    echo "1. Input data file in CSV format.";
    echo "2. Input sample weights file.";
    echo "3. No. of clusters (k).";
    echo "4. Output path."
    echo "5. Run ID.";
    exit 1;
fi

dataFile=$1
sampleWeightFile=$2
nCluster=$3
outPath=$4
runID=$5

# Customized filenames to store results.
file=$(echo $1 | sed 's/.*\///g' | sed 's/.csv//g')
weightFilePath=$outPath"WLCAweight_"$file"_nCluster="$nCluster"_r"$runID".txt"
logLikelihoodFilePath=$outPath"WLCAlogLikelihood_"$file"_nCluster="$nCluster"_r"$runID".png"
thetaFilePath=$outPath"WLCAtheta_"$file"_nCluster="$nCluster"_r"$runID".txt"
randomStateFilePath=$outPath"WLCArandomState_"$file"_nCluster="$nCluster"_r"$runID #".npy"
BICFilePath=$outPath"WLCABIC_"$file"_nCluster="$nCluster"_r"$runID".txt"
resFilePath=$outPath"WLCAres_"$file"_nCluster="$nCluster"_r"$runID".txt"
llFilePath=$outPath"WLCAll_"$file"_nCluster="$nCluster"_r"$runID".txt"

# Logs
date=$(date '+%Y-%m-%d %H:%M:%S')
echo $date" WLCA_"$file"_nCluster="$nCluster"_r"$runID" Started." >> ./output/WLCA_log.txt

# Call 'test_lca.py'
python test_wlca.py $dataFile $sampleWeightFile $nCluster $weightFilePath $logLikelihoodFilePath $thetaFilePath $randomStateFilePath $BICFilePath $resFilePath $llFilePath

date=$(date '+%Y-%m-%d %H:%M:%S')
echo $date" WLCA_"$file"_nCluster="$nCluster"_r"$runID" Finished." >> ./output/WLCA_log.txt
