# abd.py #
This script will calculate the proportion of each base at a given position for multiple sequences of the same length. The output is an excel file containing line plots displaying the proportion for each base. 

# File requirements #
The input file should be a tab delimited file with at least two columns: 
   1. A column containing one sequence per row. The sequences can be of any length (as long as they are even), but they all have to be of the same length.
   2. A column with expression/ fold change or any type of numerical data to sort the file and thereby the column with the sequences.
      * The sequence must be of the format name, underscore, DNA sequence.

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
File name: <str> tab delimited file that at a minimum contains a column to sort the file by and a column with the sequences

Header column to sort by: <str> Comma separated headers for every comlumn use for sorting. In the example run above, the input file will be first sorted by TBP fold change and the base distributions calculated for each percentage slicing before moving on to sort by TAF1 and so on.

Header column with sequences: <str> The header of the sequence column. The sequences can be of any length as long as they are even.

Percentages for slicing: <int> Commma separated pair of percentages to which the calculations will be restricted to. In the example run above, the input file will be first sorted by TBP fold change and the base distributions calculated for sequences within 70-80%, then 90-100% before moving on to sort by TAF1 and so on.
```

The dataset "trial_truQuant_master.txt" from [Santana et al., 2022](https://academic.oup.com/nar/advance-article/doi/10.1093/nar/gkac678/6659871?guestAccessKey=88024805-7d8e-4421-a032-dbef1c737757) can be downloaded [here](https://github.com/JuanFSantana/DNA-and-RNA-seq-analysis-essentials/blob/main/Average%20base%20distribution%20plots/trial_truQuant_master.txt) if interested in running the example command line. 

Example output: Line plot of the base distributions of a +/- 100bp region for different fold change percentage groups transcription start regions (TSRs) as explained here (paper under revision). Note that the output excel file contains multiple sheets for each percentage group.

![Picture8](https://user-images.githubusercontent.com/38702786/166021962-6fdf9b5e-c4e0-4d4b-9eb0-6511d47459db.png)
