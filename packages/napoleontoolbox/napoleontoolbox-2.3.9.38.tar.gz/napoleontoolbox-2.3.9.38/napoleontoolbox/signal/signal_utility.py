#!/usr/bin/env python
# coding: utf-8

from numpy.lib.stride_tricks import as_strided as stride
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, minimize
from napoleontoolbox.utility import metrics
import numpy as np
from napoleontoolbox.signal import signal_utility


def convert_to_sql_column_format(run):
    run = run.replace('[', 'ccg')
    run = run.replace(']', 'ccd')
    run = run.replace(',', 'comma')
    run = run.replace(' ', 'space')
    run = run.replace('.', 'dot')
    run = run.replace('-', 'minus')
    run = run.replace('"', 'dqq')
    run = run.replace("'", 'sqq')
    run = run.replace('{', 'aag')
    run = run.replace('}', 'aad')
    run = run.replace(':', 'dodo')
    return run

def recover_to_sql_column_format(run):
    run = run.replace('ccg','[')
    run = run.replace('ccd',']')
    run = run.replace('comma',',')
    run = run.replace('space',' ')
    run = run.replace('dot','.')
    run = run.replace('minus','-')
    run = run.replace('dqq','"')
    run = run.replace('sqq',"'")
    run = run.replace('aag','{')
    run = run.replace('aad','}')
    run = run.replace('dodo',':')
    return run

def roll_wrapper(rolled_df, lookback_window, skipping_size, function_to_apply, trigger):
    signal_df = roll(rolled_df, lookback_window).apply(function_to_apply)
    signal_df = signal_df.to_frame()
    signal_df.columns = ['signal_gen']
    signal_df['signal'] = signal_df['signal_gen'].shift()
    if trigger:
        signal_df['signal'] =  signal_df['signal'].fillna(method='ffill')

    signal_df = signal_df.fillna(0.)
    rolled_df = pd.merge(rolled_df, signal_df, how='left', left_index=True, right_index= True)
    rolled_df = rolled_df.iloc[skipping_size:]
    return rolled_df

def roll(df, w):
    v = df.values
    d0, d1 = v.shape
    s0, s1 = v.strides
    restricted_length = d0 - (w - 1)
    a = stride(v, (restricted_length, w, d1), (s0, s0, s1))
    rolled_df = pd.concat({
        row: pd.DataFrame(values, columns=df.columns)
        for row, values in zip(df.index[-restricted_length:], a)
    })
    return rolled_df.groupby(level=0)

def f_sharpe_signals_mix(data, w, display_threshold = 0.99):
    all_signals = [col for col in data.columns if 'signal' in col]
    N_ = len(all_signals)
    w = w.reshape([1,N_])
    temp_df = data[['close']].copy()
    #temp_df = temp_df.rename(columns={"signal0": "signal"}, errors="raise")
    tt = pd.DataFrame(data[all_signals].values * w, columns=all_signals, index=data.index)
    temp_df['signal'] = tt.sum(axis=1)
    hourly_df = reconstitute_signal_perf(data=temp_df, transaction_cost=True, print_turnover=False)
    sharpe_strat = metrics.sharpe(hourly_df['perf_return'].dropna(), period=252 * 24, from_ret=True)
    if np.random.rand()>display_threshold:
        print(w)
        print('signals mix sharpe')
        print(sharpe_strat)
    return -sharpe_strat

def expanding_zscore(signal_np_array=None, skipping_point = 5, signal_continuum_threshold = 10):
    u = np.unique(signal_np_array)
    nb_distinct_signals = len(u)
    if nb_distinct_signals >= signal_continuum_threshold:
        me_zscore_expanding_array = np.zeros(signal_np_array.shape)
        for i in range(len(signal_np_array)):
            if i <= skipping_point:
                me_zscore_expanding_array[i] = signal_np_array[i]
            else :
                std_dev = max(signal_np_array[:i].std(), 1e-6)
                me_zscore_expanding_array[i] = (signal_np_array[i] - signal_np_array[:i].mean())/std_dev
        return me_zscore_expanding_array
    else:
        raise Exception('zscoring a non continuous signal '+str(nb_distinct_signals))

