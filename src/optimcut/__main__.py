import os
import sys

import numpy as np

import tkinter as tk
from tkinter import filedialog




dpath = os.path.dirname( os.path.abspath(__file__) )
print(dpath)
sys.path.append(dpath)


"""
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
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class FileDialogDemo(QWidget):
   def __init__(self, parent = None):
      super(FileDialogDemo, self).__init__(parent)
		
      layout = QVBoxLayout()
      self.btn = QPushButton("QFileDialog static method demo")
      self.btn.clicked.connect(self.getfile)
		
      layout.addWidget(self.btn)
      self.le = QLabel("Hello")
		
      layout.addWidget(self.le)
      self.btn1 = QPushButton("QFileDialog object")
      self.btn1.clicked.connect(self.getfiles)
      layout.addWidget(self.btn1)
		
      self.contents = QTextEdit()
      layout.addWidget(self.contents)
      self.setLayout(layout)
      self.setWindowTitle("File Dialog demo")
		
   def getfile(self):
      fname = QFileDialog.getOpenFileName(self, 'Open file', 
         'c:\\',"Image files (*.jpg *.gif)")
      self.le.setPixmap(QPixmap(fname))
		
   def getfiles(self):
      dlg = QFileDialog()
      dlg.setFileMode(QFileDialog.AnyFile)
      dlg.setFilter("Text files (*.txt)")
      filenames = QStringList()
		
      if dlg.exec_():
         filenames = dlg.selectedFiles()
         f = open(filenames[0], 'r')
			
         with f:
            data = f.read()
            self.contents.setText(data)
				
def main():
   app = QApplication(sys.argv)
   ex = FileDialogDemo()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()
