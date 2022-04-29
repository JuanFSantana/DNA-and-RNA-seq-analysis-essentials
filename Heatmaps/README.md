# heatmap.py #
This script will create two types of heatmaps: black and white heatmaps corresponding to the number of 5´ or 3´ reads in a window and a color heatmap corresponding to the fold change between the number of 5´ or 3´ reads in a window for control and an experimental dataset. 

# File requirements #
The input file should be a tab delimited file that contains the start and end of 5´ or 3´ reads overlapping a chosen genomic window. I have posted a script that yields the genomic coordinates of 5´ and 3´ reads from a bed file [here](https://github.com/JuanFSantana/DNA-and-RNA-seq-analysis-essentials/tree/main/Stranded%205%C2%B4%20and%203%C2%B4%20reads).

Example file:
| Header 1      | Header 2      |
| ------------- |:-------------:| 
| 2.5           | Gene1_ATCGTT  | 
| 3             | Gene2_CCCAGT  |  
| 10            | Gene2_TTAGGC  |    

# Behavior #
The input file will be sorted (greatest to least) by the header of a column of choice (e.g. peak enrichment, fold change, p-value, etc). 
  * This is useful when interested in the composition of the underlying DNA sequence of high/low affinity binding sites, for example. 

A base distribution will be calculated for the indicated percentage of sequences.
  * Only the sequences that fall within the lower and upper bound percentages will be used for the analysis.

# Dependencies #
### Python libraries ###
Pandas: https://pypi.org/project/pandas/
(The output of the script is an excel file. Pandas has an excel class. However, if the error "ModuleNotFoundError: No module named 'xlsxwriter'" appears after running the script, then please pip install xlsxwriter)

Numpy: https://pypi.org/project/numpy/

Operating system (OS): https://pypi.org/project/os-sys/

# Example of arguments #
```
python abd.py <File name> \
              <Header column to sort by greatest to least> \
              <Header column with sequences> \
              <Percentages for slicing> \

Example command usage: 
python abd.py trial_truQuant_master.txt \
              TBP,TAF1,TFIIB \
              -100+100 \
              70,80,90,100
```
# Parameter description #
```
file name: <str> tab delimited file that at a minimum contains a column to sort the file by and a column with the sequences

Header column to sort by: <str> Comma separated headers for every comlumn use for sorting. In the example run above, the input file will be first sorted by TBP fold change and the base distributions calculated for each percentage slicing before moving on to sort by TAF1 and so on.

Header column with sequences: <str> The header of the sequence column. The sequences can be of any length as long as they are even.

Percentages for slicing: <int> Commma separated pair of percentages to which the calculations will be restricted to. In the example run above, the input file will be first sorted by TBP fold change and the base distributions calculated for sequences within 70-80%, then 90-100% before moving on to sort by TAF1 and so on.
```

The dataset "trial_truQuant_master.txt" from XXXX can be downloaded [here](https://github.com/JuanFSantana/DNA-and-RNA-seq-analysis-essentials/blob/main/Average%20base%20distribution%20plots/trial_truQuant_master.txt) if interested in running the example command line. 
