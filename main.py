import os
import sys

import numpy as np

import tkinter as tk
from tkinter import filedialog


sys.path.append('/home/konrad/Pulpit/Codes/pyinstaller_test')
#import _test



dpath = os.path.dirname( os.path.abspath(__file__) )
print(dpath)
sys.path.append(dpath)



if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    
    # get file path
    file_path = filedialog.askopenfilename()
    
    # open file (only csv)
    print('Opening file', file_path)
    arr = np.loadtxt(file_path, delimiter=",")
    arr = np.ascontiguousarray(arr, dtype=np.float64)
    
    print(arr)
    #_test.print_array(arr)
