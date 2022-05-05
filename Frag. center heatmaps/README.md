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

![FC_20-40_VertAvg_10_BLACK_max_146 6_WIDTH_3_](https://user-images.githubusercontent.com/38702786/166952878-83195063-9a21-4c84-a0c2-065ac92d0a43.png)
![FC_70-80_VertAvg_10_BLACK_avgx2_0 38_WIDTH_3_](https://user-images.githubusercontent.com/38702786/166952885-5a12db6c-0f69-4574-94f1-da9d11ee0449.png)
![FC_70-80_VertAvg_10_BLACK_max_83 9_WIDTH_3_](https://user-images.githubusercontent.com/38702786/166952887-0f76dcad-71d3-41ab-98b2-1f6ed055f62e.png)
![FC_all_VertAvg_10_BLACK_avgx2_1 65_WIDTH_3_](https://user-images.githubusercontent.com/38702786/166952888-7e1b1662-3104-4861-9fd8-f2213993de74.png)
![FC_all_VertAvg_10_BLACK_max_181 3_WIDTH_3_](https://user-images.githubusercontent.com/38702786/166952890-16a200bb-8eaa-4b82-a6e1-bce5060a857a.png)
![FC_20-40_VertAvg_10_BLACK_avgx2_0 06_WIDTH_3_](https://user-images.githubusercontent.com/38702786/166952892-d7d814f5-222a-489b-907f-9ed8ddf2c21c.png)