def reconstitute_signal_perf(data=None, initial_price = 1. , average_execution_cost = 7.5e-4 , transaction_cost = True, print_turnover = False, normalization = False):
    if normalization:
        #data.signal = (data.signal - data.signal.mean())/data.signal.std(ddof=0)
        data.signal = expanding_zscore(signal_np_array=data.signal.values)
    data['turn_over'] = abs(data['signal'] - data['signal'].shift(-1).fillna(0.))
    if print_turnover:
        print('average hourly turn over')
        print(data['turn_over'].sum() / len(data))

    data['close_return'] = data['close'].pct_change()
    data['reconstituted_close'] = metrics.from_ret_to_price(data['close_return'],initial_price=initial_price)
    data['non_adjusted_perf_return'] = data['close_return'] * data['signal']
    if transaction_cost :
        data['perf_return'] = data['non_adjusted_perf_return']- data['turn_over']*average_execution_cost
    else :
        data['perf_return'] = data['non_adjusted_perf_return']
    data['reconstituted_perf'] = metrics.from_ret_to_price(data['perf_return'],initial_price=initial_price)
    return data

def reconstitute_prediction_perf(y_pred=None, y_true=None, initial_price = 1. , average_execution_cost = 7.5e-4 , transaction_cost = True, print_turnover = False):
    if not isinstance(y_pred, pd.DataFrame):
        y_pred=pd.DataFrame(y_pred)
    data = y_pred
    data.columns = ['signal']
    if not isinstance(y_true, np.ndarray):
        y_true = y_true.values

    data['close_return']=y_true
    data['turn_over'] = abs(data['signal'] - data['signal'].shift(-1).fillna(0.))
    if print_turnover:
        print('average hourly turn over')
        print(data['turn_over'].sum() / len(data))
    data['reconstituted_close'] = metrics.from_ret_to_price(data['close_return'],initial_price=initial_price)
    data['non_adjusted_perf_return'] = data['close_return'] * data['signal']
    if transaction_cost :
        data['perf_return'] = data['non_adjusted_perf_return']- data['turn_over']*average_execution_cost
    else :
        data['perf_return'] = data['non_adjusted_perf_return']
    data['reconstituted_perf'] = metrics.from_ret_to_price(data['perf_return'],initial_price=initial_price)
    return data

def compute_turn_over(data=None):
    return abs((data.signal - data.signal.shift(-1).fillna(0.))).mean()


def optimize_weights(data = None, starting_date = None, ending_date = None):
    #T = data.index.size
    print(max(data.index))
    print(min(data.index))
    data = data[data.index >= starting_date]
    data = data[data.index <= ending_date]
    print(max(data.index))
    print(min(data.index))
    all_sigs = [col for col in data.columns if 'signal' in col]
    N_ = len(all_sigs)
    w0 = np.ones([N_]) / N_

    const_sum = LinearConstraint(np.ones([1, N_]), [1], [1])
    up_bound = 1.
    low_bound = 0.
    up_bound_ = max(up_bound, 1 / N_)
    low_bound_ = min(low_bound, 1 / N_)
    const_ind = Bounds(low_bound_ * np.ones([N_]), up_bound_ * np.ones([N_]))
    to_optimize = lambda x : signal_utility.f_sharpe_signals_mix(data, x)
    w__ = minimize(
        to_optimize,
        w0,
        method='SLSQP',
        constraints=[const_sum],
        bounds=const_ind
    ).x
    print('optimal weights')
    print(w__)
    return w__

def compute_signals_weights_perf(data = None, optimal_weights = None, starting_date = None, ending_date = None, normalization = False, n_items_per_year = 252):
    print(max(data.index))
    print(min(data.index))
    data = data[data.index >= starting_date]
    data = data[data.index <= ending_date]
    print(max(data.index))
    print(min(data.index))
    all_sigs = [col for col in data.columns if 'signal' in col]
    temp_df = data[['close']].copy()
    #temp_df = temp_df.rename(columns={"signal0": "signal"}, errors="raise")
    optimal_signal = pd.DataFrame(data[all_sigs].values * optimal_weights, columns=all_sigs, index=data.index)
    temp_df['signal'] = optimal_signal.sum(axis=1)
    hourly_df = reconstitute_signal_perf(data=temp_df, transaction_cost=False, normalization=normalization)
    sharpe_strat_without = metrics.sharpe(hourly_df['perf_return'].dropna(), period=n_items_per_year, from_ret=True)
    sharpe_under = metrics.sharpe(hourly_df['close_return'].dropna(), period=n_items_per_year, from_ret=True)

    hourly_df = reconstitute_signal_perf(data=temp_df, transaction_cost=True, normalization=normalization)
    sharpe_strat = metrics.sharpe(hourly_df['perf_return'].dropna(), period=n_items_per_year, from_ret=True)
    return hourly_df, sharpe_strat, sharpe_strat_without, sharpe_under

