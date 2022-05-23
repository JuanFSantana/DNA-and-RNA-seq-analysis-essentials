"""
@author: Juan F. Santana, Ph.D.
"""
import re
import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt

class Heatmap:
    def __init__(self, PATH, OUTPUT_DIR, FRAG_SIZE, BLACK_MAX, VERTICAL_AVG, WIDTH):
        self.FRAG_SIZE = FRAG_SIZE
        self.BLACK_MAX = int(BLACK_MAX)
        self.VERTICAL_AVG = int(VERTICAL_AVG)
        self.WIDTH = int(WIDTH)
        self.PATH = PATH
        self.OUTPUT_DIR = OUTPUT_DIR

    def __str__(self):
       return(f'PATH:{self.PATH}\nOUTPUT_DIR:{self.OUTPUT_DIR}\nFRAG_SIZE:{self.FRAG_SIZE}\nBLACK_MAX:{self.BLACK_MAX}\nVERTICAL_AVG:{self.VERTICAL_AVG}\nWIDTH:{self.WIDTH}')
        
    def modifyTable(self):
        df_bedtools = pd.read_csv(self.PATH, sep="\t", header=None)
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
        return df_bedtools

    def findCenters(self, df_bedtools):
        sizes = self.FRAG_SIZE.split("-")
        
        # Filter based on frag.size
        if int(sizes[0]) > int(sizes[1]):
                raise ValueError ("Fragment size range is incorrect")
        else:
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

            final_df = df_TBP_centers_coordinate.loc[(df_bedtools['Fragment_size'] >= int(sizes[0])) & (df_TBP_centers_coordinate['Fragment_size'] <= int(sizes[1])) & (df_TBP_centers_coordinate['Position_Left'] > -1)].reset_index(drop=True)

        return df_TBP_centers_coordinate,final_df
    
    def rollingAverage(self, data):
        # Rolling average
        df_avg = data.rolling(self.VERTICAL_AVG, axis=0).mean()
        # Get rid of null rows
        df_final_avg_dropped_na = df_avg.dropna(axis=0, how='any')
        # Select rows that have the avg. needed present every X rows
        df_final_avg_dropped_na = df_final_avg_dropped_na.iloc[::self.VERTICAL_AVG]
        array_to_image = np.array(df_final_avg_dropped_na)   
        if self.WIDTH > 1:
            array_to_image = np.repeat(array_to_image, self.WIDTH, axis=1) 
        return array_to_image
    
    def colorHeatmap(self, frame):
        array_average = np.mean(frame)
        return array_average * self.BLACK_MAX
    
    def makeHeatmap(self, corrfactor, array):
        vmax = corrfactor
        vmin = 0
        cmap = 'binary'
        
        image_path = os.path.join(self.OUTPUT_DIR,"_".join([r"FragCenter", self.FRAG_SIZE,"MAX", str(round(corrfactor,2)), "VertAvg", str(self.VERTICAL_AVG), "WIDTH", str(self.WIDTH), ".tiff"]))

        plt.imsave(fname=image_path, arr=array, vmin=vmin, vmax=vmax, cmap=cmap, format='tiff')    
        
        plt.close()      

    @classmethod
    def get(cls):
        with open("heatmap_arguments.txt", "r") as file:
            arguments = []
            
            for strings in file.readlines():
                lines = re.split(r'=', strings.strip())
                
                if len(lines) != 2:
                    raise ValueError("Number of arguments is incorrect")
                            
                for row_arg in lines[1:]:
                    arguments.append(row_arg.strip())
        
        return cls(arguments[0], arguments[1], arguments[2], arguments[3], arguments[4], arguments[5])

def main():
    heat = Heatmap.get()
    table = heat.modifyTable()
    originalTable, centers = heat.findCenters(table)
    matrix = makeDict(originalTable, centers)
    averaged_matrix = heat.rollingAverage(matrix)
    heatmap_intensity = heat.colorHeatmap(averaged_matrix)
    output_heatmap = heat.makeHeatmap(heatmap_intensity, averaged_matrix)


def makeDict(arrayDict,filtered_df_TBP_centers_coordinate):
    # number of base positions
    num_bases = int(arrayDict["End"][0] - arrayDict["Start"][0])
    
    tsr_dict = {tsr: [0]*num_bases for tsr in arrayDict["TSR"].values}
    # sum the number of times a frag. center is present at a given position for a TSR/gene
    for tsr,left,right in zip(filtered_df_TBP_centers_coordinate["TSR"],filtered_df_TBP_centers_coordinate["Position_Left"], filtered_df_TBP_centers_coordinate["Position_Right"]):
        if left == right:
            tsr_dict[tsr][int(left)] += 2

        else:
            tsr_dict[tsr][int(left)] += 1
            tsr_dict[tsr][int(right)] += 1

    dataframe = pd.DataFrame(tsr_dict).T  
    return dataframe
    
if __name__ == '__main__':
    main()
