from analysis.conclusion_3.rating_changes_identifier import RatingChangesIdentifier

class PredictivePowerAnalyser:
    """
    Gives access to metrics related to the predictive power of our algorithms.
    """

    def __init__(self,data_source,entity_ids):
        self.data_source = data_source
        self.entity_ids = entity_ids
        self.correctly_predicted_vals = []
        self.incorrectly_predicted_vals = []
    
    # Perform global analysis of the predictive power of a given clustering result.
    def analyse(self, credit_rating_clusters):
        observed_changes = RatingChangesIdentifier(self.data_source).identify_changes()
        predicted_changes = self.extract_predicted_changes_from_clusters(credit_rating_clusters)
        observed_switch_to_or_from_below_b_minus = self.extract_jumps_to_or_from_below_b_minus(predicted_changes)
        analysis = {}
        global_analysis = self.get_analysis_obj_for_observations_and_predictions(observed_changes,predicted_changes)
        analysis["Global"] = global_analysis
        to_or_from_b_minus_analysis = self.get_analysis_obj_for_observations_and_predictions(observed_switch_to_or_from_below_b_minus,predicted_changes)
        analysis["Restricted to jumps to or from below B-"] = to_or_from_b_minus_analysis
        return analysis

    """
    Returns a dictionary with the complete analysis of predictive power base on a set of observed
    changes and a set of predictions.
    """
    def get_analysis_obj_for_observations_and_predictions(self, observations, predictions):
        confusion_matrix = self.get_confusion_matrix_for_direction_prediction(observations,predictions)
        analysis = {}
        analysis["Metrics"] = self.calculate_prediction_quality_metrics_for_confusion_matrix(confusion_matrix)
        analysis["Confusion Matrix"] = confusion_matrix
        return analysis

    def extract_jumps_to_or_from_below_b_minus(self, changes):
        switches_to_or_from_below_b_minus = []
        for change in changes:
            if "Number of jumps from or to D" in change and change["Number of jumps from or to D"]:
                switches_to_or_from_below_b_minus.append(change)
        return switches_to_or_from_below_b_minus
    
    """
    Returns metrics of prediction quality for both rating upgrades and rating downgrades 
    from a confusion matrix. 
    """
    def calculate_prediction_quality_metrics_for_confusion_matrix(self, confusion_matrix):
        metrics_for_downgrades_without_no_change = self.calculate_prediction_quality_metrics(true_positive = confusion_matrix["predicted_down_AND_was_down"], false_positive = confusion_matrix["predicted_down_BUT_was_up"], false_negative = confusion_matrix["predicted_up_BUT_was_down"], true_negative = confusion_matrix["predicted_up_AND_was_up"])
        metrics_for_upgrades_without_no_change = self.calculate_prediction_quality_metrics(true_negative = confusion_matrix["predicted_down_AND_was_down"], false_negative = confusion_matrix["predicted_down_BUT_was_up"], false_positive = confusion_matrix["predicted_up_BUT_was_down"], true_positive = confusion_matrix["predicted_up_AND_was_up"])
        return {"Class: Upgrade":metrics_for_upgrades_without_no_change,"Class: Downgrade":metrics_for_downgrades_without_no_change}

    # Returns metrics of prediction quality based on values in a confusion matrix.
    def calculate_prediction_quality_metrics(self, true_positive, false_positive, true_negative, false_negative):
        if true_positive <1 and false_positive <1:
            return "No element of this class"
        elif true_positive <1:
            return f"No correct predictions for this class {false_positive} false positives and {false_negative} false negatives."
        accuracy = true_positive/(true_positive+false_positive)
        precision = (true_positive+true_negative)/(true_positive+false_positive+true_negative+false_negative)
        recall = true_positive/(true_positive+false_negative)
        f1_score = 2*((precision*recall)/(precision+recall))
        return {"Accuracy":accuracy,"Precision":precision,"Recall":recall,"F1-Score":f1_score}

    # Returns an ordered list of predictions made by a given clustering result.
    def extract_predicted_changes_from_clusters(self, credit_rating_clusters):
        changes = []
        for cluster in credit_rating_clusters:
            row_specified_changes = cluster.get_rows_difference_with_mean_rating()
            changes = changes + self.convert_row_specified_changes_to_entity_id_specified_changes(row_specified_changes)
        return changes
        
    """
    Convert the predictions made in terms of row id to predictions in terms of each company's 
    S&P Entity ID.
    """
    def convert_row_specified_changes_to_entity_id_specified_changes(self, changes):
        entity_id_specified_changes = []
        for change in changes:
            row_idx = list(change.keys())[0]
            diff = list(change.values())[0]
            entity_id_specified_changes.append({self.entity_ids[row_idx]:diff})
        return entity_id_specified_changes

    """
    Returns a confusion matrix for our models' ability to predict the direction of 
    credit rating upgrades or downgrades between our two snaphsots of each company's credit rating.
    We used the oldest one to train our model and compare its prediction with the values observed 
    in the most recent one.
    """
    def get_confusion_matrix_for_direction_prediction(self, expected, predicted):
        confusion_matrix = {
            "predicted_down_AND_was_down":0,
            "predicted_up_AND_was_up":0,
            "predicted_no_change_AND_was_no_change":0,
            "predicted_down_BUT_was_up":0,
            "predicted_down_BUT_was_no_change":0,
            "predicted_no_change_BUT_was_up":0,
            "predicted_no_change_BUT_was_down":0,
            "predicted_up_BUT_was_down":0,
            "predicted_up_BUT_was_no_change":0,
        }
        for row_prediction in predicted:
            entity_id = list(row_prediction.keys())[0]
            direction_prediction = self.get_direction_prediction_from_row_prediction(row_prediction)
            direction_expectation = self.get_value_for_entity_id(entity_id,expected)
            confusion_matrix = self.update_confusion_matrix(direction_prediction,direction_expectation,confusion_matrix)
        return confusion_matrix

    """
    Updates a given confusion matrix based on the value of a prediction anf the value we
    expected it to take.
    Note: implementing a separate class for the confusion matrix could improve our code quality. 
    """
    def update_confusion_matrix(self, prediction, expectation,confusion_matrix):
        if expectation != None:
            if expectation > 0:
                if prediction == 0:
                    confusion_matrix["predicted_no_change_BUT_was_up"] = confusion_matrix["predicted_no_change_BUT_was_up"] +1 
                elif prediction < 0:
                    confusion_matrix["predicted_down_BUT_was_up"] = confusion_matrix["predicted_down_BUT_was_up"] +1 
                else:
                    confusion_matrix["predicted_up_AND_was_up"] = confusion_matrix["predicted_up_AND_was_up"] +1 
            elif expectation < 0:
                if prediction == 0:
                    confusion_matrix["predicted_no_change_BUT_was_down"] = confusion_matrix["predicted_no_change_BUT_was_down"] +1 
                elif prediction < 0:
                    confusion_matrix["predicted_down_AND_was_down"] = confusion_matrix["predicted_down_AND_was_down"] +1 
                else:
                    confusion_matrix["predicted_up_BUT_was_down"] = confusion_matrix["predicted_up_BUT_was_down"] +1 
        elif prediction==0:
            confusion_matrix["predicted_no_change_AND_was_no_change"] = confusion_matrix["predicted_no_change_AND_was_no_change"] +1
        elif prediction > 0:
            confusion_matrix["predicted_up_BUT_was_no_change"] = confusion_matrix["predicted_up_BUT_was_no_change"] +1
        else:
            confusion_matrix["predicted_down_BUT_was_no_change"] = confusion_matrix["predicted_down_BUT_was_no_change"] +1
        return confusion_matrix

    def get_value_for_entity_id(self, entity_id, entity_id_changes):
        for change in entity_id_changes:
            if entity_id in change.keys():
                change_charasteristics = change[entity_id]
                return self.get_direction_prediction_for_numeric_pred(change_charasteristics["difference"])
        return None
    
    def get_direction_prediction_from_row_prediction(self,row_prediction):
        pred_diff = list(row_prediction.values())[0]
        return self.get_direction_prediction_for_numeric_pred(pred_diff)
    
    def get_direction_prediction_for_numeric_pred(self,numeric_pred):
        if numeric_pred ==0:
            return 0
        # inversed because a rating of 1 is the best rating, so a negative difference indicates a rating uprgade
        elif numeric_pred < 0:
            return 1
        else:
            return -1