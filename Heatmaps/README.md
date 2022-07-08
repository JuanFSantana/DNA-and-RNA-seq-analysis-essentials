# heatmap.py #
This script will create two types of heatmaps: black and white heatmaps corresponding to the number of 5´ or 3´ reads in a window and a color (red and blue with white as zero) heatmap corresponding to the log2 fold change between the number of 5´ or 3´ reads in a window for control over the experimental dataset in the same window. 

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

Numpy: https://pypi.org/project/numpy/

Matplotlib: https://matplotlib.org/stable/users/installing/index.html

# Example of arguments #
```
python heatmap.py <File 1,File 2> \
              <Name output heatmap 1,name output heatmap 2,Name output heatmap 3 > \
              <Black/white max value,Red/blue max value> \
              <Vertical average> \
              <Output directory> \
              <Heatmap width> \

Example command usage: 
python heatmap.py TBP_5_reads_overlap_dmso.bed,TBP_5_reads_overlap_vhl.bed \
                  TBP_5_DMSO,TBP_5_VHL,TBP_5_ratio \
                  avgx2,4 \
                  10 \
                  /Users/Desktop/Heatmaps \
                  3
```
# Parameter description #
```
File 1,File 2: <str> Two files, control and experimental - in that order -, formatted as described above.

Name output heatmap 1,name output heatmap 2,Name output heatmap 3: <str> Comma separated names for the output heatmaps. The order of names should be as follow: control, experimental, ratio (control/experimental). 

Black/white max value,Red/blue max value: Black/ white max value options are "max" or avgx<int> or avgy<int>. "max" is the largest value present in the heatmap. avgx<int/float> is the average of the heatmap times an integer. avgy<int/float> is the average of the heatmap divided by an integer. For Red/blue max value, the only option is <int/float> chosen by the user. Both the max and min values are set to this number.  
Black and white heatmaps, the darkest pixel is assigned to the max value indicated while white is zero. A gradient of white to black is proporionally determined for the rest of the values in the heatmap. Red and blue heatmaps, the darkest red and blue pixel is assigned to the max value indicated while white is zero. The color for positive numbers are determined proportionally in the white to red gradient while the colors for negative colors are determined proportionally in the white to blue gradient.

Vertical average: <int> Number of rows to be vertically averaged.

Output directory: <str> The output heatmaps will be deposited in this path. 

Heatmap width: <int> The number of pixels per base position.
```
Example output: control, experimental and fold change (log2) heatmaps for a +/- 100 bp region relative to the TSS of 10,273 transcription start regions (TSRs) identified here (paper under revision).

Black/white max value, Red/blue max value = avgx4.1,1.2

Vertical average = 10

Heatmap width = 3

![Picture4](https://user-images.githubusercontent.com/38702786/166007154-9fb6689b-abcb-4769-a530-9180741ea600.jpg)   ![Picture5](https://user-images.githubusercontent.com/38702786/166007152-6d2a2d27-2b4b-4024-a628-f4b540c9b739.jpg)   ![Picture6](https://user-images.githubusercontent.com/38702786/166007155-50f8ad5e-191a-461f-8400-8b66708b6f87.jpg)
