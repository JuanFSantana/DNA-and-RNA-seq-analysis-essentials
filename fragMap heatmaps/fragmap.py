"""
@author: Juan F. Santana, Ph.D.
"""

import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
import matplotlib.colors as colors
from pylab import * 


def main(args):
    
    file_name,black_value,frag_size,output_directory,heatmap_width = args

    black_value = black_value.split(",")
    frag_size = frag_size.split(",")
    heatmap_width = int(heatmap_width)
    
    df_bedtools = pd.read_csv(file_name, sep="\t", header=None)
    del df_bedtools[4]
    del df_bedtools[9]
    del df_bedtools[10]
    df_bedtools = df_bedtools.rename(columns={
        0:"Chromosome",
        1:"Start", 
        2:"End", 
        3:"TSR",
        5:"Strand",
        6:"Chrom_bedtools",
        7:"Start_read",
        8:"End_read",
        11:"Strand_read",
        12:"Base_overlap"
    })
    
    # Make a new column with fragment sizes
    df_bedtools["Fragment_size"] = df_bedtools["End_read"] - df_bedtools["Start_read"]
    
    # Convert intervals where one or both of the sides are smaller or larger than the region into the region limits 
    df_bedtools['New_Start'] = np.where(df_bedtools['Start_read'] < df_bedtools['Start'], df_bedtools['Start'], df_bedtools['Start_read'])
    df_bedtools['New_End'] = np.where(df_bedtools['End_read'] > df_bedtools['End'], df_bedtools['End'], df_bedtools['End_read'])
    region_size = int(df_bedtools['End'][0] - df_bedtools['Start'][0])

    # Convert coordinate to distance from Start_region
    df_bedtools['Position_Left'] = np.where(df_bedtools['Strand']=='+', (df_bedtools["New_Start"] - df_bedtools["Start"]), df_bedtools["End"] - df_bedtools["New_End"])
    df_bedtools['Position_Right'] = np.where(df_bedtools['Strand']=='+', (df_bedtools["New_End"] - df_bedtools["Start"]), df_bedtools["End"] - df_bedtools["New_Start"])

    # Sort dataframe by fragment size (small->big)
    df_bedtools_filtered = df_bedtools.sort_values(by=["Fragment_size"], ascending=True, ignore_index=True)

    # Vectorize to add a column that adds a list per row containing 1 for each base convered by the fragment
    def value_per_base(row):
        # make an array of size of the region to be analyzed
        np_array = np.zeros([region_size])
        # Add a 1 to each position in the array for the length of the fragment
        np_array[row['Position_Left']:row['Position_Right']] = 1
        return np_array

    df_bedtools_filtered['Bases'] = df_bedtools_filtered.apply(value_per_base, axis=1)    
    
    # select fragment sizes
    for frags in frag_size: 
        if frags == "all":
            df_bedtools_filtered = df_bedtools_filtered
            
        else:
            lengths = frags.split("-")

            size_left = int(lengths[0]) # inlcusive
            size_right = int(lengths[1]) # inclusive
            if size_left > size_right:
                return print("Fragment size range is incorrect")            

            df_bedtools_filtered = df_bedtools_filtered.loc[(df_bedtools_filtered['Fragment_size'] >= size_left) & (df_bedtools_filtered['Fragment_size'] <= size_right)].reset_index(drop=True)
   
        
        # Group dataframe by TSR and add the values for each base position
        df_fragment_size_grouped = df_bedtools_filtered[['Fragment_size','Bases']].groupby(by='Fragment_size', sort=False).sum()
        
        # Convert list within row into separate columns/dataframe
        df_fragment_size_grouped_split = pd.DataFrame(df_fragment_size_grouped['Bases'].tolist())
        array_to_image = np.array(df_fragment_size_grouped_split)
        
        if heatmap_width > 1:
            array_to_image = np.repeat(array_to_image, heatmap_width, axis=1) 
            
        for black_val in black_value:  
            if black_val.lower() == "max":
                bw_max_val = np.max(array_to_image)

            elif black_val[0:3].lower() == "avg":
                if black_val[3].lower() == "x":
                    corr_fact = float(black_val[4:])
                    array_average = np.mean(array_to_image)
                    bw_max_val = array_average*corr_fact

                elif black_val[3].lower() == "y":
                    corr_fact = float(black_val[4:])
                    array_average = np.mean(array_to_image)
                    bw_max_val = array_average/corr_fact  
             
            vmax = bw_max_val
            vcenter = (bw_max_val/2)
            vmin = 0
            norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
            cmap = 'binary'
            
            image_path = os.path.join(output_directory,"_".join([r"FragMaps", str(frags),"MAX", str(black_val), "WIDTH", str(heatmap_width), ".tiff"]))
            plt.imsave(fname=image_path, arr=array_to_image, vmin=vmin, vmax=vmax, cmap=cmap, format='tiff') 
            
            plt.close()        

if __name__ == '__main__':
    main(sys.argv[1:])
