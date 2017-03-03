/*************************************************************************
	> File Name: get_spherical_region.c
	> Author: mtx
	> Mail: maotianxiang@bao.ac.cn
	> Created Time: Mon 02 Jan 2017 04:18:28 PM CST
 ************************************************************************/

#include<stdio.h>
#include <stdlib.h>
#include <string.h>
#include "groupstuff.h"
struct Vel
{
	float x;
	float y;
	float z;
};

int main(int argc, char ** argv)
{

	float h=0.704;
	printf("\n\n");
	int SimNum,Mrank;
	float Sx,Sy,Sz,Rad;
	sscanf(argv[1],"%d",&SimNum);
	sscanf(argv[2],"%f",&Sx);
	sscanf(argv[3],"%f",&Sy);
	sscanf(argv[4],"%f",&Sz);
	sscanf(argv[5],"%f",&Rad);
	sscanf(argv[6],"%d",&Mrank);
	printf("SimNum:%d\n",SimNum);
	printf("Sx:%f\t",Sx);
	printf("Sy:%f\t",Sy);
	printf("Sz:%f\t",Sz);
	Rad = Rad*h;
	printf("Rad:%f\n",Rad);
	int FNi,FNj,FNk;
	FNi=SimNum/8/8;
        FNj=SimNum%64/8;
        FNk=SimNum%64%8;

	void *Par[20];  // Input parameter;
	char OutputDir[200];
	sprintf(OutputDir, "/datascope/indra%d_/%d_%d_%d/snapdir_052",FNi,FNi,FNj,FNk);
	printf("PATH:%s\n",OutputDir);
	int num = 52;
	int TotNgroups;

	// get_total_number_of_groups
	Par[0] = OutputDir;
	Par[1] = &num;
	TotNgroups = get_total_number_of_groups(2, Par);
	printf("TotNgroups:%d\n", TotNgroups);

	// get_group_catalogue
	int *GroupLen= (int*)malloc(TotNgroups * sizeof(int));
        int *GroupFileNr= (int*)malloc(TotNgroups * sizeof(int));
        int *GroupNr= (int*)malloc(TotNgroups * sizeof(int));
	Par[2] = &GroupLen[0];
	Par[3] = &GroupFileNr[0];
	Par[4] = &GroupNr[0];
	get_group_catalogue(5, Par);
    
	// get_hash_table_size
	int HashTabsize = 0;
	char SnapBase[200];
	sprintf(SnapBase, "snapshot");
	int NFiles = 0;
	Par[2] = SnapBase;
	Par[3] = &NFiles;
	HashTabsize = get_hash_table_size(4, Par);
	printf("NFiles:%d\n", NFiles);
	printf("HashTableSize:%d\n", HashTabsize);

	// get_hash_table
	int Hashtable[HashTabsize], Filetable[HashTabsize], LastHashCell[HashTabsize], NInFiles[HashTabsize];
	Par[3] = &Hashtable[0];
	Par[4] = &Filetable[0];
	Par[5] = &LastHashCell[0];
	Par[6] = &NInFiles[0];
	get_hash_table(8, Par);

	// get_spherical_region_count
//	float Sx, Sy, Sz, Rad = 0.0;

	Par[0] = OutputDir;
	Par[1] = &num;
	Par[2] = SnapBase;
	Par[3] = &Hashtable[0];
	Par[4] = &Filetable[0];
	Par[5] = &HashTabsize;
	Par[6] = &LastHashCell[0];
	Par[7] = &NInFiles[0];
	Par[8] = &Sx;
	Par[9] = &Sy;
	Par[10] = &Sz;
	Par[11] = &Rad;

	int Pcount;
	Pcount = get_spherical_region_count(12, Par);
	printf("Pcount:%d\n", Pcount);

	// get_spherical_region_coordinates
	float *Pos= (float *)malloc(Pcount*3 * sizeof(float));
	Par[12] = &Pos[0];
	get_spherical_region_coordinates(13, Par);

	/**************************************************************/
	//  write data
    	FILE *fp;
	char OUT[200];
        int i;
	sprintf(OUT, "/datascope/indra4/Cluster/halo_spherical_region/M200rank%d_Sim%d_X%.2f_Y%.2f_Z%.2f_Rad%.2f.bin",Mrank,SimNum,Sx,Sy,Sz,Rad/h);
	if((fp = fopen(OUT, "wb")) == NULL)
	{
		printf("cannot open file\n");
	}

	for(i = 0; i < Pcount*3; i++)
	{
		fwrite(&Pos[i], sizeof(float), 1, fp);
	}

	fclose(fp);


	return 0;
}


