import numpy as np
import xgboost as xgb
from sklearn.base import BaseEstimator, TransformerMixin


class ModelWrapper(BaseEstimator, TransformerMixin):
    """
    Универсальная обертка для стандартизации API вызова модели.
    Используется для возможности исполнения пайплайна с
    вызовом любого типа используемых моделей.
    Поддерживаемые модели: DS-Template, xgboost, catboost,
    lightgbm, sklearn.
    Parameters
    ----------
    estimator: estimator object implementing 'fit'
        Экземпляр модели для применения к набору данных.
    fill_value: int/float, optional, default = None
        Значене для заполнения пропусков в данных.
        Опциональный параметр, по умолчанию, не используется.
    log_scale: bool, optional, default = False
        Флаг, означающий, что прогнозы модели представлены в
        логарифмированной-шкале. После применения модели
        требуется преобразование прогнозов в исходную
        шкалу. Опциональный параметр, по умолчанию,
        не используется. Используется для задачи
        регрессии.
    log_bias: int/float, optional, default = 0
        Смещение, используемое в аргументе логарифма.
        Пример: если целевая переменная при обучении
        преобразовывалась с помощь np.log(target + 1),
        то log_bias = 1. Опциональный параметр, по умолчанию,
        равен 0. Используется для задачи регрессии.
    min_target: int/float, optional, default = 0
        Минимальное значение целевой переменной в
        обучающей выборке. Опциональный параметр, по
        умолчанию, равен 0. Используется для задачи регрессии.

    """
    def __init__(self,
                 estimator,
                 fill_value=None,
                 log_scale=False,
                 log_bias=0,
                 min_target=0) -> None:

        self.estimator = estimator
        self.fill_value = fill_value
        self.log_scale = log_scale
        self.log_bias = log_bias
        self.min_target = min_target

    def transform(self, X, y=None) -> np.array:
        """
        Применение модели к новому набору данных.
        Parameters
        ----------
        X: pandas.DataFrame, shape = [n_samples, n_features]
            Матрица признаков для применения модели.
        Returns
        -------
        y_pred: numpy.array
            Вектор прогнозов.

        """
        method = self._choose_predict_method()
        if self.fill_value:
            X = X.fillna(self.fill_value)

        y_pred = method(X)
        return self.postprocessing(y_pred)

    def _choose_predict_method(self) -> callable:
        """
        Выбор метода для прогнозирования.
        """
        module = self.estimator.__module__
        predict_proba_flg = hasattr(self.estimator, "predict_proba")

        if "dspl.models" in module:
            return self.estimator.transform
        elif "xgboost.core" in module:
            return self.xgb_booster_predict
        elif predict_proba_flg:
            return self.estimator.predict_proba
        else:
            return self.estimator.predict

    def postprocessing(self, y_pred: np.array) -> np.array:
        """
        Постпроцессинг полученных прогнозов.
        Если модель возвращает матрицу прогнозов с двумя
        столбцами - то возвращается вероятность принадлежности
        объекта в целевому классу (второй столбец).
        Если при обучении модели осуществлялось логарифмирование
        таргета - то возвращается прогноз в исходном диапазоне
        целевой переменной.
        Parameters
        ----------
        y_pred: np.array, shape = [n_samples, ]
            Вектор прогнозов.
        Returns
        -------
        y_pred_transformed: np.array, shape = [n_samples, ]
            Преобразованный вектор прогнозов.

        """
        shape = np.ndim(y_pred)

        if shape == 2:
            return y_pred[:, 1]
        if self.log_scale:
            return np.exp(y_pred) - self.log_bias + self.min_target

        return y_pred

    def xgb_booster_predict(self, X) -> np.array:
        """
        Применение нативной модели xgboost к новому
        набору данных X. Для применения нативной версии
        xgboost требуется преобразования набора данных в
        xgboost.DMatrix.
        Parameters
        ----------
        X: pandas.DataFrame, shape = [n_samples, n_features]
            Матрица признаков для применения модели.
        Returns
        -------
        y_pred: numpy.array
            Вектор прогнозов.

        """
        X = xgb.DMatrix(X)
        return self.estimator.predict(X)
