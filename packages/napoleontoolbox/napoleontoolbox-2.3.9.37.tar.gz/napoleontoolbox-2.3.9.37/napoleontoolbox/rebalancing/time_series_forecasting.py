from napoleontoolbox.rebalancing import rolling

from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

from napoleontoolbox.signal import signal_utility


import pandas as pd
import numpy as np


from napoleontoolbox.utility import metrics
from scipy.optimize import Bounds, minimize



def discretize(y_pred, upper_quantile_threshold=0.8, lower_quantile_threshold = 0.2):
    y_pred_discrete = np.zeros(y_pred.shape)
    upper_threshold = np.quantile(y_pred, upper_quantile_threshold)
    lower_threshold = np.quantile(y_pred, lower_quantile_threshold)
    y_pred_discrete[y_pred > upper_threshold] = 1.
    y_pred_discrete[y_pred < lower_threshold] = -1.
    return y_pred_discrete


def find_best_discretization(y_pred, y, seed = 42):
    N_ = 2
    w0 = np.array([0.3,0.7])
    # Set constraints
    #const_sum = LinearConstraint(np.ones([1, N_]), [1], [1])
    up_bound_ = 1.
    low_bound_ = 0.
    const_ind = Bounds(low_bound_ * np.ones([N_]), up_bound_ * np.ones([N_]))

    def f_to_optimize(w):
        lower_quantile_threshold = w[0]
        upper_quantile_threshold = w[1]

        y_pred_discrete = discretize(y_pred, upper_quantile_threshold=upper_quantile_threshold, lower_quantile_threshold=lower_quantile_threshold)
        perf_df = signal_utility.reconstitute_prediction_perf(y_pred=y_pred_discrete, y_true=y,
                                                              transaction_cost=False,
                                                              print_turnover=False)
        sharpe_strat = metrics.sharpe(perf_df['perf_return'].dropna(), period=252, from_ret=True)
        return sharpe_strat

    np.random.seed(seed)
    # Optimize f
    w__ = minimize(
        f_to_optimize,
        w0,
        method='SLSQP',
        #constraints=[const_sum],
        bounds=const_ind
    ).x

    lower_quantile_threshold = w__[0]
    upper_quantile_threshold = w__[1]
    y_pred_discrete = discretize(y_pred, upper_quantile_threshold=upper_quantile_threshold,
                                 lower_quantile_threshold=lower_quantile_threshold)
    perf_df = signal_utility.reconstitute_prediction_perf(y_pred=y_pred_discrete, y_true=y,
                                                          transaction_cost=False,
                                                          print_turnover=False)
    sharpe_strat = metrics.sharpe(perf_df['perf_return'].dropna(), period=252, from_ret=True)
    sharpe_under = metrics.sharpe(perf_df['close_return'].dropna(), period=252, from_ret=True)
    return lower_quantile_threshold, upper_quantile_threshold, sharpe_strat, sharpe_under

def rolling_forecasting(forecasting_model, X, y, n=252, s=63,  s_eval= None, calibration_step=None, optimize_threshold=True, method = 'standard', display = False, **kwargs):
    assert X.shape[0] == y.shape[0]
    idx = X.index
    forecasting_series = pd.Series(index=idx, name='prediction')

    if n is None and s_eval is None:
        roll = rolling._ExpandingRollingMechanism(idx, s=s)
    if n is None and s_eval is not None:
        roll = rolling._ExpandingEvalRollingMechanism(idx, s=s, s_eval = s_eval)
    if n is not None and s_eval is None :
        roll = rolling._RollingMechanism(idx, n=n, s=s)
    if n is not None and s_eval is not None:
        roll = rolling._EvalRollingMechanism(idx, n=n, s=s, s_eval = s_eval)
    features_names = list(X.columns)
    features_importances = []
    iteration_counter = 0
    for slice_n, slice_s, slice_s_eval in roll():
        # Select X
        X_train = X.loc[slice_n].copy()
        y_train = y.loc[slice_n].copy()

        X_test = X.loc[slice_s].copy()
        y_test = y.loc[slice_s].copy()
        if calibration_step >0:
            if iteration_counter%calibration_step == 0:
                # print('launching calibration '+str(iteration_counter))
                forecasting_model.calibrate(X_train, y_train, method)
                # print('endiing calibration ' + str(iteration_counter))

        if slice_s_eval is not None:
            X_eval = X.loc[slice_s_eval].copy()
            y_eval = y.loc[slice_s_eval].copy()
            forecasting_model.fit(X_train, y_train, X_eval, y_eval, method)
        else :
            forecasting_model.fit(X_train, y_train, X_train, y_train, method)

        y_pred = forecasting_model.predict(X_test, method)

        if optimize_threshold:
            y_train_pred = forecasting_model.predict(X_train, method)
            lower_quantile_threshold, upper_quantile_threshold, sharpe_strat, sharpe_under =find_best_discretization(y_train, y_train_pred)
            # print('best sharpe training period '+str(sharpe_strat))
            # print('lower quantile '+str(lower_quantile_threshold))
            # print('upper quantile '+str(upper_quantile_threshold))
            y_pred_discrete = discretize(y_pred, upper_quantile_threshold,lower_quantile_threshold)
            y_test_discrete = discretize(y_test, upper_quantile_threshold,lower_quantile_threshold)
        else:
            y_pred_discrete =  y_pred > 0
            y_test_discrete = y_test > 0


        run_importances=forecasting_model.get_features_importance(features_names,method = method)
        features_importances.append(run_importances)


        forecasting_series.loc[slice_s] = y_pred.ravel()
        matrix = confusion_matrix(y_test_discrete, y_pred_discrete)
        rmse = mean_squared_error(y_test, y_pred)
        accuracy = accuracy_score(y_test_discrete, y_pred_discrete)

        if display:
            print('training slice ' + str(slice_n))
            print('testing slice ' + str(slice_s))
            print('rmse for slice : '+str(rmse))
            print('accuracy')
            print(accuracy)
            print('confusion matrix')
            print(matrix)
        iteration_counter = iteration_counter+1

    features_importances = pd.DataFrame(features_importances)
    return forecasting_series, features_importances

