class NumberFromStringExtractor:

    # Returns the numerical value (if any) in a string containing this value and its title.
    def extract_share_value(self,string):
        share = 0
        if (len(string.split(":"))>1) and (len(string.split(":")[1].split(" "))>2):
            share = string.split(":")[1].split(" ")[2][1:-2]
            try:
                return float(share)
            except ValueError:
                return 0
        return 0
    
    # Returns the the title associateed with a value in a string containing this value and its title.
    def extract_value_name(self, string):
        return string.split(":")[0].strip()