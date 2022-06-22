"""
Juan F. Santana, Ph.D.

"""

import pandas as pd
import os
import sys
import argparse
import numpy as np
import shutil
import multiprocessing as mp
pd.options.mode.chained_assignment = None  # default='warn'


parser = argparse.ArgumentParser(prog='Fragment bam/bed to bigWig',
                                 description='Generate bigWig tracks with a specific fragment range',
                                 epilog='''A new directory, bigWig, containing the resulting bigWig track(s) 
                                 will be created in the current directory''')
parser.add_argument('bam_bed', type=str,
                    help='path to bam or bed file')
parser.add_argument('chromosome_sizes', type=str,
                    help='path to chrom_sizes file')
parser.add_argument('-r', '--range', type=int, nargs='+', metavar='LowerBound UpperBound',
                    help='Intervals are inlcusive', required=True)
parser.add_argument('-n', '--normalization', type=float, default=1.0,
                    help='Normalization factor')
parser.add_argument('-t', '--threads', type=int, default=1,
                    help='Threads to use')

if len(sys.argv[1:]) <= 3:
    sys.argv.append('--help')

args = parser.parse_args()

bam_file = args.bam_bed
ranges = args.range
chroms = args.chromosome_sizes
norm_factor = args.normalization
threads = args.threads

tmp_dir = os.path.join(os.getcwd(),'tmp_bigWig')
if not os.path.isdir(tmp_dir):
    os.makedirs(tmp_dir)
  
if not bam_file:
    sys.stderr.write('No bam/bed file found. Exiting ...\n')
    sys.exit(1)
    
elif not chroms:
    sys.stderr.write('No chromosome sizes file found. Exiting ...\n')
    sys.exit(1)
    
elif len(ranges) % 2 != 0:
    sys.stdout.write('Input range is not paired. Exiting ...\n')
    sys.exit(1)     
    
for num in range(0,len(ranges),2):
     x,y = ranges[num], ranges[num+1]
     if x > y:
         sys.stderr.write('Range is not correct. Exiting ...\n')
         sys.exit(1)          
# grab properly paired reads from a bam file, sort and make bedpe file         
if bam_file[-3:] == 'bam':        
    bed_path = os.path.join(tmp_dir,'myFile.bed')
    print('Making bed file...')  
    os.system(
        ' '.join(['samtools','view','-S','-u','-bf','0x2',bam_file,'|','samtools','sort','-n','/dev/stdin','--threads',str(threads),'|','bedtools','bamtobed','-i','stdin','-bedpe','-mate1','>',bed_path])
    )   
    print('Filtering fragment sizes...')
    # make bed file with the end with the lowest start coordinate reported first (convert negative strand ends)
    df = pd.read_csv(bed_path, sep="\t", header=None)
    s1 = np.where(df[8].values == '-', df[4], df[1])
    s2 = np.where(df[8].values == '-', df[2], df[5])
    df[1] = s1
    df[2] = s2
    df.drop([3,4,5,9], axis=1, inplace=True)

elif bam_file[-3:] == 'bed': 
    df = pd.read_csv(bam_file, sep="\t", header=None)
    print('Filtering fragment sizes...')
# calculate fragment sizes   
df['Fragment_size'] = df[2] - df[1]
    
def main(interval, df):
    left,right = interval

    data_min = int(df['Fragment_size'].min())
    data_max = int(df['Fragment_size'].max())
    
    if left < data_min and right > data_max:
        left = data_min
        right = data_max
        print('The fragment range selected is out of range: smallest and biggest fragments are {} and {}, respectively. The range was automatically set to {}-{}.'.format(data_min,data_max,data_min,data_max))
    
    elif left < data_min:
        left = data_min
        print('The fragment range selected is out of range: smallest and biggest fragments are {} and {}, respectively. The lower bound was automatically set to {}.'.format(data_min,data_max,data_min))
    
    elif right > data_max:
        right = data_max
        print('The fragment range selected is out of range: smallest and biggest fragments are {} and {}, respectively. The upper bound was automatically set to {}.'.format(data_min,data_max, data_max))            
        
    # filter dataset by fragment sizes and create temporary bed file    
    filtered_df = df[(df['Fragment_size'] >= left) & (df['Fragment_size'] <= right)].reset_index(drop=True)  
    filtered_df.drop(['Fragment_size'], axis=1, inplace=True)  
    bed_filtered_path = os.path.join(tmp_dir,'bed_filtered.bed')
    filtered_df.to_csv(bed_filtered_path, index=False, sep="\t", header=None)
    
    # sort bed file and create temporary sorted bed file
    sorted_bed_path = os.path.join(tmp_dir,str(left)+'-'+str(right)+'-'+'bed_filtered_sorted.bed')
    os.system(
        'LC_COLLATE=C sort -k 1,1 ' +bed_filtered_path+ ' --parallel ' + str(threads) +' > ' +sorted_bed_path
    ) 
    # create remporary bedgraph file    
    bedGraph_path = os.path.join(tmp_dir,str(left)+'-'+str(right)+'-'+'myFile.bedgraph')
    print('Making bedGraph file...')
    os.system(
        ' '.join(['bedtools genomecov -i', sorted_bed_path, '-g', chroms, '-bg', '-scale', str(norm_factor), '>', bedGraph_path])
    )   
    # sort bedgraph file and vreate temporary sorted bedgraph file
    sorted_bedGraph_path = os.path.join(tmp_dir,str(left)+'-'+str(right)+'-'+'myFile_sorted.bedgraph')
    os.system(
        'LC_COLLATE=C sort -k1,1 -k2,2n ' +bedGraph_path+ ' --parallel ' + str(threads) +' > ' +sorted_bedGraph_path
    )
    # create bigwig directory and make bigwig tracks
    bigWig_direc = os.path.join(os.getcwd(), 'bigWig')
    os.makedirs(bigWig_direc, exist_ok=True) 
    bigWig_file_name = os.path.basename(bam_file).replace(bam_file[-4:], '-'.join(['','frag_size',str(left),str(right)]) + '.bw')
    bigWig_path = os.path.join(bigWig_direc, bigWig_file_name)
    print('Making bigWig...')
    os.system(
        " ".join(['bedGraphToBigWig', sorted_bedGraph_path, chroms, bigWig_path])
    )
       
    print('All done for {}!'.format(bigWig_file_name))
    return tmp_dir
    

def delete_files(mydir):
    try:
        shutil.rmtree(mydir[0])
    except OSError as e:
        print ("Error: {} - {}.".format(e.filename, e.strerror))      
    
if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())
    docs = pool.starmap(main, [((ranges[num],ranges[num+1]), df) for num in range(0,len(ranges),2)])
    pool.close()
    delete_files(docs)
