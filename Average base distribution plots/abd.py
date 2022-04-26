"""
@author: Juan F. Santana, Ph.D.
"""

import pandas as pd   
import numpy as np 
import sys

def count_each_base(all_sequences):
    
    array_count = np.zeros([4,len(all_sequences[0])])

    for line in all_sequences:
        line = np.array(line, dtype='c')
        for num,base_per_seq in enumerate("ATGC"):
            array_count[num]+= line == bytes(base_per_seq, 'utf-8')

    array_average = array_count / len(all_sequences)
   
    return array_average 

def output_data(averages, size_of_list):
    df_transpose = pd.DataFrame(averages).T
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
    file1,column_name_to_sort,column_name_sequences,percent_list = args
    factor_cols = column_name_to_sort.split(",")
    percent_slice = percent_list.split(",")

    # lower the burden of the file to upload by selecting the columns
    col_list = factor_cols + [column_name_sequences]
    
    # Writer for excel
    writer = pd.ExcelWriter("ABD" + "-" + str(percent_slice) + "%" + ".xlsx", engine='xlsxwriter')

    # Upload dataset and turn percents into whole numbers
    file_1_df = pd.read_csv(file1, sep="\t", header=0, usecols=col_list)
    
    percentages = []
    for percent in range(0,len(percent_slice),2):
        num_seqs = int(len(file_1_df[column_name_sequences]))
        start_percent = (int(percent_slice[percent])*num_seqs)/100
        end_percent = (int(percent_slice[percent+1])*num_seqs)/100
        percentages.append((int(start_percent),int(end_percent)))

    # Sorting, slicing datasets top and bottom for each factor
    final_dfs = []
    for to_sort in factor_cols:
        for set_percent in percentages:
            file_1_sequences_and_tsr_df = file_1_df[[to_sort,column_name_sequences]].sort_values(by=[to_sort], ascending=False).reset_index(drop=True)

            sliced_seq_list = file_1_sequences_and_tsr_df[column_name_sequences].str.split("_")[set_percent[0]:set_percent[1]].str[1].reset_index(drop=True)

            base_averages = count_each_base(sliced_seq_list)

            final = output_data(base_averages, sliced_seq_list) 

            final_dfs.append(final)    

    # Making an excel file with multiple sheets and charts
    counter = 0
    for to_sort_again in factor_cols:
         for each_final_df in range(0,int((len(final_dfs)/len(factor_cols))+1),2):
            final_dfs[counter].to_excel(writer, sheet_name=to_sort_again+"-"+str(percent_slice[each_final_df])+"-"+str(percent_slice[each_final_df+1])+"%")
            counter += 1
            # Access the XlsxWriter workbook and worksheet objects from the dataframe
            sheet_name = to_sort_again+"-"+str(percent_slice[each_final_df])+"-"+str(percent_slice[each_final_df+1])+"%"
            workbook = writer.book
            worksheet = writer.sheets[to_sort_again+"-"+str(percent_slice[each_final_df])+"-"+str(percent_slice[each_final_df+1])+"%"]

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
