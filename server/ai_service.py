"""AI service module."""
from typing import List

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from pydantic import BaseModel


class PatientModel(BaseModel):
    """
    A Pydantic model representing patient data for a medical study.

    Attributes:
        age (int): Age of the patient in years.
        sex (int): Sex of the patient (e.g., 0 for female, 1 for male).
        cp (int): Chest pain type (value 1-4, where 1 is typical angina and 4 is asymptomatic).
        trestbps (int): Resting blood pressure (in mm Hg on admission to the hospital).
        chol (int): Serum cholesterol in mg/dl.
        fbs (int): Fasting blood sugar > 120 mg/dl (1 = true; 0 = false).
        restecg (int): Resting electrocardiographic results (values 0,1,2).
        thalach (int): Maximum heart rate achieved.
        exang (int): Exercise-induced angina (1 = yes; 0 = no).
        oldpeak (float): ST depression induced by exercise relative to rest.
        slope (int): The slope of the peak exercise ST segment.
        ca (int): Number of major vessels (0-4) colored by fluoroscopy.
        thal (int): Thalassemia (3 = normal; 6 = fixed defect; 7 = reversible defect).

    Each attribute is a required field and should be provided when creating an
    instance of the model.
    """

    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

    def to_list(self) -> List:
        """Returns a list of the patient's attributes."""
        return [
            self.age,
            self.sex,
            self.cp,
            self.trestbps,
            self.chol,
            self.fbs,
            self.restecg,
            self.thalach,
            self.exang,
            self.oldpeak,
            self.slope,
            self.ca,
            self.thal,
        ]


class AIService:
    """Hosts a sklearn model and provides a predict method."""

    _model: RandomForestClassifier

    def __init__(self) -> None:
        self._model = joblib.load(
            "./model/heart_disease_random_forest_classifier.joblib"
        )

    def predict(self, patient: PatientModel):
        """Test method for now"""
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

        return {
            "prediction": prediction_value,
            "predict_proba": predict_proba_dict,
        }
