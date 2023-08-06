#!/usr/bin/env python
# coding: utf-8

from abc import ABC, abstractmethod

import pandas as pd

from napoleontoolbox.file_saver import dropbox_file_saver
from napoleontoolbox.signal import signal_generator
from napoleontoolbox.connector import napoleon_connector
from napoleontoolbox.signal import signal_utility
from napoleontoolbox.parallel_run import signal_result_analyzer
import json


# def reconstitute_signal_perf(data=None, initial_price = 1. , average_execution_cost = 7.5e-4 , transaction_cost = True):
#     data['turn_over'] = abs(data['signal'] - data['signal'].shift(-1).fillna(0.))
#     print('average hourly turn over')
#     print(data['turn_over'].sum() / len(data))
#     data['close_return'] = data['close'].pct_change()
#     data['reconstituted_close'] = metrics.from_ret_to_price(data['close_return'],initial_price=initial_price)
#     data['non_adjusted_perf_return'] = data['close_return'] * data['signal']
#     if transaction_cost :
#         data['perf_return'] = data['non_adjusted_perf_return']- data['turn_over']*average_execution_cost
#     else :
#         data['perf_return'] = data['non_adjusted_perf_return']
#     data['reconstituted_perf'] = metrics.from_ret_to_price(data['perf_return'],initial_price=initial_price)
#     return data
#
# def roll_wrapper(rolled_df, lookback_window, skipping_size, function_to_apply, trigger):
#     signal_df = roll(rolled_df, lookback_window).apply(function_to_apply)
#     signal_df = signal_df.to_frame()
#     signal_df.columns = ['signal_gen']
#     signal_df['signal'] = signal_df['signal_gen'].shift()
#     if trigger:
#         signal_df['signal'] =  signal_df['signal'].fillna(method='ffill')
#
#     signal_df = signal_df.fillna(0.)
#     rolled_df = pd.merge(rolled_df, signal_df, how='left', left_index=True, right_index= True)
#     rolled_df = rolled_df.iloc[skipping_size:]
#     return rolled_df
#
# def roll(df, w):
#     v = df.values
#     d0, d1 = v.shape
#     s0, s1 = v.strides
#     restricted_length = d0 - (w - 1)
#     a = stride(v, (restricted_length, w, d1), (s0, s0, s1))
#     rolled_df = pd.concat({
#         row: pd.DataFrame(values, columns=df.columns)
#         for row, values in zip(df.index[-restricted_length:], a)
#     })
#     return rolled_df.groupby(level=0)



class AbstractRunner(ABC):
    def __init__(self, starting_date = None, running_date = None, drop_token=None, dropbox_backup = True, hourly_pkl_file_name='hourly_candels.pkl',aggregated_pkl_file_name='hourly_to_mix.pkl', aggregated_pkl_mapping_file_name = 'hourly_to_mix_mapping.pkl', list_pkl_file_name = 'my_list.pkl', local_root_directory='../data/', user = 'napoleon', add_turn_over = False, skipping_size=200, recompute_all = True, db_path_suffix=None):
        super().__init__()
        self.hourly_pkl_file_name=hourly_pkl_file_name
        self.aggregated_pkl_file_name=aggregated_pkl_file_name
        self.aggregated_pkl_mapping_file_name=aggregated_pkl_mapping_file_name
        self.list_pkl_file_name = list_pkl_file_name
        self.local_root_directory=local_root_directory
        self.user=user
        self.dropbox_backup = dropbox_backup
        self.dbx = dropbox_file_saver.NaPoleonDropboxConnector(drop_token=drop_token,dropbox_backup=dropbox_backup)
        self.running_date = running_date
        self.starting_date = starting_date
        self.add_turn_over = add_turn_over
        self.skipping_size = skipping_size
        self.signals_list = napoleon_connector.load_pickled_list(local_root_directory=self.local_root_directory,
                                                                 list_pkl_file_name=self.list_pkl_file_name)
        self.recompute_all = recompute_all
        self.db_path_suffix = db_path_suffix
        if not self.recompute_all:
            saver = signal_result_analyzer.ParallelRunResultAnalyzer(drop_token=drop_token,
                                                                     local_root_directory=local_root_directory, user=user,
                                                                     db_path_suffix=self.db_path_suffix)
            self.precomputed_results_df, self.precomputed_signals_df = saver.analyzeAllRunResults()
        else:
            self.precomputed_results_df, self.precomputed_signals_df  = None, None

    @abstractmethod
    def runTrial(self,saver,  seed, trigger, signal_type, idios_string, transaction_costs, normalization):
        pass


