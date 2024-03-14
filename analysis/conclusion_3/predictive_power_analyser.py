from analysis.conclusion_3.rating_changes_identifier import RatingChangesIdentifier

class PredictivePowerAnalyser:

    def __init__(self,data_source,entity_ids):
        self.data_source = data_source
        self.entity_ids = entity_ids
        self.correctly_predicted_vals = []
        self.incorrectly_predicted_vals = []
    
    def analyse(self, credit_rating_clusters):
        observed_changes = RatingChangesIdentifier(self.data_source).identify_changes()
        predicted_changes = self.extract_predicted_changes_from_clusters(credit_rating_clusters)
        direction_prediction_confusion_matrix = self.get_confusion_matrix_for_direction_prediction(observed_changes,predicted_changes)
        analysis = {}
        analysis["Metrics"] = self.calculate_prediction_quality_metrics_for_confusion_matrix(direction_prediction_confusion_matrix)
        analysis["Confusion Matrix"] = direction_prediction_confusion_matrix
        return analysis
    
    def calculate_prediction_quality_metrics_for_confusion_matrix(self, confusion_matrix):
        metrics_for_downgrades_without_no_change = self.calculate_prediction_quality_metrics(true_positive = confusion_matrix["predicted_down_AND_was_down"], false_positive = confusion_matrix["predicted_down_BUT_was_up"], false_negative = confusion_matrix["predicted_up_BUT_was_down"], true_negative = confusion_matrix["predicted_up_AND_was_up"])
        metrics_for_upgrades_without_no_change = self.calculate_prediction_quality_metrics(true_negative = confusion_matrix["predicted_down_AND_was_down"], false_negative = confusion_matrix["predicted_down_BUT_was_up"], false_positive = confusion_matrix["predicted_up_BUT_was_down"], true_positive = confusion_matrix["predicted_up_AND_was_up"])
        return {"Class: Upgrade":metrics_for_upgrades_without_no_change,"Class: Downgrade":metrics_for_downgrades_without_no_change}

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

    def extract_predicted_changes_from_clusters(self, credit_rating_clusters):
        changes = []
        for cluster in credit_rating_clusters:
            row_specified_changes = cluster.get_rows_difference_with_mean_rating()
            changes = changes + self.convert_row_specified_changes_to_entity_id_specified_changes(row_specified_changes)
        print("ANDND EF")
        print(len(changes))
        return changes
        
    def convert_row_specified_changes_to_entity_id_specified_changes(self, changes):
        entity_id_specified_changes = []
        for change in changes:
            row_idx = list(change.keys())[0]
            diff = list(change.values())[0]
            entity_id_specified_changes.append({self.entity_ids[row_idx]:diff})
        return entity_id_specified_changes

    # def get_confusion_matrix_for_direction_prediction_for_changes_in_classes(self, expected, predicted):
    #     confusion_matrix = {
    #         "predicted_down_AND_was_down":0,
    #         "predicted_up_AND_was_up":0,
    #         "predicted_no_change_AND_was_no_change":0,
    #         "predicted_down_BUT_was_up":0,
    #         "predicted_down_BUT_was_no_change":0,
    #         "predicted_no_change_BUT_was_up":0,
    #         "predicted_no_change_BUT_was_down":0,
    #         "predicted_up_BUT_was_down":0,
    #         "predicted_up_BUT_was_no_change":0,
    #     }
    #     for row_prediction in predicted:
    #         entity_id = list(row_prediction.keys())[0]
    #         direction_prediction = self.get_direction_prediction_from_row_prediction(row_prediction)
    #         direction_expectation = self.get_value_for_entity_id(entity_id,expected)


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
    # def get_rating_classes_diffenrence(self, rating_before, rating_now)


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
    
    def get_direction_prediction_for_numeric_pred_with_tolerance(self,numeric_pred,tolerance):
        if numeric_pred <=tolerance and numeric_pred >=-tolerance:
            return 0
        # inversed because a rating of 1 is the best rating, so a negative difference indicates a rating uprgade
        elif numeric_pred < tolerance:
            return 1
        else:
            return -1