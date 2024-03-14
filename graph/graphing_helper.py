import matplotlib.pyplot as plt
import os
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
class GraphingHelper:

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
    
    def remove_elements_with_None_values(self, arr):
        cleaned = []
        for element in arr:
            if element[0] != None and element[1] != None and element[2]!= None :
                cleaned.append(element)
        return cleaned

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
    
    def extract_x_values(self, array):
        x_vals = []
        for point in array:
            x_vals.append(point[0])
        return x_vals
    
    def extract_y_values(self, array):
        y_vals = []
        for point in array:
            y_vals.append(point[1])
        return y_vals

    def extract_z_values(self, array):
        z_vals = []
        for point in array:
            z_vals.append(point[2])
        return z_vals