class NumberFromStringExtractor:

    def extract_share_value(self,string):
        share = 0
        if (len(string.split(":"))>1) and (len(string.split(":")[1].split(" "))>2):
            share = string.split(":")[1].split(" ")[2][1:-2]
            try:
                return float(share)
            except ValueError:
                return 0
        return 0
    
    def extract_country_name(self, string):
        return string.split(":")[0].strip()