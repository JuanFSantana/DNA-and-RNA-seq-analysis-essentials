# heatmap.py #
This script will create two types of heatmaps: black and white heatmaps corresponding to the number of 5´ or 3´ reads in a window and a color (red and blue with white as zero) heatmap corresponding to the fold change between the number of 5´ or 3´ reads in a window for control and an experimental dataset. 

# File requirements #
The input file should be a tab delimited file that contains the start and end of 5´ or 3´ reads overlapping a chosen genomic window. I have posted a script that yields the genomic coordinates of 5´ and 3´ reads from an aligment bed file [here](https://github.com/JuanFSantana/DNA-and-RNA-seq-analysis-essentials/tree/main/Stranded%205%C2%B4%20and%203%C2%B4%20reads). This file can now be used as input for programs such as [bedtools intersect] (https://bedtools.readthedocs.io/en/latest/content/tools/intersect.html) which can determine whether two sets of genomic features overlap.

Example file:

| chr6 | 142946246 | 142946446 | Gene_A | 102 | - | chr6 | 142946247 | 142946248 | A00876:119:HW5F5DRXX:2:2207:29170:1157 | 255 | - |
| ---- |:---------:|:---------:|:------:|:---:|:-:|:----:|:---------:|:---------:|:--------------------------------------:|:---:|:-:|


# Behavior #
Two input files, control and experimental, are required with the format described above. The script has optionality for black/white and blue/red max color levels, calculating vertical a vertical average and width.

# Dependencies #
### Python libraries ###
Pandas: https://pypi.org/project/pandas/
(The output of the script is an excel file. Pandas has an excel class. However, if the error "ModuleNotFoundError: No module named 'xlsxwriter'" appears after running the script, then please pip install xlsxwriter)

Numpy: https://pypi.org/project/numpy/

https://matplotlib.org/stable/users/installing/index.html

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
