"""
@author: Juan F. Santana, Ph.D.
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
        
        five_prime = df.copy()
        three_prime = df.copy()
        
        five_prime['New_Start'] = np.where(five_prime[6] == "+", five_prime[1], five_prime[2]-1)
        five_prime['New_End'] = np.where(five_prime[6] == "+", five_prime[1]+1, five_prime[2])
        five_prime = five_prime[[0,'New_Start', 'New_End', 3,4,5,6]]
        primes_list.append(five_prime)
    
        three_prime['New_Start'] = np.where(three_prime[6] == "+", three_prime[2]-1, three_prime[1])
        three_prime['New_End'] = np.where(three_prime[6] == "+", three_prime[2], three_prime[1]+1)
        three_prime = three_prime[[0,'New_Start', 'New_End', 3,4,5,6]]
        primes_list.append(three_prime)
    
    for num, label in enumerate(names):
        primes_list[num].to_csv(str(names[num]) + ".bed", sep="\t", index=False, header=False)

if __name__ == '__main__':
    main(sys.argv[1:])
