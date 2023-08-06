import lightgbm as lgb

import numpy as np

from scipy.stats import uniform, randint

from sklearn.datasets import load_breast_cancer, load_diabetes, load_wine
from sklearn.metrics import auc, accuracy_score, confusion_matrix, mean_squared_error
from sklearn.model_selection import cross_val_score, GridSearchCV, KFold, RandomizedSearchCV, train_test_split
from sklearn.linear_model import Lasso
import xgboost as xgb
from sklearn import datasets, linear_model

def report_best_scores(results, n_top=3):
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                  results['mean_test_score'][candidate],
                  results['std_test_score'][candidate]))
            print("Parameters: {0}".format(results['params'][candidate]))
            print("")

class ForecasterWrapper:
    """ Base object to roll a neural network model.
    Rolling over a time axis with a train period from `t - n` to `t` and a
    testing period from `t` to `t + s`.
    Parameters
    ----------
    X, y : array_like
        Respectively input and output data.
    f : callable, optional
        Function to transform target, e.g. ``torch.sign`` function.
    index : array_like, optional
        Time index of data.
    Methods
    -------
    __call__
    Attributes
    ----------
    n, s, r : int
        Respectively size of training, testing and rolling period.
    b, e, T : int
        Respectively batch size, number of repass_steps and size of entire dataset.
    t : int
        The current time period.
    y_eval, y_test : np.ndarray[ndim=1 or 2, dtype=np.float64]
        Respectively evaluating (or training) and testing predictions.
    """
    def __init__(self, method = 'standard'):
        """ Initialize shape of target. """
        if method == 'standard':
            self.model =  linear_model.LinearRegression()
        if method == 'lasso':
            alpha = 0.1
            self.model = Lasso(alpha=alpha, fit_intercept=False, max_iter=5000)
        if method == 'lgbm':
            self.model = lgb.LGBMRegressor()
        if method == 'xgb':
            self.model = xgb.XGBRegressor()

    def calibrate(self, X, y, method = 'standard'):
        if method == 'standard':
            #nothing to calibrate here
            self.model = linear_model.LinearRegression()
        if method == 'lasso':
            param_grid = {
                'alpha': [0.01, 0.1,0.5,1],
            }
            gbm_grid = GridSearchCV(self.model, param_grid, cv=2)
            gbm_grid.fit(X, y)
            print('Best parameters found by grid search are:', gbm_grid.best_params_)
            best_params = gbm_grid.best_params_
            self.model = Lasso(alpha=best_params['alpha'], fit_intercept=False, max_iter=5000)
        if method == 'lgbm':
            param_grid = {
                'boosting_type': ['gbdt'],
                'num_leaves': [int(x) for x in np.linspace(start=10, stop=30, num=10)],
                'max_depth': [int(x) for x in np.linspace(start=-1, stop=7, num=3)],
                'learning_rate': [0.001,0.01,0.2],
                'n_estimators': [int(x) for x in np.linspace(start=40, stop=120, num=40)]
            }
            gbm_grid = GridSearchCV(self.model, param_grid, cv=2)
            gbm_grid.fit(X, y)
            print('Best parameters found by grid search are:', gbm_grid.best_params_)
            best_params = gbm_grid.best_params_
            self.model.set_params(**best_params)
            return best_params
        if method == 'xgb':
            params = {
                "colsample_bytree": uniform(0.7, 0.3),
                "gamma": uniform(0, 0.5),
                "learning_rate": uniform(0.03, 0.3),  # default 0.1
                "max_depth": randint(2, 6),  # default 3
                "n_estimators": randint(100, 150),  # default 100
                "subsample": uniform(0.6, 0.4)
            }
            cv = 2
            n_iter = 50
            # cv=3
            # n_iter = 200
            search = RandomizedSearchCV(self.model, param_distributions=params, random_state=42, n_iter=n_iter, cv=cv,
                                        verbose=1, n_jobs=1, return_train_score=True)
            search.fit(X, y)
            print('reporting best scores')
            report_best_scores(search.cv_results_, 1)

    def fit(self, X_train, y_train, X_val, y_val, method = 'standard'):
        if method == 'standard':
            self.model.fit(X_train, y_train)
        if method == 'lasso':
            self.model.fit(X_train, y_train)
        if method == 'lgbm':
            self.model.fit(X_train, y_train,eval_set=[(X_val, y_val)],eval_metric= ['l1','l2'],early_stopping_rounds=5,verbose= 0)
        if method == 'xgb':
            self.model.fit(X_train, y_train, eval_set=[(X_val, y_val)], eval_metric=['rmse', 'logloss'],
                           early_stopping_rounds=5, verbose=0)

    def predict(self, X_test, method = 'standard'):
        y_pred = self.model.predict(X_test)
        return y_pred

    def get_features_importance(self, features_names, method = 'standard'):
        run_importances = {}
        if method == 'lgbm':
            for (name, imp) in zip(features_names, self.model.feature_importances_):
                run_importances[name] = imp
        if method == 'standard':
            for (name, imp) in zip(features_names, self.model.coef_):
                run_importances[name] = imp
        return run_importances
