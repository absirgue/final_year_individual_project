import numpy as np
import pandas as pd
from data_preparation.number_from_string_extractor import NumberFromStringExtractor
class EntropyCalculator:
    def encode(self,cell_content):
        total_share = 0
        shares = []
        for element in cell_content.split(";"):
            share = NumberFromStringExtractor().extract_share_value(element)
            total_share+=share
            if share:
                shares.append(share)
        if total_share:
            # Normalize the split
            for raw_share_idx in range(len(shares)):
                shares[raw_share_idx] = shares[raw_share_idx]/total_share
            entropy_score = self.entropy(shares)
            if pd.notna(entropy_score):
                return entropy_score
            else:
                return None
        else:
            return None

    def entropy(self,probabilities):
        return -np.sum(probabilities * np.log2(probabilities))

class SegmentsCount:
    def encode(self,cell_content):
        return cell_content