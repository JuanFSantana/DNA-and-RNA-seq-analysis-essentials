# dff_seq_feature_count.py #
Juan F. Santana, Ph.D. (<juan-santana@uiowa.edu>), University of Iowa, Iowa City, I.A.

Digestion with human DNA fragmentation factor (DFF) followed by immunoprecipitation and sequencing (DFF-Seq-ChIP) precisely reveals the relationship between DNA-interacting proteins and chromatin [Santana et al., 2022](https://academic.oup.com/nar/article/50/16/9127/6659871), [Spector et al., 2022](https://www.nature.com/articles/s41467-022-29739-x), [Ball et al., 2022a](https://www.mdpi.com/1999-4915/14/4/779), and [Ball et al., 2022b](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9239164/).

fragMap of Pol II DFF-Seq performed on HFF cells ([Spector et al., 2022](https://www.nature.com/articles/s41467-022-29739-x)) over +/- 1,000 bp regions from the MaxTSS of 12,229 genes in HFF cells determined with PRO-Cap ([Nilson et al., 2022](https://doi.org/10.1093/nar/gkac678)). Chromatin features of Pol II can be determined based on the fragment size and their positional ranges in relation to the MaxTSS (see below). 

The program tallies the number of DFF-Seq reads with specific length ranges that overlap within a designated genomic interval. The program requires a Linux operating system and Python 3+.
 
![fragMap-exp4-polII](https://github.com/JuanFSantana/DNA-and-RNA-seq-analysis-essentials/assets/38702786/184aa0a9-d262-4639-adce-4b492ef2f2ea)

# File requirements #
The input regions file should be a six-column, tab-delimited bed file containing chromosome, start and end positions, and the strand information for each region. The regions can be of any length as long as it is even and the center is the MaxTSS. 
 
| chr6 | 142946246 | 142946446 | Gene_A | 255 | - |
|:----:|:---------:|:---------:|:------:|:---:|:-:|

The input fragments file should be a six-column, tab-delimited bed file containing chromosome, start and end positions, and the strand information for each fragment.

| chr6 | 142946247 | 142946298 | A00876:119:HW5F5DRXX:2:2207:29170:1157 | 255 | - |
|:----:|:---------:|:---------:|:--------------------------------------:|:---:|:-:|


# Behavior #
Generates a bed file with raw and normalized counts for each feature per gene.  

# Dependencies #

bedtools: https://bedtools.readthedocs.io/en/latest/content/installation.html, developed by the Quinlan laboratory at the University of Utah. 

# Example command usage #
```
python3 dff_seq_feature_count.py plusminus1000_from_TSS_1000genes.bed \
        -f PolII-DFF-ChIP-Seq-Rep1.bed -20 90 40 65 -60 60 65 10 \
        -n Free-Pol-II PIC \
        -t centers \
        -o /home/user/dir/ \
        -s 0.5

```
# Parameter description #
```
regions: <str> Bed file of genomic regions of chosen length. The regions should be of even length and the MaxTSS should be in the middle of the region.

-f: <str> Singular fragment dataset, followed by position range, followed by fragment range (range limits are inclusive). Example 1: -f /home/reads.bed 20 1000 400 800. Example 2: -f /home/reads.bed 20 1000 400 800 20 1000 300 600

-n: <str> Provide a name for each feature (space sperated). The names should be in the same order as the features provided with -f.

-t: <str> Overlap for quantification. Please choose from the following options: center, full, or partial (center = center of fragment within interval; full = whole read within interval; partial = fragment overlap with interval >= 1 bp)

-s: <int | float> Correction factors - must be 1 per dataset (-f) space separated. The correction factors should be in the same order as the datasets provided with -f.

-o: <str> Path to output, for example -o /home/user/dir

```


