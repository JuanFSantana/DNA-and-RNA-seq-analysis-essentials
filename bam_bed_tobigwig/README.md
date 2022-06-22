# bam_bed_tobigwig.py #
This script will create bigWig tracks of fragments of user specified sizes from BAM or BED files.

# File requirements #
A BAM or BED file and a chromsome size file.   

# Behavior #
The user can specifiy multiple tracks to be created from different fragment sizes. The output of this script is a directory named 'bigWig' containing each of the bigWig tracks.

# Dependencies #
### Python libraries ###
Pandas: https://pypi.org/project/pandas/

Numpy: https://pypi.org/project/numpy/

# Example of arguments #
```
python bam_bed_tobigwig.py <BAM/BED file> <chromosome size file> \
                           <Fragment size intervals> \
                           [Threads] \
                           [Spike-in/normalization factor] \
              
Example command usage: 
python bam_bed_tobigwig.py test.bam hg38.chrom.sizes \
                           -r 30 35 62 82 250 300 500 500 \
                           -t 4 \
                           -n 1.8
```
# Parameter description #
```
file name: <str> tab delimited file that at a minimum contains a column to sort the file by and a column with the sequences

Header column to sort by: <str> Comma separated headers for every comlumn use for sorting. In the example run above, the input file will be first sorted by TBP fold change and the base distributions calculated for each percentage slicing before moving on to sort by TAF1 and so on.

Header column with sequences: <str> The header of the sequence column. The sequences can be of any length as long as they are even.

Percentages for slicing: <int> Commma separated pair of percentages to which the calculations will be restricted to. In the example run above, the input file will be first sorted by TBP fold change and the base distributions calculated for sequences within 70-80%, then 90-100% before moving on to sort by TAF1 and so on.
```

The dataset "trial_truQuant_master.txt" from XXXX can be downloaded [here](https://github.com/JuanFSantana/DNA-and-RNA-seq-analysis-essentials/blob/main/Average%20base%20distribution%20plots/trial_truQuant_master.txt) if interested in running the example command line. 

Example output: Line plot of the base distributions of a +/- 100bp region for different fold change percentage groups transcription start regions (TSRs) as explained here XXXXXXXX. Note that the output excel file contains multiple sheets for each percentage group.

![Picture8](https://user-images.githubusercontent.com/38702786/166021962-6fdf9b5e-c4e0-4d4b-9eb0-6511d47459db.png)
