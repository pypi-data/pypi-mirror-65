#!/usr/bin/env python
# coding: utf-8

def generate_lead_lag(lookback_windows, contravariants, lead_lags, lag_lags, ranging_stride, starting_lag = 5, starting_lead = 2):
    parameters = []
    lookback_window = max(lookback_windows)
    if lead_lags is None:
        for contravariant in contravariants:
            for lag in range(starting_lag, lookback_window, ranging_stride):
                for lead in range(starting_lead, lag, ranging_stride):
                    parameters.append({
                        'lead':lead,
                        'lag':lag,
                        'lookback_window':lookback_window,
                        'contravariant':contravariant
                    })
    else :
        for contravariant in contravariants:
            for lag in lag_lags:
                for lead in lead_lags:
                    parameters.append({
                        'lead':lead,
                        'lag':lag,
                        'lookback_window':lookback_window,
                        'contravariant':contravariant
                    })
    return parameters

def generate_dd_threshold(lookback_windows, low_thresholds, up_thresholds, lags, contravariants):
    parameters = []
    for lookback_window in lookback_windows:
        for contravariant in contravariants:
            for low_threshold in low_thresholds:
                for up_threshold in up_thresholds:
                    for lag in lags:
                        parameters.append({
                            'lookback_window':lookback_window,
                            'contravariant':contravariant,
                            'low_threshold':low_threshold,
                            'up_threshold':up_threshold,
                            'lag':lag
                        })
    return parameters

def generate_lookback_only(lookback_windows):
    parameters = []
    for lookback_window in lookback_windows:
                parameters.append({
                    'lookback_window':lookback_window
                })
    return parameters

def generate_lookback_contravariant(lookback_windows, contravariants):
    parameters = []
    for lookback_window in lookback_windows:
        for contravariant in contravariants:
            parameters.append({
                'lookback_window':lookback_window,
                'contravariant':contravariant
            })
    return parameters


def generate_alpha_8(lookback_windows, contravariants, lags):
    parameters = []
    for lookback_window in lookback_windows:
        for lag in lags:
            for contravariant in contravariants:
                if lag <= lookback_window/4:
                    parameters.append({
                        'lookback_window':lookback_window,
                        'lag' : lag,
                        'contravariant':contravariant
                    })
    return parameters

def generate_volume_weighted_high_low_vol(lookback_windows, vol_thresholds, up_trend_thresholds,  low_trend_thresholds, contravariants, lags, display):
    parameters = []
    for lookback_window in lookback_windows:
        for contravariant in contravariants:
            for vol_threshold in vol_thresholds:
                for up_trend_threshold in up_trend_thresholds:
                    for low_trend_threshold in low_trend_thresholds:
                        for lag in lags:
                            if lag <= int(lookback_window/2):
                                parameters.append({
                                    'lookback_window':lookback_window,
                                    'contravariant':contravariant,
                                    'vol_threshold':vol_threshold,
                                    'up_trend_threshold':up_trend_threshold,
                                    'low_trend_threshold': low_trend_threshold,
                                    'lag':lag,
                                    'display' : display
                                })
    return parameters

def generate_slope_induced(lookback_windows, contravariants, lags, slope_columns, up_trend_thresholds,  low_trend_thresholds, display):
    parameters = []
    for slope_column in slope_columns:
        for lookback_window in lookback_windows:
            for contravariant in contravariants:
                for lag in lags:
                    for up_trend_threshold in up_trend_thresholds:
                        for low_trend_threshold in low_trend_thresholds:
                            if lag <= int(lookback_window/2):
                                parameters.append({
                                    'lookback_window':lookback_window,
                                    'contravariant':contravariant,
                                    'up_trend_threshold': up_trend_threshold,
                                    'low_trend_threshold': low_trend_threshold,
                                    'lag':lag,
                                    'slope_column': slope_column,
                                    'display' : display
                                })
    return parameters

def generate_slope_induced_cont(lookback_windows, contravariants, lags, slope_columns, display):
    parameters = []
    for slope_column in slope_columns:
        for lookback_window in lookback_windows:
            for contravariant in contravariants:
                for lag in lags:

                    if lag <= int(lookback_window/2):
                        parameters.append({
                            'lookback_window':lookback_window,
                            'contravariant':contravariant,
                            'lag':lag,
                            'slope_column': slope_column,
                            'display' : display
                        })
    return parameters


def generate_volume_weighted_high_low_vol_cont(lookback_windows, contravariants, lags, display):
    parameters = []
    for lookback_window in lookback_windows:
        for contravariant in contravariants:
            for lag in lags:
                if lag <= int(lookback_window/2):
                    parameters.append({
                        'lookback_window':lookback_window,
                        'contravariant':contravariant,
                        'lag':lag,
                        'display' : display
                    })
    return parameters