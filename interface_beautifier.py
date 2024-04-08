class InterfaceBeautifier:
    """
    Enables communications with the user through the command line, enbaling constant styling
    of messages.
    """
    
    def print_percentage_progress(self, name_of_task,percent_progress):
        pertwenty_progress = percent_progress//5
        statement = name_of_task+": "
        for i in range(int(pertwenty_progress)):
            statement+="#"
        for i in range(int(20-pertwenty_progress)):
            statement+="_"
        print(statement+"("+str(round(percent_progress,2))+"%)\n")
        
    def print_information_statement(self, text):
        print("\nInformation:",text)
    
    def print_major_annoucement(self, text):
        print("\n            ************            ")
        print("ANNOUNCEMENT:",text.upper())
        print("            ************            \n")