class EnsemblingSignalRunner(AbstractRunner):
    def runTrial(self, saver, seed, trigger, transaction_costs, normalization):
        cumulated_signals = None
        print('Number of signals to aggregate '+str(len(self.signals_list)))
        counter = 1
        mapping_dictionary = {}
        for me_signal in self.signals_list:
            # we have to reload the file each time
            hourly_df = pd.read_pickle(self.local_root_directory + self.hourly_pkl_file_name)
            hourly_df = hourly_df.sort_index()
            print('time range before filtering ')
            print(max(hourly_df.index))
            print(min(hourly_df.index))
            hourly_df = hourly_df[hourly_df.index >= self.starting_date]
            hourly_df = hourly_df[hourly_df.index <= self.running_date]
            print('time range after filtering ')
            print(max(hourly_df.index))
            print(min(hourly_df.index))
            close_df = hourly_df.copy()

            ## idiosyncratic run itself
            run_json_string = signal_utility.recover_to_sql_column_format(me_signal)
            params = json.loads(run_json_string)
            signal_type = params['signal_type']
            if normalization and not signal_generator.is_signal_continuum(signal_type):
                return
            signal_column = 'signal'+str(counter)
            mapping_dictionary[me_signal]=[signal_column]
            if self.recompute_all:
                print('Launching computation with parameters : '+run_json_string)
                print('Signal number '+str(counter))
                if signal_type == 'long_only':
                    hourly_df['signal']=1.
                else:
                    lookback_window = params['lookback_window']
                    if self.skipping_size < lookback_window:
                        raise Exception('The skipping size must be greater than the lookback window')
                    # kwargs = {**generics, **idios}
                    signal_generation_method_to_call = getattr(signal_generator, signal_type)
                    hourly_df = signal_utility.roll_wrapper(hourly_df, lookback_window, self.skipping_size,
                                              lambda x: signal_generation_method_to_call(data=x, **params), trigger)
                    hourly_df = signal_utility.reconstitute_signal_perf(data = hourly_df, transaction_cost = transaction_costs, normalization = normalization)
            else :
                if self.add_turn_over:
                    raise Exception('to add turn over, you have to recompute all')
                hourlyperf_df = self.precomputed_results_df[me_signal]
                hourlysig_df = self.precomputed_signals_df[me_signal]
                hourlyperf_df = hourlyperf_df.to_frame()
                hourlyperf_df.columns = ['reconstituted_perf']
                hourlysig_df = hourlysig_df.to_frame()
                hourlysig_df.columns = ['signal']
                hourly_df = hourlyperf_df.merge(hourlysig_df, left_index = True, right_index = True)
                if cumulated_signals is None :
                    hourlyclose_df = close_df['close'].to_frame()
                    hourlyclose_df.columns = ['close']
                    hourly_df = hourly_df.merge(hourlyclose_df, left_index=True, right_index=True)
            if cumulated_signals is None:
                if self.add_turn_over:
                    cumulated_signals = hourly_df[['close','signal','turn_over']]
                    cumulated_signals = cumulated_signals.rename(columns={'signal': signal_column,'turn_over':'turn_over'+str(counter)})
                else :
                    cumulated_signals = hourly_df[['close','signal']]
                    cumulated_signals = cumulated_signals.rename(columns={'signal': signal_column})
            else :
                cumulated_signals[signal_column]=hourly_df['signal']
                if self.add_turn_over:
                    cumulated_signals['turn_over'+str(counter)]=hourly_df['turn_over']
            #hourly_df = hourly_df.drop(columns = ['signal','turn_over','reconstituted_perf','non_adjusted_perf_return','perf_return'])
            counter = counter + 1
        print('saving to '+self.aggregated_pkl_file_name)
        cumulated_signals.to_pickle(self.local_root_directory+self.aggregated_pkl_file_name)
        print('saving to '+self.aggregated_pkl_mapping_file_name)
        pd.DataFrame(mapping_dictionary).to_pickle(self.local_root_directory + self.aggregated_pkl_mapping_file_name)










