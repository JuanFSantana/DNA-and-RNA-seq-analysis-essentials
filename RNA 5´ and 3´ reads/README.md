
# prime3_5.py #
This script will yield two files: each with the position of the 5´ and 3´ ends of reads.

# File requirements #
The input file should be bed file. 

# Behavior #
The input file will be sorted (greatest to least) by the header of a column of choice (e.g. peak enrichment, fold change, p-value, etc). 
  * This is useful when interested in the composition of the underlying DNA sequence of high/low affinity binding sites, for example. 

The sequence will be sliced for each of the regions only for the sequences that fall within the lower and upper bound percentages chosen.
  * This analysis gives a clearer view of the preference/disfavor of sequences. 

# Dependencies #
### Python libraries ###
Pandas: https://pypi.org/project/pandas/
(The output of the script is an excel file. Pandas has an excel class. However, if the error "ModuleNotFoundError: No module named 'xlsxwriter'" appears after running the script, then please pip install xlsxwriter)

Operating system (OS): https://pypi.org/project/os-sys/

# Example of arguments #
```
python abd.py <File name> \
              <Header column to sort by greatest to least> \
              <Header column with sequences> \
              <Percent for slicing> \
              <Region to slice> \

Example command usage: 
python sequence_slicer.py trial_truQuant_master.txt \
                          -100+100 \
                          TBP,TAF1,TFIIB \
                          0,10,20,30
                          -36,-19,-5,5
```
# Parameter description #
```
File name: <str> tab delimited file that at a minimum contains a column to sort the file by and a column with the sequences

Header column with sequences: <str> The header of the sequence column. The sequences can be of any length as long as they are even.

Header column to sort by: <str> Comma separated headers for every comlumn use for sorting. In the example run above, the input file will be first sorted by TBP fold change and sequences sliced for each region before moving on to sort by TAF1 and so on.

Percentages to segment the dataset: <int> A percentage to which the analysis will be restricted to. In the example run above, the dataset will be segment to 0-10% based on the TBP fold change and then the regions -36 to -19, and -5 to +5 will be sliced before moving on to sort by TAF1 and so on.

Region to slice: <int> The region of the sequence to be sliced and kept reltive to the center of the sequence. In the example above, the center of the sequence is in the +1 position, the transcription start site (TSS), and the regions -36 to -19 and -5 to +5 relative to the TSS will be sliced and kept.
```

The dataset "trial_truQuant_master.txt" from XXXX can be downloaded [here](https://github.com/JuanFSantana/DNA-and-RNA-seq-analysis-essentials/blob/main/Average%20base%20distribution%20plots/trial_truQuant_master.txt) if interested in running the example command line.    

