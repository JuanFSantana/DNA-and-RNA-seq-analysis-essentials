"""
@author: Juan
"""

import pandas as pd
import numpy as np
import sys

def main(args):
    
    files,names = args
    
    files = files.split(",")
    names = names.split(",")
    
    primes_list = []
    for dataset in files:
        df = pd.read_csv(dataset, sep="\t", header=None)
        df_human = df.drop(df[df[0] == "JQCY02.1"].index).reset_index(drop=True)
        df_human.columns = ["Chromsome", "Start", "End", "Read", "Score", "Strand"]
        
        five_prime = df_human.copy()
        three_prime = df_human.copy()
        
        five_prime['New_Start'] = np.where(five_prime["Strand"] == "+", five_prime['Start'], five_prime['End']-1)
        five_prime['New_End'] = np.where(five_prime["Strand"] == "+", five_prime['Start']+1, five_prime['End'])
        cols_five = five_prime.columns.tolist()
        cols_five = [cols_five[0]] + [cols_five[6]] + [cols_five[7]] + cols_five[3:6] 
        five_prime = five_prime[cols_five]
        primes_list.append(five_prime)
    
        three_prime['New_Start'] = np.where(three_prime["Strand"] == "+", three_prime['End']-1, three_prime['Start'])
        three_prime['New_End'] = np.where(three_prime["Strand"] == "+", three_prime['End'], three_prime['Start']+1)
        cols_three = three_prime.columns.tolist()
        cols_three = [cols_three[0]] + [cols_three[6]] + [cols_three[7]] + cols_three[3:6] 
        three_prime = three_prime[cols_three]
        primes_list.append(three_prime)
    
    for num, label in enumerate(names):
        primes_list[num].to_csv(str(names[num]) + ".bed", sep="\t", index=False, header=False)

if __name__ == '__main__':
    main(sys.argv[1:])
