#!/usr/bin/env python
# coding: utf-8

import numpy as np
import numpy.ma as ma
from napoleontoolbox.tools.analyze_tools import roll_corr

continuum_signals = ['alpha_2', 'alpha_3', 'alpha5',  'alpha_6', 'alpha_6_rank', 'alpha_8', 'alpha_12', 'alpha_13', 'alpha_14',  'alpha_15',  'alpha_16', 'slope_induced' ]

def compute_correlation(col_one, col_two):
    a = ma.masked_invalid(col_one)
    b = ma.masked_invalid(col_two)
    msk = (~a.mask & ~b.mask)
    correlation_matrix = ma.corrcoef(col_one[msk], col_two[msk])
    correlation_coefficient = correlation_matrix[0][1]
    return correlation_coefficient

def is_signal_continuum(signal_type):
    if signal_type in continuum_signals:
        return True
    else:
        return False

def alpha_2(data = None,  contravariant = -1., **kwargs):
    data['log_vol'] = np.log(data['volumefrom'])
    correlation_coefficient = compute_correlation(data.log_vol.diff(2).rank(pct=True), (data.close - data.open)/data.open)
    return contravariant*correlation_coefficient

def alpha_3(data = None, contravariant = -1., **kwargs):
    correlation_coefficient = compute_correlation(data.open.rank(pct = True), data.volumefrom.rank(pct = True))
    return contravariant*correlation_coefficient

def alpha_5(data = None, contravariant = -1., **kwargs):
    data['volu_close'] = data['volumefrom']*data['close']
    vwap = data['volu_close'].sum() / data['volumefrom'].sum()
    data['open_minus_vwap'] = data.open - vwap
    data['close_minus_vwap'] = data.close - vwap
    correlation_coefficient = compute_correlation(data['open_minus_vwap'].rank(pct = True), data['close_minus_vwap'].rank(pct = True))
    return contravariant*correlation_coefficient

def alpha_6(data = None, contravariant = -1., **kwargs):
    correlation_coefficient = compute_correlation(data['open'], data['volumefrom'])
    return contravariant*correlation_coefficient

def alpha_6_rank(data = None, contravariant = -1., **kwargs):
    correlation_coefficient = compute_correlation(data['open'].rank(pct = True), data['volumefrom'].rank(pct = True))
    return contravariant*correlation_coefficient

def alpha_8(data = None, contravariant = -1 , lag=5, **kwargs):
    data['close_return']=data['close'].pct_change()
    col1 = (data['open']*data['close_return'])
    col2 = (data['open']*data['close_return']).shift(lag)
    correlation_coefficient = compute_correlation(col1, col2)
    return contravariant*correlation_coefficient

# Alpha  # 12: (sign(delta(volume, 1)) * (-1 * delta(close, 1)))
def alpha_12(data = None, contravariant = -1., **kwargs):
    signals = np.sign(data['volumefrom'].diff() * data['close'].diff())
    return signals[-1]*contravariant

def alpha_13(data = None, contravariant = -1., lag = 5,  **kwargs):
    to_roll =  data[['close','volumefrom']]
    to_roll = to_roll.reset_index(drop = True)
    result_df = roll_corr(to_roll, window=lag)
    result_df = result_df.dropna()
    result_df = result_df.rank(pct = True)
    return contravariant*result_df.iloc[-1,0]

#Alpha#14: ((-1 * rank(delta(returns, 3))) * correlation(open, volume, 10))
def alpha_14(data = None, contravariant = -1., lag = 3, **kwargs):
    correlation_coefficient = compute_correlation(data['open'],data['volumefrom'])
    returns = data['close'].pct_change().diff(lag)
    returns=returns.to_frame()
    return returns.iloc[-1,0]*correlation_coefficient*contravariant

