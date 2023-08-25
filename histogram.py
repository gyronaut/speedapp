import numpy as np
#import matplotlib.pyplot as plt

class Histogram:

    def __init__(self, low, high, numbins, x_label = "x", y_label = "counts"):
        if(high<=low or type(numbins)!= int or numbins<=0):
            raise Exception("Error in initialization. Check histogram parameters.")
        self.x_label = x_label
        self.y_label = y_label
        self.low = low
        self.high = high
        self.numbins = numbins
        self.data = [0]*numbins
        self.bincenters = []
        self.binwidth = (high-low)/numbins
        for ibin in range(0, numbins):
            self.bincenters.append((ibin+0.5)*self.binwidth)

    def fill(self, value, weight=1):
        if(value > self.high or value < self.low):
            return 1
        bin = int(np.floor((value-self.low)/(self.binwidth)))
        self.data[bin] += weight
        return 0
    
#    def plot(self):
#        plt.bar(self.bincenters, self.data, width=self.binwidth, align='center')
#        plt.ylabel(self.y_label)
#        plt.xlabel(self.x_label)
#        plt.show()
    
    def rebin(self, factor):
        if(type(factor)!=int or factor <= 0):
            raise Exception("Invalid rebin factor {}. Must be Positive integer".format(factor))
        if(self.numbins%factor !=0):
            raise Exception("Histogram's number of bins {} is not divisible by {}".format(self.numbins, factor))
        rebinned_hist = Histogram(self.low, self.high, int(self.numbins/factor), self.x_label, self.y_label)
        for bin_center, bin_value in zip(self.bincenters, self.data):
            rebinned_hist.fill(bin_center, bin_value)
        return rebinned_hist

    def add(self, hist2):
        if(self.low != hist2.low or self.high != hist2.high or self.numbins != hist2.numbins):
            raise Exception("Histograms must have matching limits and numbins to add together")
        for ibin in range(0, self.numbins):
            self.data[ibin] += hist2.data[ibin]

    def scale(self, scale_factor):
        self.data = [bin*scale_factor for bin in self.data]
        