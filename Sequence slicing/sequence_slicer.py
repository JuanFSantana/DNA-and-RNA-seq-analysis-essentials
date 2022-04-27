"""
@author: Juan F. Santana, Ph.D.
"""

import pandas as pd
import sys

def position_converion(base1, base2, length):
    if int(base1) >= int(base2):
        return "Slicing position 2 should be greater than position 1"
    
    if int(base1) < 0 and int(base2) < 0:
        first_base = (length/2) - abs(int((base1)))  
        second_base = (length/2) - abs(int(base2)) + 1

    elif int(base1) > 0 and int(base2) > 0:
        first_base = abs(int(base1)) + (length/2) - 1 
        second_base = (length/2) + abs(int(base2))
    
    elif int(base1) < 0 and int(base2) > 0:
        first_base = (length/2) - abs(int(base1))        
        second_base = (length/2) + abs(int(base2))
        
    return int(first_base), int(second_base)

def main(args):

    file_name,seq_col_name,sort_by_col_name,percents,slicing_region = args 
    
    seq_col_name = seq_col_name.split(",")
    sort_by_col_name = sort_by_col_name.split(",")
    percents = percents.split(",")
    slicing_region = slicing_region.split(",")
    

    cols_to_use = seq_col_name + sort_by_col_name
    file = pd.read_csv(file_name, sep="\t", header=0, usecols=cols_to_use)
    original_df_total_rows = file.shape[0]

    percentages = []
    for each_percent in range(0,len(percents),2):
        start_percent = int((int(percents[each_percent])*len(file[seq_col_name]))/100)
        end_percent = int((int(percents[each_percent+1])*len(file[seq_col_name]))/100)
        percentages.append((start_percent,end_percent))

    sliced_list = []
    for fact in sort_by_col_name:
         for per in percentages:
                for pos in range(0,len(slicing_region),2):
                    file_sorted = file[[fact,seq_col_name[0]]].sort_values(by=[fact], ascending=False).reset_index(drop=True)
                    # split sequences in "_" and keep both sides (TSR and sequence), slice list based on percentage
                    sliced_seq_df = file_sorted[seq_col_name[0]].str.split(pat="_", expand=True)[per[0]:per[1]].reset_index(drop=True)
                    # convert genomic position into position base position in the sequence
                    position_one, position_two = position_converion(slicing_region[pos], slicing_region[pos+1], len(sliced_seq_df[1][0]))
                    # slice sequence base on converted base position
                    sliced_seq_df["2"] = sliced_seq_df[1].str.slice(position_one, position_two, 1)
                    # append factor, percents (natural numbers) and dataframes to list
                    sliced_list.append([fact] + [per] + [sliced_seq_df] + [slicing_region[pos]] + [slicing_region[pos+1]])         
    # Writer for excel
    writer = pd.ExcelWriter("Seq_slicing" + "-" + str(percents) + "%" + ".xlsx", engine='xlsxwriter')

    # Making an excel file with multiple sheets
    for num,each_final_df in enumerate(sliced_list):
        # Shape of individual df 
        total_rows = each_final_df[2].shape[0]
        # add column titles
        each_final_df[2].columns = ["TSR", "Ori.seq", "Sliced_seq"]
        # join TSR column with sliced seq column
        df_without_orig_seq = each_final_df[2]["TSR"] + "_" + each_final_df[2]["Sliced_seq"] 
        df_without_orig_seq = pd.DataFrame(df_without_orig_seq)
        regions = str(each_final_df[3]) + " to " + str(each_final_df[4])
        df_without_orig_seq.columns = [regions]

        # add data to excel
        df_without_orig_seq.to_excel(writer, sheet_name=each_final_df[0]+"-"+str(round((each_final_df[1][0]/original_df_total_rows)*100)) + "-" + str(round((each_final_df[1][1]/original_df_total_rows)*100)) + "%"+str(num))

    # Close the Pandas Excel writer and output the Excel file
    writer.save()

if __name__ == '__main__':
    main(sys.argv[1:])
