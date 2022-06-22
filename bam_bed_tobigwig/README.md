# bam_bed_tobigwig.py #
This script will create bigWig tracks of fragments of user specified sizes from BAM or BED files. Best used for data from ChIP-seq as strandedness is not taken into account when making the tracks. 

# File requirements #
1) BAM or BED file
2) chromsome size file.   

# Behavior #
The user can specifiy multiple tracks to be created from different fragment sizes. The output of this script is a directory named 'bigWig' containing each of the bigWig tracks.

# Dependencies #
### Python libraries ###
Pandas: https://pypi.org/project/pandas/

Numpy: https://pypi.org/project/numpy/

### Programs ###
bedtools: https://bedtools.readthedocs.io/en/latest/index.html

samtools: http://www.htslib.org/

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
BAM/BED file: <str> Either BAM or BED file can be used as input. The BAM file does not have to be sorted.

Chromosome size file: <str> The same chromosome size file used for mapping. 

Fragment size intervals: <int> Space delimited pair of numbers that indicate the fragment sizes to filter the BAM or BED file by to make the bigWig tracks. The lower and upper bound of the intervals are inclusive. Multiple intervals at once can serve as input (as shown in the example above).

Threads: <int> Threads to use.

Spike-in/normalization factor: <float> Each count value per base is multiplied by this factor.
```


