import pandas
import numpy as np
import os
import csv
import numpy.random as nr
import IPython.display
import hashlib
from math import *

def generator( nonce ):
    """Generate a random number generator which may be used for the given student"""
    projectId = os.environ['COCALC_PROJECT_ID']
    assert projectId, 'No cocalc project id'
    s = projectId + nonce
    h = int(hashlib.sha1(s.encode('utf-8')).hexdigest(), 16)
    if h<0:
        h = -h
    rs = nr.RandomState(nr.MT19937(nr.SeedSequence(h)))
    return rs

class Question:
    
    def __init__(self):
        self.write_data_file()
        g = generator('hfjdi')
        self.underlyings = [0,0,1,1]
        n_options = len( self.underlyings )
        self.quantities = g.randint(low=2,high=10, size=n_options)
        self.puts = [False]*n_options
        self.puts[g.randint(low=1,high=3)]=True
        p1 = self.final_prices[0]
        p2 = self.final_prices[1]
        self.strikes = [0]*n_options
        for i in range(1,n_options):
            p = self.final_prices[self.underlyings[i]]
            if i % 2==0:
                self.strikes[i] = g.randint(low=floor(0.9*p), high=floor(0.99*p))
            else:
                self.strikes[i] = g.randint(low=floor(1.01*p), high=floor(1.1*p))                
        self.r = g.randint(low=1,high=9)/100
        
    def describe_portfolio(self):
        s = "";
        for i in range(0,len(self.quantities)):
            s = s+"* "+self.describe_derivative(i)+".\n";
        s+=("\n\nThe continuously compounded interest rate is r={:.2f}.").format(self.r)
        
        IPython.display.display(IPython.display.Markdown(s))
   
    def describe_derivative(self, i):
        if (not self.puts[i]) and self.strikes[i]==0:
            return "{} units of stock {}".format(self.quantities[i], self.underlyings[i]+1);
        option_type = "call"
        if (self.puts[i]):
            option_type = "put"
        return "{} European {} options on stock {} with strike {} and maturity 52 weeks".format(
                           self.quantities[i],
                           option_type,
                           self.underlyings[i]+1,
                           self.strikes[i]);
        

    def write_data_file( self, filename = 'stock-data.csv'):
        """Generate a data file for each student and returns the final prices"""
        excel_data = pandas.read_excel('ukx.xlsx', header=None)
        num_rows = excel_data.shape[0]
        num_cols = excel_data.shape[1]
        num_stocks = ceil(num_cols/3) #Round up to the nearest integer
        num_weeks = num_rows-2

        g = generator('1fjdh')
        c1 = g.randint(low=0,high=num_stocks-1)
        c2 = c1
        while c2==c1:
            c2 = g.randint(low=0,high=num_stocks-1)

        with open(filename, 'w', newline='') as csvfile:
            w = csv.writer(csvfile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
            w.writerow(['Date','ACME Price','BigBank Price'])
            for i in range(0,num_weeks):
                row = 2+i
                date = excel_data[0][row]
                p1 = excel_data[c1*3+1][row]
                p2 = excel_data[c2*3+1][row]
                w.writerow([date,p1,p2])

        self.final_prices = np.array([p1,p2])

question = Question()