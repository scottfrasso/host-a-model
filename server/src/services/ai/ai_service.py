"""AI service module."""
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from schemas import PatientModel, HeartDiseasResult


class AIService:
    """Hosts a sklearn model and provides a predict method."""

    _model: RandomForestClassifier

    def __init__(self, model_location) -> None:
        self._model = joblib.load(model_location)

    def predict(self, patient: PatientModel) -> HeartDiseasResult:
        """
        Predicts the probability of a patient having heart disease.
        """
        test_data_df = pd.DataFrame([patient.model_dump()])
        prediction = self._model.predict(test_data_df)
        prediction_value = int(prediction[0])

        predict_proba = self._model.predict_proba(test_data_df)
        predict_proba_values = predict_proba[0].tolist()
        class_labels = self._model.classes_

        predict_proba_dict = {}
        class_probabilities = dict(zip(class_labels, predict_proba_values))
        for label, probability in class_probabilities.items():
            predict_proba_dict[str(label)] = probability

        return HeartDiseasResult(
            prediction=prediction_value, predict_proba=predict_proba_dict
        )
