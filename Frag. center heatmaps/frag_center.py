"""
@author: Juan F. Santana, Ph.D.
"""

import pandas as pd
import numpy as np
import os
import sys
import subprocess
from PIL import Image, ImageOps
import PIL.ImageOps  


def main(args):
    
    file_name,frag_size,black_value,vertical_average,output_directory,heatmap_width = args
    
    frag_size = frag_size.split(",")
    black_value = black_value.split(",")
    vertical_average = int(vertical_average)
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
    df_bedtools["Fragment_size"] = (df_bedtools["End_read"] - df_bedtools["Start_read"])

    # Calculate fragment centers    
    df_bedtools['Center_Left'] = np.where(df_bedtools["Fragment_size"].values % 2 == 0, df_bedtools["Start_read"] + ((df_bedtools["Fragment_size"] / 2) - 1), df_bedtools["Start_read"] + (df_bedtools["Fragment_size"] / 2) - 0.5)
    df_bedtools['Center_Right'] = np.where(df_bedtools["Fragment_size"].values % 2 == 0, df_bedtools["Start_read"] + (df_bedtools["Fragment_size"] / 2), df_bedtools['Center_Left'])

    # Convert fragment centers coordinate to distance from Start_region
    df_TBP_centers_coordinate = df_bedtools.copy()
    
    conditions_left = [
    (df_TBP_centers_coordinate["Center_Left"].values >= df_TBP_centers_coordinate["Start"].values) & (df_TBP_centers_coordinate["Center_Right"].values < df_TBP_centers_coordinate["End"].values) & (df_TBP_centers_coordinate['Strand']=='+'),
    (df_TBP_centers_coordinate["Center_Right"].values >= df_TBP_centers_coordinate["End"].values) & (df_TBP_centers_coordinate["Center_Left"].values < df_TBP_centers_coordinate["Start"].values) & (df_TBP_centers_coordinate['Strand']=='-') 
    ] 

    choices_left = [
    df_TBP_centers_coordinate["Center_Left"] - df_TBP_centers_coordinate["Start"],
    (df_TBP_centers_coordinate["End"] - df_TBP_centers_coordinate["Center_Left"])-1 # substracting 1 to invert coordinate with coordinate right
    ]

    df_TBP_centers_coordinate['Position_Left'] = np.select(conditions_left, choices_left, default=-1)


    conditions_right = [
    (df_TBP_centers_coordinate["Center_Left"].values >= df_TBP_centers_coordinate["Start"].values) & (df_TBP_centers_coordinate["Center_Right"].values < df_TBP_centers_coordinate["End"].values) & (df_TBP_centers_coordinate['Strand']=='+'),
    (df_TBP_centers_coordinate["Center_Right"].values >= df_TBP_centers_coordinate["End"].values) & (df_TBP_centers_coordinate["Center_Left"].values < df_TBP_centers_coordinate["Start"].values) & (df_TBP_centers_coordinate['Strand']=='-') 
    ] 

    choices_right = [
    df_TBP_centers_coordinate["Center_Right"] - df_TBP_centers_coordinate["Start"],
    (df_TBP_centers_coordinate["End"] - df_TBP_centers_coordinate["Center_Right"])+1 # adding 1 to invert coordinate with coordinate left
    ]

    df_TBP_centers_coordinate['Position_Right'] = np.select(conditions_right, choices_right, default=-1)
    
    # number of base positions
    num_bases = int(df_TBP_centers_coordinate["End"][0] - df_TBP_centers_coordinate["Start"][0])
    
    # select fragment sizes
    for frags in frag_size:
        # make dict
        tsr_dict = {tsr: [0]*num_bases for tsr in df_TBP_centers_coordinate["TSR"].values}
        
        if frags == "all":
            filtered_df_TBP_centers_coordinate = df_TBP_centers_coordinate.loc[df_TBP_centers_coordinate['Position_Left'] > -1].reset_index(drop=True)
            
        else:
            lengths = frags.split("-")

            size_left = int(lengths[0]) # inlcusive
            size_right = int(lengths[1]) # inclusive
            if size_left > size_right:
                return print("Fragment size range is incorrect")
            filtered_df_TBP_centers_coordinate = df_TBP_centers_coordinate.loc[(df_TBP_centers_coordinate['Fragment_size'] >= size_left) & (df_TBP_centers_coordinate['Fragment_size'] <= size_right) & (df_TBP_centers_coordinate['Position_Left'] > -1)].reset_index(drop=True)
            
        # sum the number of times a frag. center is present at a given position for a TSR/gene
        for tsr,left,right in zip(filtered_df_TBP_centers_coordinate["TSR"],filtered_df_TBP_centers_coordinate["Position_Left"], filtered_df_TBP_centers_coordinate["Position_Right"]):
            if left == right:
                tsr_dict[tsr][int(left)] += 2

            else:
                tsr_dict[tsr][int(left)] += 1
                tsr_dict[tsr][int(right)] += 1

        df_final = pd.DataFrame(tsr_dict).T  
        
        for black_val in black_value:
            # Performing averages
            # Rolling average every 10 bases per 10 rows
            df_avg = df_final.rolling(vertical_average, axis=0).mean()
            # Get rid of null rows
            df_final_avg_dropped_na = df_avg.dropna(axis=0, how='any')
            # Select rows that have the avg. needed present every X rows
            df_final_avg_dropped_na = df_final_avg_dropped_na.iloc[::vertical_average]
            
            # Get the mean
            mean_df_final_avg_dropped_na = np.mean(df_final_avg_dropped_na.values)
            
            if type(black_val) == float or type(black_val) == int:
                num_to_correct = float(black_val)
                array_to_image = df_final_avg_dropped_na.where(df_final_avg_dropped_na < num_to_correct, num_to_correct)
                df_array_to_image = pd.DataFrame(array_to_image)              
            
            elif black_val[0:3] == "avg":
                corr_fact = float(black_val[-1])
                
                if black_val[-2] == "x":
                    num_to_correct = float(mean_df_final_avg_dropped_na*corr_fact)
            
                elif black_val[-2] == "y":
                    num_to_correct = float(mean_df_final_avg_dropped_na/corr_fact)
                    
                # change max values: where the condition is false values are replaced by the second number
                array_to_image = df_final_avg_dropped_na.where(df_final_avg_dropped_na < num_to_correct, num_to_correct)
                df_array_to_image = pd.DataFrame(array_to_image)         
            
            elif black_val == "max":
                array_to_image = df_final_avg_dropped_na
                df_array_to_image = pd.DataFrame(array_to_image) 
                # df.max() give you a Series containing the maximum values for each column. Therefore series.max() gives you the maximum for the whole dataframe
                num_to_correct = float(np.max(df_final_avg_dropped_na.values))        

     
            # Convert df to np array
            np_final_avg_dropped_na = np.array(array_to_image)
            # Normalize the array by the max number (later conversion of np array to dtype=unit8 covers the range from 0 to 255)
            normalized_np_final_avg_dropped_na = (np_final_avg_dropped_na/(np_final_avg_dropped_na.max()))*255 
            
            if heatmap_width > 1:
                normalized_np_final_avg_dropped_na = np.repeat(normalized_np_final_avg_dropped_na, heatmap_width, axis=1)
            # Convert to unit8 type
            nd_norm = np.array(normalized_np_final_avg_dropped_na, dtype=np.uint8)
            
            # Make heatmaps
            # Make image
            im = Image.fromarray(nd_norm)
            # Path
            num_to_correct_rounded = round(num_to_correct, 2)
            image_path = os.path.join(output_directory,"_".join([r"FC", str(frags), "VertAvg", str(vertical_average), "BLACK", str(black_val), str(num_to_correct_rounded), "WIDTH", str(heatmap_width), ".tiff"]))            
            # Invert balck/white
            inverted_image = PIL.ImageOps.invert(im)

            inverted_image.save(image_path, dpi=(600, 600), quality=95, subsampling=0)      
            inverted_image.close()
          
#fragCenters("plusminus100.bed", [("all"),(20,40),(70,80)], ["avgx2", "max"], 10, r'C:\Users\Juan\Desktop\CS1210\Genomics Functions\Heatmaps', 3)


if __name__ == '__main__':
    main(sys.argv[1:])
