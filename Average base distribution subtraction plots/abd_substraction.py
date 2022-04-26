"""
@author: Juan F. Santana, Ph.D.
"""

import pandas as pd   
import numpy as np 
import sys

def count_each_base(all_sequences):
    
    array_count = np.zeros([4,len(all_sequences[0])])

    # Count each instance of a base per position and store in base_count_dict
    for line in all_sequences:
        line = np.array(line, dtype='c')
        for num,base_per_seq in enumerate("ATGC"):
            array_count[num]+= line == bytes(base_per_seq, 'utf-8')

    array_average = array_count / len(all_sequences)
   
    return array_average 

def output_data(averages_substracted, size_of_list, start_percentile_1, end_percentile_1, start_percentile_2, end_percentile_2):
    
    df_transpose = pd.DataFrame(averages_substracted).T
    df = df_transpose.rename(columns={
        0:"A", 
        1:"T", 
        2:"G", 
        3:"C"
    })
    
    positions = []
    # sequence length must be even, with maxTSS in +1
    for i in range(-(int(len(size_of_list[0])/2)), int(len(size_of_list[0])/2)+1):
        if i == 0:
            continue
        positions.append(i)
    df["Position"] = positions
    df.set_index('Position', inplace=True)

    return df
    
def main(args): 
    file1,column_name_to_sort,column_name_sequences,percent = args
    factor_cols = column_name_to_sort.split(",")

    col_list = factor_cols + [column_name_sequences]

    # Writer for excel
    writer = pd.ExcelWriter("ABD_"+ "Top_minus_Bottom" + "_" + str(percent) + "%" + ".xlsx", engine='xlsxwriter')
    
    # Calculate the different %s
    file_1_start_percent = int(0)
    file_1_end_percent = int(percent)
    file_2_start_percent = 100 - int(percent)
    file_2_end_percent = int(100)
    
    # Upload dataset and turn percents into whole numbers
    file_1_df = pd.read_csv(file1, sep="\t", header=0, usecols=col_list)
    start_1, end_1, start_2, end_2 = int((file_1_start_percent*len(file_1_df[column_name_sequences]))/100), int((file_1_end_percent*len(file_1_df[column_name_sequences]))/100), int((file_2_start_percent*len(file_1_df[column_name_sequences]))/100), int((file_2_end_percent*len(file_1_df[column_name_sequences]))/100)
    
    # Sorting, slicing datasets top and bottom for each factor
    final_dfs = []
    for fact in factor_cols:
        # sort by factor
        file_1_sequences_and_tsr_df = file_1_df[[fact,column_name_sequences]].sort_values(by=[fact], ascending=False).reset_index(drop=True)
        # split sequences and slice dataset
        fact_top = file_1_sequences_and_tsr_df[column_name_sequences].str.split("_")[start_1:end_1].str[1].reset_index(drop=True)
        fact_bot = file_1_sequences_and_tsr_df[column_name_sequences].str.split("_")[start_2:end_2].str[1].reset_index(drop=True)
        # call function to calculate number of bases and their fraction
        base_averages_top = count_each_base(fact_top)
        base_averages_bottom = count_each_base(fact_bot)        
        # Substract top minus bottom numpy arrays for each factor and create dfs
        substraction = base_averages_top - base_averages_bottom
        # Call function to make final dfs
        final = output_data(substraction, fact_top, file_1_start_percent, file_1_end_percent, file_2_start_percent, file_2_end_percent) 
        final_dfs.append(final)

    # Making an excel file with multiple sheets and charts
    for each_final_df in range(len(final_dfs)):
        final_dfs[each_final_df].to_excel(writer, sheet_name=factor_cols[each_final_df]+"_top " + str(percent) +"% minus bottom " + str(percent) +"%")
        
        # Access the XlsxWriter workbook and worksheet objects from the dataframe
        sheet_name = factor_cols[each_final_df]+"_top " + str(percent) +"% minus bottom " + str(percent) +"%"
        workbook = writer.book
        worksheet = writer.sheets[factor_cols[each_final_df]+"_top " + str(percent) +"% minus bottom " + str(percent) +"%"]
        
        # Create a chart object
        chart = workbook.add_chart({
            'type': 'scatter',
            'subtype':'straight'
            })
        
        # Shape of individual df and colors to use for each line
        total_rows, total_cols = final_dfs[0].shape
        line_colors = ["#CC0000", "#008000", "#FFB300", "#0000CD"]
        
        # Configure the series of the chart from the dataframe data
        for i in range(total_cols): # range must be the total number of columns not counting the first (x axis)
            col = i + 1
            chart.add_series({
                'name':       [sheet_name, 0, col], # Column titles used for the legend
                'categories': [sheet_name, 1, 0, total_rows, 0], # first num=row num, second=col num, third=row num, fourth=col num ==== extend of the data
                'values':     [sheet_name, 1, col, total_rows, col], # plotting each column (starting on the second one) 
                'line':       {
                    "width":1,
                    'color': line_colors[i]
                    }
            })

        chart.set_x_axis({
            'name': 'Position',
            'min':-(total_rows/2),
            'max':total_rows/2,
            'name_font': {
                "name":"Arial",
                'size': 12,
                },
            'crossing':'min',
            'num_font':  {
                'name': 'Arial', 
                'size': 9
                }
            })
        
        chart.set_y_axis({
            'name': 'Fraction of each base',
            'name_font': {
                "name":"Arial",
                'size': 12
                },
            "crossing":"min",
            'num_font':  {
                'name': 'Arial', 
                'size': 9
                },
            'major_gridlines': {
                'visible': False,
                }
            })
        
        chart.set_chartarea({
            'border': {
                'none': True
                }
            })
        
        chart.set_size({
            'x_scale': 1.5, 
            'y_scale': 2
            })
        
        # Insert the chart into the worksheet
        worksheet.insert_chart('G2', chart)
  
    # Close the Pandas Excel writer and output the Excel file
    writer.save()

if __name__ == '__main__':
    main(sys.argv[1:])
