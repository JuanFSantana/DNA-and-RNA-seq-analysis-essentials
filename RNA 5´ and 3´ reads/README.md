
# prime3_5.py #
This script will yield two files each with the position of the 5´ or 3´ ends of reads from a bed file resulting from any type of RNA-seq experiment (PRO-seq, GRO-seq, etc). The output will be stranded. Currently, the script removes moth reads used as spike-in in XXXXXXXX. It can be modified to remove any other organism used as spike-in.

# File requirements #
The input file should be a bed file containing the first six columns. 

# Dependencies #
### Python libraries ###
Pandas: https://pypi.org/project/pandas/

Numpy: https://pypi.org/project/numpy/

Operating system (OS): https://pypi.org/project/os-sys/

# Example of arguments #
```
python prime3_5.py <File name> \
                   <Output 5´ name,  Output 3´ name> \

Example command usage: 
python prime3_5.py tbp_dmso_comb.bed \
                   tbp_5_dmso,tbp_3_dmso
```
# Parameter description #
```
File name: <str> Bed files containing the first six columns. More than one bed file can be used as input separated by a comma. 

Output 5´ name,  Output 3´ name: <str> Comma separated names for the output files. Two names per input bed file in order with the 5´ file name first followed by the name of the 3´ file.

```


