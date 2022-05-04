"""
@author: Juan F. Santana, Ph.D.
"""

import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt

def main(args):
    
    file_names,name,blackVal_logColor,vertical_average,output_directory,heatmap_width = args

    file_names = file_names.split(",")
    name = name.split(",")
    blackVal_logColor = blackVal_logColor.split(",")
    vertical_average = int(vertical_average)
    heatmap_width = int(heatmap_width)
    
    if len(file_names) % 2 != 0:
        return print("Missig files: must be pairs")
    if len(name) == 0:
        return print("Add a list of names")
    if len(file_names) == 2:
        if len(name) != 3:
            return print("Number of names do not match number files that will be generated")
    else:
        if (len(file_names)/2)*3 != len(name):
            return print("Number of names do not match number files that will be generated")            

    counter=0
    for dataset_number in range(0, int(len(file_names)),2):  
        df_dmso = pd.read_csv(file_names[dataset_number], sep="\t", header=None)
        df_vhl = pd.read_csv(file_names[dataset_number+1], sep="\t", header=None)
        
        df_lists = []
        for dataset in [df_dmso,df_vhl]:
            del dataset[4]
            del dataset[9]
            del dataset[10]
            dataset.rename(columns={
                0:"Chromosome",
                1:"Start", 
                2:"End", 
                3:"TSR",
                5:"Strand",
                6:"Chrom_bedtools",
                7:"Start_read",
                8:"End_read",
                11:"Strand_read",
                12:"Base_overlap"},
                inplace=True)   

            # Convert coordinate to distance from Start_region
            dataset['Position_Left'] = np.where(dataset["Strand"] == "+", dataset["Start_read"] - dataset["Start"], dataset["End"] - dataset["End_read"] )
            dataset['Position_Right'] = np.where(dataset["Strand"] == "+", (dataset["Start_read"] - dataset["Start"]) + 1, (dataset["End"] - dataset["End_read"]) + 1)

            # make a dictionary with each TSR (or any other identifier)
            num_bases = (dataset["End"][0] - dataset["Start"][0]) 

            tsr_dict = {tsr: [0]*num_bases for tsr in dataset["TSR"].values}

            for tsr,left in zip(dataset["TSR"],dataset["Position_Left"]):
                tsr_dict[tsr][int(left)] += 1
            # convert dict into dataframe
            df_final = pd.DataFrame(tsr_dict).T  
            df_lists.append(df_final)
 
        # make individual arrays for control and treatment
        dmso_array = np.array(df_lists[0], dtype=float)
        vhl_array = np.array(df_lists[1], dtype=float)
        division = np.divide(dmso_array, vhl_array, out=np.array(dmso_array), where=vhl_array!=0, dtype=float)
        division_log2 = np.log2(division, out=np.array(division), where=division!=0, dtype=float)
        
        dmso_max_for_vhl = [] 
        for num_array,each_array in enumerate([dmso_array,vhl_array,division_log2]):
            new = pd.DataFrame(each_array)
            df_avg = new.rolling(vertical_average, axis=0).mean()
            df_final_avg_dropped_na = df_avg.dropna(axis=0, how='any')
            df_final_avg_dropped_na_selected = df_final_avg_dropped_na.iloc[::vertical_average]
            array_to_image = np.array(df_final_avg_dropped_na_selected)
            
            if heatmap_width > 1:
                array_to_image = np.repeat(array_to_image, heatmap_width, axis=1) 

            height,width = array_to_image.shape
            
            counter2=0
            for maxes in range(0,len(blackVal_logColor),2):

                if blackVal_logColor[maxes].lower() == "max":
                    bw_max_val = np.max(array_to_image)

                elif blackVal_logColor[maxes][0:3].lower() == "avg":
                    if blackVal_logColor[maxes][-2].lower() == "x":
                        corr_fact = float(blackVal_logColor[maxes][-1])
                        array_average = np.mean(array_to_image)
                        bw_max_val = array_average*corr_fact
                      
                    elif blackVal_logColor[maxes][-2].lower() == "y":
                        corr_fact = float(blackVal_logColor[maxes][-1])
                        array_average = np.mean(array_to_image)
                        bw_max_val = array_average/corr_fact 

                # Make the heatmap
                if num_array == 0:
                    vmax = bw_max_val
                    vmin = 0
                    dmso_max_for_vhl.append(bw_max_val)
                    cmap = 'binary'

                elif num_array == 1:
                    vmax = dmso_max_for_vhl[counter2]
                    vmin = 0
                    cmap = 'binary'

                elif num_array == 2:
                    vmax = int(blackVal_logColor[maxes+1])
                    vmin = -(vmax)
                    cmap = 'bwr_r'

                # save heatmap
                image_path = os.path.join(output_directory,"_".join([r"Heatmap", str(name[counter]),"MAX", str(maxes), "VertAvg", str(vertical_average), "WIDTH", str(heatmap_width), ".tiff"]))
                                     
                plt.imsave(fname=image_path, arr=array_to_image, vmin=vmin, vmax=vmax, cmap=cmap, format='tiff')         

                plt.close()
                
                counter2+=1
            counter+=1

if __name__ == '__main__':
    main(sys.argv[1:])
    
