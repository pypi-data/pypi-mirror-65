
from .LinearRegression import LinearRegression

class SVLinearRegression(LinearRegression):
    
    def __init__(self,a=1,b=1,X1=[]):
        """
        Define a Single explanatory Variable Linear Regression class Y = aX1 + b

        Attributes:
        -- X1(a list of float) is the explanatory variable 
        -- b(float) is the slop of the line
        -- a (float) is the intercept (the value of y when x = 0)
        -- Y (a list of float) is the dependent variable 
          """

        LinearRegression.__init__(self,a,b,X1)
        self.Y = self.calculate_Y()
       
        pass
       
    def calculate_Y(self):
        """
        Function to calculate the Y values from the a,b,X1 values given 
        The outcome values (Y) are stored in a list.
                
        Args:
            None
        
        Returns:
            a list of values for Y
        
          """ 
        Y=[self.a*i+self.b for i in self.X1] #Start with an empty list
        
        self.Y = Y
        
        return self.Y
       
        pass
    
    def import_data_from_csv(self,file_name):
        """
        Function to update the X1 values from the csv file imported, 
        and then update the respective Y values
       
        The outcome values (Y) are stored in a list.
                
        Args:
            file_name: CSV file anme
        
        Returns:
            list of X1 and Y Values
        
           """           
        self.X1=LinearRegression.import_X_data(self,file_name) # import X values and updating self.X1 to the values
       
        self.calculate_Y() # update Y values
      
        return print('X1 is {} and Y is {}'.format(self.X1,self.Y))
        
        
      
    
        
