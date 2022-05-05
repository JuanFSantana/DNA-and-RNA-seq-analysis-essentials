# frag_center.py #
This script will create balck and white heatmaps of fragment centers. Best used for unstranded data such as ChIP-seq.

# File requirements #
The input file should be a tab delimited file that contains the start and end of fragments/reads that overlap to the region of interest where the center is the feature under study (e.g. TSSs). [Bedtools intersect](https://bedtools.readthedocs.io/en/latest/content/tools/intersect.html) should be used to determine this overlap and obtain the following required type file required as input for **frag_center.py**:

| chr6 | 142946246 | 142946446 | Gene_A | 102 | - | chr6 | 142946247 | 142946248 | A00876:119:HW5F5DRXX:2:2207:29170:1157 | 255 | - |
| ---- |:---------:|:---------:|:------:|:---:|:-:|:----:|:---------:|:---------:|:--------------------------------------:|:---:|:-:|


# Behavior #
The fragment centers are determined. Fragment lengths and black values are optionalities. Heatmaps of fragment centers of fragments of user chosen lengthd will be created with user chosen black values. 

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
python heatmap.py plusminus100.bed \
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

![Picture4](https://user-images.githubusercontent.com/38702786/166007154-9fb6689b-abcb-4769-a530-9180741ea600.jpg)   ![Picture5](https://user-images.githubusercontent.com/38702786/166007152-6d2a2d27-2b4b-4024-a628-f4b540c9b739.jpg)   ![Picture6](https://user-images.githubusercontent.com/38702786/166007155-50f8ad5e-191a-461f-8400-8b66708b6f87.jpg)

