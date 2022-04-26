# abd.py #
This script will calculate the proportion of each base at a given position for multiple sequences of the same length. The output is an excel file containing line plots displaying the proportion for each base. 

# File requirements #
The input file should be a tab delimited file with at least two columns: 
   1. A column containing one sequence per row. The sequences can be of any length (as long as they are even), but they all have to be of the same length.
   2. A column with expression/ fold change or any type of numerical data to sort the file and thereby the column with the sequences.

# Behavior #
The input file will be sorted (greatest to least) by the header of a column of choice (e.g. peak enrichment, fold changes, p-values, etc). 
  * This is useful when interested in the composition of the underlying DNA sequence of high/low affinity binding sites, for example. 

A base distribution will be calculated for the indicated percentage of sequences.
  * Only the sequences that fall within the lower and upper bound percentages will be used for the analysis.

# Dependencies #
Pandas: https://pypi.org/project/pandas/
(The output of the script is an excel file. Pandas has an excel class. However, if the error "ModuleNotFoundError: No module named 'xlsxwriter'" appears after running the script, then please pip install xlsxwriter)

Numpy: https://pypi.org/project/numpy/

Operating system (OS): https://pypi.org/project/os-sys/

# Example of arguments #
```
python abd.py <file name> \
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
file name: <str> tab delimited file that at a minimum contains a column to sort the file by and a column with the sequences
Header column to sort by: <str> Comma separated headers for every comlumn use for sorting. In the example run above, the input file will be first sorted by TBP fold changes and the base distributions calculated for each percentage slicing before moving on to sort by TAF1 and so on.
Header column with sequences: <str> The header of the sequence column. The sequences can be of any length as long as they are even.
Percentages for slicing: <int> Commma separated pair of percentages to which the calculations will be restricted to. In the example run above, the input file will be first sorted by TBP fold changes and the base distributions calculated for sequences within 70-80%, then 90-100% before moving on to sort by TAF1 and so on.

The dataset "trial_truQuant_master.txt" from XXXX can be downloaded [here](https://github.com/JuanFSantana/DNA-and-RNA-seq-analysis-essentials/blob/main/Average%20base%20distribution%20plots/trial_truQuant_master.txt) if interested in running the example command line. 
