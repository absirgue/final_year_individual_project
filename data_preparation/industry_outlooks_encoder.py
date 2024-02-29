import pandas as pd

class IndustryOutlookEncode:
    def __init__(self,data):
        self.data = data

    def encode(self,weight_distribution):
        if len(weight_distribution) != 7:
            return self.data
        industry_outlooks_col_names = ['# of Analyst Buy (1) Industry Recommendations  Capital IQ [Latest]','# of Analyst High (2) Industry Recommendations  Capital IQ [Latest]','# of Analyst Highest (1) Industry Recommendations  Capital IQ [Latest]','# of Analyst Hold (3) Industry Recommendations  Capital IQ [Latest]','# of Analyst Low (4) Industry Recommendations  Capital IQ [Latest]','# of Analyst Lowest (5) Industry Recommendations  Capital IQ [Latest]','# of Analyst Neutral (3) Industry Recommendations  Capital IQ [Latest]']
        ordered_weights = []
        for col_name in industry_outlooks_col_names:
            for industry_outlook_type in weight_distribution:
                if industry_outlook_type in col_name.lower().split(" "):
                    ordered_weights.append(weight_distribution[industry_outlook_type])
        try:
            self.data['CUSTOM Industry Outlook Weighted Average'] = (self.data[industry_outlooks_col_names].mul(ordered_weights)).sum(axis=1)
            self.data.drop(industry_outlooks_col_names, axis=1,inplace=True)
        except:
            pass
        return self.data


