# frag_center.py #
This script will create balck and white heatmaps of fragment centers. Best used for unstranded data such as ChIP-seq.

# File requirements #
The input file should be a tab delimited file that contains the start and end of fragments/reads that overlap to the region of interest where the center is the feature under study (e.g. TSSs). [Bedtools intersect](https://bedtools.readthedocs.io/en/latest/content/tools/intersect.html) should be used to determine this overlap and obtain the following required type file required as input for **frag_center.py**:

| chr6 | 142946246 | 142946446 | Gene_A | 102 | - | chr6 | 142946247 | 142946248 | A00876:119:HW5F5DRXX:2:2207:29170:1157 | 255 | - |
| ---- |:---------:|:---------:|:------:|:---:|:-:|:----:|:---------:|:---------:|:--------------------------------------:|:---:|:-:|


# Behavior #
The fragment centers are determined from fragments of user chosen lengths to and heatmaps are created. Fragment lengths and black values are optionalities.

# Dependencies #
### Python libraries ###
Pandas: https://pypi.org/project/pandas/

Numpy: https://pypi.org/project/numpy/

Matplotlib: https://matplotlib.org/stable/users/installing/index.html

# Example command usage #
```
python frag_center.py <arguments.txt> 
```
# Please provide a paramter.txt file #
## Parameter description ##
```
PATH=<str> path to the file formatted as described above.
OUTPUT_DIR=<str> path to ouput directory.
FRAG_SIZE=<int>-<int> dashed separated integers of range of fragment sizes
BLACK_MAX=<int> the average value in the heatmap will be calculated. The max black value will be set as the average times the BLACK_MAX. The darkest pixel is assigned             to the max value indicated while white is zero. A gradient of white to black is proporionally determined for the rest of the values in the heatmap.
VERTICAL_AVG=<int> Number of rows to be vertically averaged.
WIDTH=<int> The number of pixels per base position.
```
# Example parameter.txt #
```
PATH=\Users\Desktop\plusminus100.bed
OUTPUT_DIR=\Users\Desktop\Heatmaps
FRAG_SIZE=50-100
BLACK_MAX=2
VERTICAL_AVG=10
WIDTH=1 
```
Output from example command usage: TBP-DFF-Seq data from [Spector et al., 2022](https://www.nature.com/articles/s41467-022-29739-x) for a +/- 100 bp region relative to the TSS of 10,273 transcription start regions (TSRs) identified here xxxxxxxxxxx.

Heatmaps: FRAG_SIZE 20-40, BLACK_MAX 10 | FRAG_SIZE 20-40, BLACK_MAX 1 | FRAG_SIZE 70-80, BLACK_MAX 10 | FRAG_SIZE 70-80, BLACK_MAX 1 

![20 40 avgx2](https://user-images.githubusercontent.com/38702786/166954004-c60c4ae2-de57-4450-80ba-ecd488d1b0a4.png)
![20 40 max](https://user-images.githubusercontent.com/38702786/166954007-63346351-24a6-40e2-bb51-b14501cf9496.png)
![70 80 avgx22](https://user-images.githubusercontent.com/38702786/166954008-297aaf9a-f135-41b9-ae7b-8f66ca999870.png)
![70 80 max](https://user-images.githubusercontent.com/38702786/166954010-232013bb-4ecf-42ad-8fc3-8612f66e188e.png)