# Alpha#15: (-1 * sum(rank(correlation(rank(high), rank(volume), 3)), 3))
def alpha_15(data = None, contravariant = -1., lag = 3, **kwargs):
    data['high_rank'] = data['high'].rank(pct=True)
    data['volume_rank'] = data['volumefrom'].rank(pct=True)
    to_roll =  data[['high_rank','volume_rank']]
    to_roll = to_roll.reset_index(drop = True)
    result_df = roll_corr(to_roll, window=lag)
    result_df = result_df.dropna()
    result_df = result_df.rank(pct = True)
    return contravariant*result_df[-lag:].mean().iloc[0]

# #Alpha#16: (-1 * rank(covariance(rank(high), rank(volume), 5)))
def alpha_16(data = None, contravariant = -1., lag = 5, **kwargs):
    data['high_rank'] = data['high'].rank(pct=True)
    data['volume_rank'] = data['volumefrom'].rank(pct=True)
    to_roll =  data[['high_rank','volume_rank']]
    to_roll = to_roll.reset_index(drop = True)
    result_df = roll_corr(to_roll, window=lag)
    result_df = result_df.rank(pct = True)
    return result_df.iloc[-1,0]



def lead_lag_indicator(data = None, lead=3, lag=5, contravariant = -1., **kwargs):
    output_sma_lead = data.close[-lead:].mean()
    output_sma_lag = data.close[-lag:].mean()
    if output_sma_lead > output_sma_lag:
        return -contravariant
    else :
        return contravariant

def volume_weighted_high_low_vol(data = None, vol_threshold = 0.8, up_trend_threshold=0.8, low_trend_threshold=0.2, contravariant = -1., lag = 2, **kwargs):
    ## aggregating the volumes by lag
    data.index = range(0,len(data))
    all_indices = list(reversed(range(len(data) - 1, 0, -lag)))
    data['aggregated_indice'] = np.nan
    data['aggregated_indice'].loc[all_indices] = all_indices
    data['aggregated_indice']= data['aggregated_indice'].fillna(method='bfill')
    data['aggregated_indice'] = data['aggregated_indice'].astype(int)
    volumefrom = data.groupby(['aggregated_indice'])['volumefrom'].agg('sum')
    high = data.groupby(['aggregated_indice'])['high'].agg('max')
    low = data.groupby(['aggregated_indice'])['low'].agg('min')

    data['aggregated_volume'] =  data['aggregated_indice'].map(volumefrom)
    data['aggregated_high'] =  data['aggregated_indice'].map(high)
    data['aggregated_low'] =  data['aggregated_indice'].map(low)

    data = data[::-lag]
    data = data.iloc[::-1]

    data['hl'] = (data['aggregated_high'] - data['aggregated_low'])/data['aggregated_low']
    data['volu_hi_low'] = data['aggregated_volume']*data['hl']

    data['close_ret']=data['close'].pct_change()

    data['volu_hi_low_pct_rank'] = data['volu_hi_low'].rank(pct=True)
    data['close_ret_pct_rank'] = data['close_ret'].rank(pct=True)

    trend_rank = data['close_ret_pct_rank'].iloc[-1]
    vol_rank = data['volu_hi_low_pct_rank'].iloc[-1]

    # #trend over the all lookback period
    # trend = ((data['close'][-1]-data['close'][0])/data['close'][0])
    # # vol over the all lookback_period
    # weighted_volu_hi_low = data['volu_hi_low'].sum() / data['volumefrom'].sum()
    #
    #
    # #trend over the lagging period
    # trend_lag = ((data['close'][-1]-data['close'][-1])/data['close'][-1])
    # weighted_volu_hi_low_lag = data['volu_hi_low'][-1]/ data['volumefrom'][-1]
    #
    if vol_rank > vol_threshold:
        if trend_rank > up_trend_threshold:
            return contravariant
        elif trend_rank < low_trend_threshold:
            return -contravariant
        else:
            return np.nan
    else :
        return np.nan


