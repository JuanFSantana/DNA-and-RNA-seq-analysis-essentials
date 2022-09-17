# I have created an updated version of the fragMap program with more capabilities and much faster #

Please see: https://github.com/P-TEFb/fragMap

Example output: PolII_fragMap_20-400_Max_68609_X_1 0_Y_4 (Pol II DFF-Seq performed on HFF cells ([Spector et al., 2022](https://www.nature.com/articles/s41467-022-29739-x)) over +/- 1000 bp regions from the MaxTSS of 12,229 genes obtained from PRO-Cap performed on HFF cells ([Nilson et al., 2022](https://doi.org/10.1093/nar/gkac678))).
![PolII_fragMap_Custom_20-400_Max_68609_X_1 0_Y_4 0_](https://user-images.githubusercontent.com/38702786/190675335-1b8271ef-a0f7-449e-9ac3-aeee7dca6611.png)



# Older version: fragmap.py #
This script will create fragment heatmaps as described here [Spector et al., 2022](https://www.nature.com/articles/s41467-022-29739-x) and here [Santana et al., 2022](https://academic.oup.com/nar/advance-article/doi/10.1093/nar/gkac678/6659871?guestAccessKey=88024805-7d8e-4421-a032-dbef1c737757). Best used for unstranded data such as ChIP-seq.

# File requirements #
The input file should be a tab delimited file that contains the start and end of fragments/reads that overlap to the region of interest where the center is the feature under study (e.g. TSSs). [Bedtools intersect](https://bedtools.readthedocs.io/en/latest/content/tools/intersect.html) should be used to determine this overlap and obtain the following required type file required as input for **fragmap.py**:

| chr6 | 142946246 | 142946446 | Gene_A | 102 | - | chr6 | 142946247 | 142946248 | A00876:119:HW5F5DRXX:2:2207:29170:1157 | 255 | - |
| ---- |:---------:|:---------:|:------:|:---:|:-:|:----:|:---------:|:---------:|:--------------------------------------:|:---:|:-:|


# Behavior #
This approach allows the visualization of the distribution of DNA fragments of various lengths (y-axis) relative to a feature of interest present in the center of a chosen region (x-axis). Fragment lengths and black values are optionalities. 

# Dependencies #
### Python libraries ###
Pandas: https://pypi.org/project/pandas/

Numpy: https://pypi.org/project/numpy/

Matplotlib: https://matplotlib.org/stable/users/installing/index.html

# Example of arguments #
```
python fragmap.py <File> \
                  <Black values> \
                  <Fragment lengths> \
                  <Output directory> \
                  <Heatmap width> \

Example command usage: 
python fragmap.py plusminus100.bed \
                  max \
                  20-200 \
                  /Desktop/Heatmaps \
                  1

```
# Parameter description #
```
File: <str> file formatted as described above.

Black values: Max value optionalities are "max" or avgx<int> or avgy<int>. "max" is the largest value present in the heatmap. avgx<int/float> is the average of the heatmap times an integer. avgy<int/float> is the average of the heatmap divided by an integer. The darkest pixel is assigned to the max value indicated while white is zero. A gradient of white to black is proporionally determined for the rest of the values in the heatmap.

Fragment lengths: Comma separated fragment lengths to be used for calculating the centers. The options can be a <str> all and/or <int>-<int>.

Output directory: <str> The output heatmaps will be deposited in this path. 

Heatmap width: <positive int> The number of pixels per base position.
```
Output from example command usage: TBP-DFF-Seq data from [Spector et al., 2022](https://www.nature.com/articles/s41467-022-29739-x) for a +/- 100 bp region relative to the TSS of 10,273 transcription start regions (TSRs) identified here (paper under revision).

Heatmaps: frag.length 20-200, black.val max  


![Picture3](https://user-images.githubusercontent.com/38702786/166994030-a9cf399c-eb39-4d0b-8861-08b6d7924d38.png) 




