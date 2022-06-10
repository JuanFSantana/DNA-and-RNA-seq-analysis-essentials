# abd_substraction.py #
This script will calculate the proportion of each base at a given position for multiple sequences of the same length for two groups. Specifcally, it will sort the file based on a given paramter (fold change, peak enrichment, etc) and calculate the base distribution for the top and bottom X% chosen. It will then substract the base distribution of the top X% from the bottom X%. The output is an excel file containing line plots displaying the proportion for each base. 

# File requirements #
The input file should be a tab delimited file with at least two columns: 
   1. A column with expression/ fold change or any type of numerical data to sort the file and thereby the column with the sequences.
   2. A column containing one sequence per row. The sequences can be of any length (as long as they are even), but they all have to be of the same length.
      * The sequence must be of the format: name, underscore, DNA sequence.

Example file:
| Header 1      | Header 2      |
| ------------- |:-------------:| 
| 2.5           | Gene1_ATCGTT  | 
| 3             | Gene2_CCCAGT  |  
| 10            | Gene2_TTAGGC  |    


# Behavior #
The input file will be sorted (greatest to least) by the header of a column of choice (e.g. peak enrichment, fold change, p-value, etc). 
  * This is useful when interested in the composition of the underlying DNA sequence of high/low affinity binding sites, for example. 

A base distribution will be calculated for the indicated two groups of percentage of sequences.
  * Only the sequences that fall within the lower and upper bound percentages will be used for the analysis.
  * This analysis gives a clearer view of the preference/disfavor of sequences by substracting the top from the bottom. 

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
              <Percent for slicing> \

Example command usage: 
python abd_substraction.py trial_truQuant_master.txt \
                           TBP,TAF1,TFIIB,TAF4,XPB \
                           -100+100 \
                           20
```
# Parameter description #
```
File name: <str> tab delimited file that at a minimum contains a column to sort the file by and a column with the sequences

Header column to sort by: <str> Comma separated headers for every comlumn use for sorting. In the example run above, the input file will be first sorted by TBP fold change and the base distributions calculated for each percentage slicing before moving on to sort by TAF1 and so on.

Header column with sequences: <str> The header of the sequence column. The sequences can be of any length as long as they are even.

Percentages for slicing: <int> A percentage to which the calculations will be restricted to. In the example run above, the base distribution of the top 20% will be substracted from the bottom 20%. The input file will be first sorted by TBP fold change and the base distributions calculated for sequences within 0-20% followed by 80-100%. The base distribution calculated from 0-20% will be substracted from the 80-100% before moving on to sort by TAF1 and so on.
```

The dataset "trial_truQuant_master.txt" from XXXX can be downloaded [here](https://github.com/JuanFSantana/DNA-and-RNA-seq-analysis-essentials/blob/main/Average%20base%20distribution%20plots/trial_truQuant_master.txt) if interested in running the example command line. 

Example output: Line plot of the base distributions of a +/- 100bp region following substraction of the top 20% minus bottom 20% dependent TBP transcription start regions (TSRs) as explained here XXXXXXXX. Note that the output excel file contains multiple sheets for each factor.

![Picture7](https://user-images.githubusercontent.com/38702786/166009944-6e392122-94b7-4712-81d9-95f75606c80c.png)
