# frag_center.py #
This script will create balck and white heatmaps of fragment centers. Best used for unstranded data such as ChIP-seq.

# File requirements #
The input file should be a tab delimited file that contains the start and end of fragments/reads that overlap to the region of interest where the center is the feature under study (e.g. TSSs). [Bedtools intersect](https://bedtools.readthedocs.io/en/latest/content/tools/intersect.html) should be used to determine this overlap and obtain the following required type file required as input for **frag_center.py**:

| chr6 | 142946246 | 142946446 | Gene_A | 102 | - | chr6 | 142946247 | 142946248 | A00876:119:HW5F5DRXX:2:2207:29170:1157 | 255 | - |
| ---- |:---------:|:---------:|:------:|:---:|:-:|:----:|:---------:|:---------:|:--------------------------------------:|:---:|:-:|


# Behavior #
The fragment centers are determined. Fragment lengths and black values are optionalities. Heatmaps of fragment centers of fragments of user chosen length will be created with user chosen black values. 

# Dependencies #
### Python libraries ###
Pandas: https://pypi.org/project/pandas/

Numpy: https://pypi.org/project/numpy/

Matplotlib: https://matplotlib.org/stable/users/installing/index.html

# Example of arguments #
```
python frag_center.py <File 1> \
                      <Fragment lengths> \
                      <Black values> \
                      <Vertical average> \
                      <Output directory> \
                      <Heatmap width> \

Example command usage: 
python frag_center.py plusminus100.bed \
                      all,20-40,70-80 \
                      avgx2,max \
                      10 \
                      /Desktop/Heatmaps \
                      3

```
# Parameter description #
```
File 1: <str> file formatted as described above.

Fragment lengths: Comma separated fragment lengths to be used for calculating the centers. The options can be a <str> all and/or <int>-<int>.

Black values: Max value optionalities are "max" or avgx<int> or avgy<int>. "max" is the largest value present in the heatmap. avgx<int/float> is the average of the heatmap times an integer. avgy<int/float> is the average of the heatmap divided by an integer. The darkest pixel is assigned to the max value indicated while white is zero. A gradient of white to black is proporionally determined for the rest of the values in the heatmap.

Vertical average: <int> Number of rows to be vertically averaged.

Output directory: <str> The output heatmaps will be deposited in this path. 

Heatmap width: <int> The number of pixels per base position.
```
Output from example command usage: TBP-DFF-Seq data from [Spector et al., 2022](https://www.nature.com/articles/s41467-022-29739-x) for a +/- 100 bp region relative to the TSS of 10,273 transcription start regions (TSRs) identified here xxxxxxxxxxx.

Heatmaps: frag.length 20-40, black.val avgx2 | frag.length 20-40, black.val max | frag.length 70-80, black.val avgx2 | frag.length 70-80, black.val max | frag.length all, black.val avgx2 | frag.length all, black.val max 

![20 40 avgx2](https://user-images.githubusercontent.com/38702786/166954004-c60c4ae2-de57-4450-80ba-ecd488d1b0a4.png)
![20 40 max](https://user-images.githubusercontent.com/38702786/166954007-63346351-24a6-40e2-bb51-b14501cf9496.png)
![70 80 avgx22](https://user-images.githubusercontent.com/38702786/166954008-297aaf9a-f135-41b9-ae7b-8f66ca999870.png)
![70 80 max](https://user-images.githubusercontent.com/38702786/166954010-232013bb-4ecf-42ad-8fc3-8612f66e188e.png)
![all avgx2](https://user-images.githubusercontent.com/38702786/166954011-e6231345-b7be-44a3-8d29-8816aff6dab1.png)
![all max](https://user-images.githubusercontent.com/38702786/166954013-6f73ae9f-0619-4395-9719-10a500e70bef.png)
