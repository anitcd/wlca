// gcc -o mergeUniqLTCcombinations mergeUniqLTCcombinations.c
// ./mergeUniqLTCcombinations freq_combi.txt all_temp.txt dupRemoved.csv patIDmapping.txt sampleWeights.txt

#include "common.h"

int main(int argc, char *argv[]) {
    FILE *f1, *f2, *f3, *f4, *f5;
    char combiFilePath[256], allFilePath[256], outFilePath[256], outMappingFilePath[256], outFreqFilePath[256], combinationString[256], combinationString2[256], patID[256], content[999];
    long i, freq, flag;
    
    strcpy(combiFilePath, argv[1]);
    strcpy(allFilePath, argv[2]);
    strcpy(outFilePath, argv[3]);
    strcpy(outMappingFilePath, argv[4]);
    strcpy(outFreqFilePath, argv[5]);
    
    f1 = fopen(combiFilePath, "r");
    if(f1 == NULL) {
        printf("\n  Can not open the file 1 \"%s\"\n", combiFilePath); exit(1);
    }
    f2 = fopen(allFilePath, "r");
    if(f2 == NULL) {
        printf("\n  Can not open the file 2 \"%s\"\n", allFilePath); exit(1);
    }
    f3 = fopen(outFilePath, "a");
    if(f3 == NULL) {
        printf("\n  Can not open the file 3 \"%s\"\n", outFilePath); exit(1);
    }
    f4 = fopen(outMappingFilePath, "w");
    if(f4 == NULL) {
        printf("\n  Can not open the file 4 \"%s\"\n", outMappingFilePath); exit(1);
    }
    f5 = fopen(outFreqFilePath, "w");
    if(f5 == NULL) {
        printf("\n  Can not open the file 5 \"%s\"\n", outFreqFilePath); exit(1);
    }
    
    while(fscanf(f1, "%ld %s", &freq, combinationString) > 0) {
        flag = 0;
        for(i=0; i<freq; i++) {
            fscanf(f2, "%s %s %s", patID, combinationString2, content);
            if(strcmp(combinationString, combinationString2) == 0) {
                if(flag == 0) {
                    fprintf(f3, "%s\n", content);
                    fprintf(f4, "%s ", patID);
                    flag = 1;
                }
                else {
                    fprintf(f4, "%s ", patID);
                }
            }
            else {
                printf("Combination strings are not sorted in file '%s'.\n", allFilePath);
                exit(1);
            }
        }
        fprintf(f4, "\n");
        fprintf(f5, "%ld\n", freq);
    }
    
    fclose(f1); fclose(f2); fclose(f3); fclose(f4); fclose(f5);
    return 0;
}

