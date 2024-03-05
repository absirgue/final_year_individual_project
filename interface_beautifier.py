class InterfaceBeautifier:

    def print_percentage_progress(self, name_of_task,percent_progress):
        pertwenty_progress = percent_progress//5
        statement = "Progress on Hyperparameter Optimization: "
        for i in range(pertwenty_progress):
            statement+="#"
        for i in range(20-pertwenty_progress):
            statement+="_"
        print(statement+"("+str(percent_progress)+"%)\n")
        
    def print_information_statement(self, text):
        print("\nInformation:",text)
    
    def print_major_annoucement(self, text):
        print("\n            ************            ")
        print("ANNOUNCEMENT:",text.upper())
        print("            ************            \n")