def volume_weighted_high_low_vol_cont(data = None,  contravariant = -1., lag = 2, **kwargs):
    ## aggregating the volumes by lag
    data.index = range(0,len(data))
    all_indices = list(reversed(range(len(data) - 1, 0, -lag)))
    data['aggregated_indice'] = np.nan
    data['aggregated_indice'].loc[all_indices] = all_indices
    data['aggregated_indice']= data['aggregated_indice'].fillna(method='bfill')
    data['aggregated_indice'] = data['aggregated_indice'].astype(int)
    volumefrom = data.groupby(['aggregated_indice'])['volumefrom'].agg('sum')
    high = data.groupby(['aggregated_indice'])['high'].agg('max')
    low = data.groupby(['aggregated_indice'])['low'].agg('min')

    data['aggregated_volume'] =  data['aggregated_indice'].map(volumefrom)
    data['aggregated_high'] =  data['aggregated_indice'].map(high)
    data['aggregated_low'] =  data['aggregated_indice'].map(low)

    data = data[::-lag]
    data = data.iloc[::-1]

    data['hl'] = (data['aggregated_high'] - data['aggregated_low'])/data['aggregated_low']
    data['volu_hi_low'] = data['aggregated_volume']*data['hl']

    data['close_ret']=data['close'].pct_change()

    data['volu_hi_low_pct_rank'] = data['volu_hi_low'].rank(pct=True)
    data['close_ret_pct_rank'] = data['close_ret'].rank(pct=True)

    #trend_rank = data['close_ret_pct_rank'].iloc[-1]
    #vol_rank = data['volu_hi_low_pct_rank'].iloc[-1]

    ##  common stuff with the discrete version above

    #trend over the all lookback period
    trend = ((data['close'].iloc[-1]-data['close'].iloc[0])/data['close'].iloc[0])
    # vol over the all lookback_period
    weighted_volu_hi_low = data['volu_hi_low'].sum() / data['volumefrom'].sum()


    #trend over the lagging period
    trend_lag = ((data['close'].iloc[-1]-data['close'].iloc[-2])/data['close'].iloc[-2])
    weighted_volu_hi_low_lag = data['volu_hi_low'].iloc[-1]/ data['volumefrom'].iloc[-1]


    signal = np.nan
    try:
        trend_ratio = trend_lag/trend
        vol_ratio = weighted_volu_hi_low_lag / weighted_volu_hi_low
        signal = contravariant * vol_ratio * trend_ratio
    except Exception as e:
        print(e)
    return signal

    #@todo : devise a continuous signal
    # if vol_rank > vol_threshold:
    #     if trend_rank > up_trend_threshold:
    #         return signal
    #     elif trend_rank < low_trend_threshold:
    #         return signal
    #     else:
    #         return np.nan
    # else :
    #     return np.nan
#


def slope_induced(data = None, contravariant = -1., up_trend_threshold=0.8, low_trend_threshold=0.2, lag = 2, slope_column = 'high',**kwargs):
    ## aggregating the volumes by lag
    data.index = range(0,len(data))
    all_indices = list(reversed(range(len(data) - 1, 0, -lag)))
    data['aggregated_indice'] = np.nan
    data['aggregated_indice'].loc[all_indices] = all_indices
    data['aggregated_indice']= data['aggregated_indice'].fillna(method='bfill')
    data['aggregated_indice'] = data['aggregated_indice'].astype(int)
    volumefrom = data.groupby(['aggregated_indice'])['volumefrom'].agg('sum')
    high = data.groupby(['aggregated_indice'])['high'].agg('max')
    low = data.groupby(['aggregated_indice'])['low'].agg('min')

    data['aggregated_volume'] =  data['aggregated_indice'].map(volumefrom)
    data['aggregated_high'] =  data['aggregated_indice'].map(high)
    data['aggregated_low'] =  data['aggregated_indice'].map(low)

    data = data[::-lag]
    data = data.iloc[::-1]

    data['hl'] = (data['aggregated_high'] - data['aggregated_low'])/data['aggregated_low']
    data['volu_hi_low'] = data['aggregated_volume']*data['hl']

    data['close_ret']=data['close'].pct_change()
    data['high_ret']=data['aggregated_high'].pct_change()

    data['volu_hi_low_pct_rank'] = data['volu_hi_low'].rank(pct=True)
    data['close_ret_pct_rank'] = data['close_ret'].rank(pct=True)
    data['high_ret_pct_rank'] = data['high_ret'].rank(pct=True)

    trend_rank = np.nan
    if slope_column == 'close':
        trend_rank = data['close_ret_pct_rank'].iloc[-1]
    elif slope_column == 'high':
        trend_rank = data['high_ret_pct_rank'].iloc[-1]

    if trend_rank > up_trend_threshold:
        return contravariant
    elif trend_rank < low_trend_threshold:
        return -contravariant
    else:
        return np.nan

