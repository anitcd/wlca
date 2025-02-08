# sh run_wlca.sh PCCIU_1K_40Col_0Removed.csv <sampleWeightsFile> 3 <outPath>

dataFile=$1
weightFile=$2
nCluster=$3
outPath=$4

# WLCA instances
for i in `seq 1 10`
do

    qsub batch_wlca.sh $dataFile $weightFile $nCluster $outPath $i

done

