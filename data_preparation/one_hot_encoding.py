import pandas as pd
from data_preparation.cell_cleaning import CleanCellOfParenthesis


class CountryRiskScoreOneHotEncoding:
    def __init__(self,data):
        self.data = data
        self.COUNTRY_RISK_SCORE_COL_NAME = "PD Fundamental  Country/Region Risk Score [Latest Quarter] (Model Version 1.0)"
    
    def encode(self):
        self.clean_scores_of_parenthesis()
        self.data = OneHotEncoding().one_hot_encode_list_items(self.data,self.COUNTRY_RISK_SCORE_COL_NAME)
        return self.data
    
    def clean_scores_of_parenthesis(self):
        for index, row in self.data.iterrows():
            cell_content = str(row[self.COUNTRY_RISK_SCORE_COL_NAME])
            without_parenthesis = CleanCellOfParenthesis().clean(cell_content)
            if not (without_parenthesis.strip() in ["a","a+","aa","aa+","aaa","b","b+","bb","bb+","bbb","bbb+","ccc or worse","ccc+"]):
                without_parenthesis = 'No Country Risk Score Known'
            self.data.loc[index, self.COUNTRY_RISK_SCORE_COL_NAME] = without_parenthesis


class OneHotEncoding:
    def one_hot_encode_list_items(self,data_frame,column_name):
        one_hot_encoded = pd.get_dummies(data_frame[column_name].explode())
        data_frame = pd.concat([data_frame, one_hot_encoded.groupby(one_hot_encoded.index).sum()], axis=1)
        data_frame = data_frame.drop(column_name, axis=1)
        return data_frame