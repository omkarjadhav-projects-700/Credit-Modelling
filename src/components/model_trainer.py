import os
import sys
from src.exception import CustomException
from src.components.model_trainer import ModelTrainerConfig, ModelTrainer

from dataclasses import dataclass

from catboost import CatBoostRegressor

from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor



from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor


from src.exception import CustomException
from src.logger import logging

from src.utils import save_object


def evaluate_model(X_train, X_test, y_train, y_test, models):
    report = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score = r2_score(y_test, y_pred)
        report[name] = score
    return report


@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    
    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and testing data.")
            X_train, y_train, X_test, y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:, :-1],
                test_array[:,-1]
            )

            models={
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Nearest Neighbores": KNeighborsRegressor(),
                "CatBoost Regressor": CatBoostRegressor(),
                "Adaboost Regressor": AdaBoostRegressor()
            }
            

            model_report:dict=evaluate_model(X_train=X_train, X_test=X_test, 
                                             y_train=y_train, y_test=y_test,models=models)
            

            ### To get the best model names fro  dict:
            best_model_score = max(model_report.values())
            best_model_name= list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("No best model found.", sys)
            logging.info(f"Best found model on both training and testing dataset.")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )


            predicted=best_model.predict(X_test)

            r_squared=r2_score(y_test, predicted)

            return r2_score

        except Exception as e:
            raise CustomException(e, sys)
        




