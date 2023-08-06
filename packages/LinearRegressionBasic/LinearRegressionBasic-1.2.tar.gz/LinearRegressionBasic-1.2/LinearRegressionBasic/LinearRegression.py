import pandas as pd

class LinearRegression:

    def __init__(self,a=1,b=1,X1=[]):
        
       """
       Generic Linear Regression class is used to define a simple LinearRegression
       model

       Attributes:
       -- X1(a list of float) is the explanatory variable 
       -- b(float) is the slop of the line
       -- a(float) is the intercept (the value of y when x = 0)
          """ 
    
       self.a = a
       self.b = b
       self.X1 = X1
        

    def import_X_data(self,file_name):
        
       """
       Function to read in data from a csv file. The csv file should have the 
       first column for X1 values
       which has one number (float) per line. 
       
       There should be no header in the csv file 
                
       Args:
            file_name (string): name of a file to read from
        
       Returns:
          the list of values      
          """       
       data= pd.read_csv(file_name,header=None)
        
       values = data.iloc[:,0].tolist()
    
       self.X1 = values
        
       return self.X1 

