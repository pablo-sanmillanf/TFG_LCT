# Import libraries using import keyword
import numpy as np
from scipy.interpolate import interp1d
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


# Custom Axis to don't allow Y movement
class My_Axes(matplotlib.axes.Axes):
    name = "My_Axes"
    def drag_pan(self, button, key, x, y):
        matplotlib.axes.Axes.drag_pan(self, button, 'x', x, y) # pretend key=='x'

matplotlib.projections.register_projection(My_Axes)

matplotlib.rcParams['toolbar'] = 'None'



class graph:
    def __init__(self, allow_float=False):
        self.allow_float = allow_float
    
        # Setting Plot and Axis variables as subplots()
        # function returns tuple(fig, ax)
        self.fig, self.axis = plt.subplots(subplot_kw={"projection" : "My_Axes"}, figsize=(9, 6))
        
        #Set Y values
        plt.yticks(np.arange(1, 5))
        
        # Adjust the bottom and left size according to the
        # requirement of the user
        plt.subplots_adjust(bottom=0.25)
        plt.subplots_adjust(left=0.15)
        
        plt.grid()
        
        # Max default graph length to adjust the slider movement to the function 
        self.max_graph_len = 100
        
        # Choose the Slider color
        slider_color = 'White'
        
        # Set the axis and slider position in the plot
        axis_position = plt.axes([0.2, 0.1, 0.65, 0.03],
                                facecolor = slider_color)
        self.slider = Slider(axis_position,
                                'Pos', 0, 100.0, valinit=0)
        self.slider.valtext.set_visible(False)
        
        # update graph position 
        self.slider.on_changed(self.update)
        self.update(0)
        
        self.no_graphs_added = True
        
        
        
    # update() function to change the graph when the
    # slider is in use
    def update(self, val):
        # Adjust the slider value to the graphs length
        adjusted_val = val * (self.max_graph_len - 10) / 100
        self.axis.axis([adjusted_val, adjusted_val+10, 0.75, 4.25])
        self.fig.canvas.draw_idle()


    def add_graph(self, x, y, labels):
        if len(labels) != 4:
            raise Exception("Length labels must be 4")
        
        if self.allow_float == False:
            if issubclass(x.dtype.type, np.integer) == False:
                raise Exception("X values must be integers")
            
            if issubclass(y.dtype.type, np.integer) == False:
                raise Exception("Y values must be integers")
    
        # plot the x and y using scatter function
        data = self.axis.scatter(x, y, marker="o")
        
        # Resize slider movement to adjust to graph length
        if len(x) > self.max_graph_len:
            self.max_graph_len = len(x)
        
        # Create smooth union points line
        cubic_interpolation_model = interp1d(x, y, kind = "cubic")
        X_=np.linspace(x.min(), x.max(), len(x)*10)
        Y_=cubic_interpolation_model(X_)
        smooth_line = self.axis.plot(X_, Y_)
        
        line_color = smooth_line[0].get_color()
        
        if self.no_graphs_added == True:
            self.no_graphs_added = False
            
            #Add custom Y-labels
            self.axis.set_yticklabels(labels)
            
            # Setting up Y-axis tick color
            self.axis.spines['left'].set_color(line_color)
            
            # Setting up X-axis tick color
            self.axis.tick_params(axis='y', colors=line_color)    
        else:
            self.no_graphs_added = True
            
            sec_axis = self.axis.secondary_yaxis(-0.1, functions=(lambda x: x, lambda x: x))
            
            #Set Y values
            sec_axis.set_yticks(np.arange(1, 5))
            
            #Add custom Y-labels
            sec_axis.set_yticklabels(labels)
            
            # setting up Y-axis tick color
            sec_axis.spines['left'].set_color(line_color)
            
            #setting up X-axis tick color
            sec_axis.tick_params(axis='y', colors=line_color)    
        
    
    def print_figure(self):
        # Display the plot
        plt.show()
