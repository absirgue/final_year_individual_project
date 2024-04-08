import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from scipy import stats
class GraphingHelper:
    """
    Concerns with all related to generating viusal representations of data through any sort of graph.
    """
    
    """
    Creates a scatter plot and a trendline for the points it presents.
    Params
        - data - the 2d data to be plotted
        - title - the graph's title
        - x_axis - the label of the graph's x axis
        - y_axis - the label of the graph's y axis.
        - folder_name - (if defined) the name of the folder to save the generated graph in
    """
    def scatter_with_trendline(self,data, title, x_axis, y_axis, folder_name=None):
        x = np.array(self.extract_x_values(data))
        y = np.array(self.extract_y_values(data))
        plt.scatter(x, y, label='Data')
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title(title)
        plt.legend()
        file_path = title+'.png'
        if folder_name:
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            file_path = os.path.join(folder_name, file_path)
        plt.savefig(file_path)
        plt.close()

    """
    Creates a graph representing a surface of 3d points.
    Params
        - d3_arr - the 3d data to be plotted, taking the form of a 2d array where internal 
        arrays each have 3 elements.
        - title - the graph's title
        - x_axis - the label of the graph's x axis
        - y_axis - the label of the graph's y axis.
        - z_label - the label of the graph's z axis.
        - folder_name - (if defined) the name of the folder to save the generated graph in
    """
    def plot_3d_array_of_points(self, d3_arr, x_label, y_label, z_label, title,folder_name=None):
        try:
            cleaned_d3_arr = self.remove_elements_with_None_values(d3_arr)
            x_values = self.extract_x_values(cleaned_d3_arr)
            y_values = self.extract_y_values(cleaned_d3_arr)
            z_values = self.extract_z_values(cleaned_d3_arr)
            fig = plt.figure()
            ax = plt.figure().add_subplot(projection='3d')
            ax.plot_trisurf(x_values, y_values, z_values, linewidth=0.2, antialiased=True)
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.set_zlabel(z_label)
            ax.view_init(elev=20, azim=15)
            ax.set_title(title)
            file_path = title+'.png'
            if folder_name:
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                file_path = os.path.join(folder_name, file_path)
            plt.savefig(file_path)
            plt.close()
        except Exception as e:
            print(e)
    
    # Returns the array cleaned of all None elements.
    def remove_elements_with_None_values(self, arr):
        cleaned = []
        for element in arr:
            if element[0] != None and element[1] != None and element[2]!= None :
                cleaned.append(element)
        return cleaned

    """
    Creates a line graph for an array of points
    Params
        - d3_arr - the 2d data to be plotted
        - title - the graph's title
        - x_axis - the label of the graph's x axis
        - y_axis - the label of the graph's y axis.
        - folder_name - (if defined) the name of the folder to save the generated graph in
    """
    def plot_2d_array_of_points(self,d2_arr,x_label,y_label,title,folder_name=None):
        x_values = self.extract_x_values(d2_arr)
        y_values = self.extract_y_values(d2_arr)
        plt.figure()
        plt.grid()
        plt.plot(x_values, y_values)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        file_path = title+'.png'
        if folder_name:
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            file_path = os.path.join(folder_name, file_path)

        plt.savefig(file_path)
        plt.close()

    """
    Creates a bar chart from a dictionary associating a category name with a value for 
    this category.
    Params
        - data - the dictionary
        - title - the graph's title
        - x_axis - the label of the graph's x axis
        - y_axis - the label of the graph's y axis.
        - folder_name - (if defined) the name of the folder to save the generated graph in
    """
    def create_bar_chart_from_dictionary(self,data,x_label, y_label,title, folder_name=None):
        plt.figure()
        plt.bar(data.keys(), data.values())
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        file_path = title+'.png'
        if folder_name:
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            file_path = os.path.join(folder_name, file_path)

        plt.savefig(file_path)
        plt.close()
    
    """
    Creates a box plot for a dictionary of different set names and their associated list of values.
    The box plot is color-coded to indicate the number of elements in each set.

    Params
        - data - the dictionary
        - title - the graph's title
        - x_axis - the label of the graph's x axis
        - y_axis - the label of the graph's y axis.
        - folder_name - (if defined) the name of the folder to save the generated graph in
    """
    def create_box_plot(self,x_label,y_label, title,data,folder_name=None):
        counts = {key: len(value) for key, value in data.items()}
        norm = Normalize(vmin=min(counts.values()), vmax=max(counts.values()))
        colors = [plt.cm.viridis(norm(count)) for count in counts.values()]
        sm = ScalarMappable(cmap=plt.cm.viridis, norm=norm)
        sm.set_array([])
        plt.figure(figsize=(13, 9))
        plt.grid()
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.title(title)
        plt.xticks(rotation=45)
        bplot = plt.boxplot(data.values(), labels=data.keys(), patch_artist=True)
        for box, color in zip(bplot['boxes'], colors):
            box.set_facecolor(color)
        plt.colorbar(sm, label='Number of Elements')
        
        file_path = title+'.png'
        if folder_name:
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            file_path = os.path.join(folder_name, file_path)
        plt.savefig(file_path)
        plt.close()
    
    # Returns the x value of all points in a list of points.
    def extract_x_values(self, array):
        x_vals = []
        for point in array:
            x_vals.append(point[0])
        return x_vals
    
    # Returns the y value of all points in a list of points.
    def extract_y_values(self, array):
        y_vals = []
        for point in array:
            y_vals.append(point[1])
        return y_vals

    # Returns the z value (if any) of all points in a list of points.
    def extract_z_values(self, array):
        z_vals = []
        for point in array:
            if len(point) >= 3:
                z_vals.append(point[2])
        return z_vals