def slope_induced_cont(data = None, contravariant = -1., lag = 2, slope_column = 'high',**kwargs):
    ## aggregating the volumes by lag
    data.index = range(0,len(data))
    all_indices = list(reversed(range(len(data) - 1, 0, -lag)))
    data['aggregated_indice'] = np.nan
    data['aggregated_indice'].loc[all_indices] = all_indices
    data['aggregated_indice']= data['aggregated_indice'].fillna(method='bfill')
    data['aggregated_indice'] = data['aggregated_indice'].astype(int)
    volumefrom = data.groupby(['aggregated_indice'])['volumefrom'].agg('sum')
    high = data.groupby(['aggregated_indice'])['high'].agg('max')
    low = data.groupby(['aggregated_indice'])['low'].agg('min')

    data['aggregated_volume'] =  data['aggregated_indice'].map(volumefrom)
    data['aggregated_high'] =  data['aggregated_indice'].map(high)
    data['aggregated_low'] =  data['aggregated_indice'].map(low)

    data = data[::-lag]
    data = data.iloc[::-1]

    data['hl'] = (data['aggregated_high'] - data['aggregated_low'])/data['aggregated_low']
    data['volu_hi_low'] = data['aggregated_volume']*data['hl']

    data['close_ret']=data['close'].pct_change()
    data['high_ret']=data['aggregated_high'].pct_change()

    data['volu_hi_low_pct_rank'] = data['volu_hi_low'].rank(pct=True)
    data['close_ret_pct_rank'] = data['close_ret'].rank(pct=True)
    data['high_ret_pct_rank'] = data['high_ret'].rank(pct=True)

    signal = np.nan
    try:
        if slope_column == 'close':
            signal = data['close_ret_pct_rank'].iloc[-1]
        elif slope_column == 'high':
            signal = data['high_ret_pct_rank'].iloc[-1]
    except Exception as e:
        print(e)

    return contravariant*signal

def counting_candles(data= None, low_threshold = 0.3, up_threshold = 0.8, contravariant = -1., lag = 2, **kwargs):
    data['close_diff']= (data.close.diff() >= 0.).astype(float)

    ## aggregating the volumes by lag
    data.index = range(0,len(data))
    all_indices = list(reversed(range(len(data) - 1, 0, -lag)))
    data['aggregated_indice'] = np.nan
    data['aggregated_indice'].loc[all_indices] = all_indices
    data['aggregated_indice']= data['aggregated_indice'].fillna(method='bfill')
    data['aggregated_indice'] = data['aggregated_indice'].astype(int)
    volumefrom = data.groupby(['aggregated_indice'])['volumefrom'].agg('sum')
    high = data.groupby(['aggregated_indice'])['high'].agg('max')
    low = data.groupby(['aggregated_indice'])['low'].agg('min')
    close_diff = data.groupby(['aggregated_indice'])['close_diff'].agg('sum')

    data['aggregated_volume'] =  data['aggregated_indice'].map(volumefrom)
    data['aggregated_high'] =  data['aggregated_indice'].map(high)
    data['aggregated_low'] =  data['aggregated_indice'].map(low)
    data['aggregated_close_diff'] =  data['aggregated_indice'].map(close_diff)

    data = data[::-lag]
    data = data.iloc[::-1]


    data['positive_candle_pct_rank'] = data['aggregated_close_diff'].rank(pct=True)

    ratio_rank = data['positive_candle_pct_rank'].iloc[-1]

    if ratio_rank >= up_threshold:
        return contravariant
    elif ratio_rank <= low_threshold:
        return -contravariant
    else:
        return np.nan