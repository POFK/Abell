/*************************************************************************
	> File Name: test.c
	> Author: mtx
	> Mail: maotianxiang@bao.ac.cn
	> Created Time: Sat 24 Dec 2016 04:26:55 PM CST
 ************************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "groupstuff.h"
struct POS
{
    float x;
    float y;
    float z;
};
struct Vel
{
    float x;
    float y;
    float z;
};

int main()
{

    printf("\n\n");
    void *Par[20];  // Input parameter;
    char OutputDir[200];
    sprintf(OutputDir, "/datascope/indra0_/0_0_3/snapdir_052");
    int num=52;
    int TotNgroups;

    // get_total_number_of_groups
    Par[0]=OutputDir;
    Par[1]=&num;
    TotNgroups=get_total_number_of_groups(2,Par);
    //swap_Nbyte((char *)&TotNgroups,1,4);
    printf("TotNgroups:%d\n",TotNgroups);

    // get_group_catalogue
    int *GroupLen= (int*)malloc(TotNgroups * sizeof(int));
    int *GroupFileNr= (int*)malloc(TotNgroups * sizeof(int));
    int *GroupNr= (int*)malloc(TotNgroups * sizeof(int));
    Par[2]=&GroupLen[0];
    Par[3]=&GroupFileNr[0];
    Par[4]=&GroupNr[0];
    get_group_catalogue(5,Par);

    // get_hash_table_size
    int HashTabsize=0;
    char SnapBase[200];
    sprintf(SnapBase, "snapshot");
    int NFiles=0;
    Par[2]=SnapBase;
    Par[3]=&NFiles;
    HashTabsize=get_hash_table_size(4,Par);
    //swap_Nbyte((char *)&HashTabsize,1,4);
    //swap_Nbyte((char *)&NFiles,1,4);
    printf("NFiles:%d\n",NFiles);
    printf("HashTableSize:%d\n",HashTabsize);

    // get_hash_table
    int Hashtable[HashTabsize],Filetable[HashTabsize],LastHashCell[HashTabsize],NInFiles[HashTabsize];
    Par[3]=&Hashtable[0];
    Par[4]=&Filetable[0];
    Par[5]=&LastHashCell[0];
    Par[6]=&NInFiles[0];
    get_hash_table(8,Par);
    //swap_Nbyte((char *)&Hashtable[0],HashTabsize,4);

    // get_group_coordinates
    int N=0; //group number
    int FiNr, GrNr, Len;
    FiNr=GroupFileNr[N];
    GrNr=GroupNr[N];
    Len=GroupLen[N];
    char PostProcDir[200];
    sprintf(PostProcDir,"/datascope/indra0_/0_0_3/postproc_052");
    float vel[Len*3], pos[Len*3];
    float Sx,Sy,Sz=0.0;
    Par[0]=OutputDir;
    Par[1]=PostProcDir;
    Par[2]=&num;
    Par[3]=SnapBase;
    Par[4]=&Hashtable[0];
    Par[5]=&Filetable[0];
    Par[6]=&HashTabsize;
    Par[7]=&LastHashCell[0];
    Par[8]=&NInFiles[0];
    Par[9]=&GrNr;
    Par[10]=&FiNr;
    Par[11]=&Len;
    Par[12]=&pos[0];
    Par[13]=&vel[0];

    Par[14]=&Sx;
    Par[15]=&Sy;
    Par[16]=&Sz;
    get_group_coordinates(16,Par);
/**************************************************************/
    printf("myself:\n");
    printf("GroupLen:%d\n",Len);
    printf("GroupFileNr:%d\n",FiNr);
    printf("GroupNr:%d\n",GrNr);
    printf("Sx:%lf\n",Sx);
    printf("Sy:%lf\n",Sy);
    printf("Sz:%lf\n",Sz);
   
    return 0;
}


