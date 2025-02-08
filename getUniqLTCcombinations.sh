# sh getUniqLTCcombinations.sh inputSample_Dup.csv

uniqLTCcombiFile=$(echo $1 | sed 's/.csv/_uniqLTCcombi.csv/g')
uniqLTCcombiWeightsFile=$(echo $1 | sed 's/.csv/_uniqLTCcombiWeights.txt/g')
patIDmappingFile=$(echo $1 | sed 's/.csv/_uniqLTCcombiPatIDmapping.txt/g')

gcc -o mergeUniqLTCcombinations mergeUniqLTCcombinations.c

n=$(cat $1 | wc -l)
n=$((n - 1))

cat $1 | tail -$n > content_temp.txt
cat $1 | tail -$n | sed 's/,/ /g' | awk '{print $2}' > patIDs_temp.txt # Column 2 in input csv is UniquePatientID for PCCIU. Change for other data.
cat $1 | tail -$n | sed 's/,/ /g' | awk '{for(i=6;i<=NF-1;i++) printf(" %s", $i); printf("\n");}' | sed 's/ //g' > combinations_temp.txt # col (6 - NF1) in input csv are LTCs for PCCIU. Change for other data.

paste patIDs_temp.txt combinations_temp.txt content_temp.txt | sort -k2,2 > all_temp.txt

cat combinations_temp.txt | sort | uniq -c | sort -k2,2 > freq_combi.txt

rm -f dupRemoved.csv patIDs_temp.txt combinations_temp.txt content_temp.txt
cat $1 | head -1 > $uniqLTCcombiFile

./mergeUniqLTCcombinations freq_combi.txt all_temp.txt $uniqLTCcombiFile $patIDmappingFile $uniqLTCcombiWeightsFile

rm -f freq_combi.txt all_temp.txt

echo "Following files are successfully generated.\n - "$uniqLTCcombiFile"\n - "$uniqLTCcombiWeightsFile"\n - "$patIDmappingFile
