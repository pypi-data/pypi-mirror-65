#!/usr/bin/env python
# coding: utf-8

from abc import ABC, abstractmethod

import pandas as pd

from napoleontoolbox.file_saver import dropbox_file_saver
from napoleontoolbox.utility import metrics

from napoleontoolbox.signal import signal_generator
from napoleontoolbox.signal import signal_utility

import json



class AbstractRunner(ABC):
    def __init__(self, starting_date = None, running_date = None, drop_token=None, dropbox_backup = True, freqly_pkl_file_name='freqly_candels.pkl', local_root_directory='../data/', user = 'napoleon'):
        super().__init__()
        self.freqly_pkl_file_name=freqly_pkl_file_name
        self.local_root_directory=local_root_directory
        self.user=user
        self.dropbox_backup = dropbox_backup
        self.dbx = dropbox_file_saver.NaPoleonDropboxConnector(drop_token=drop_token,dropbox_backup=dropbox_backup)
        self.running_date = running_date
        self.starting_date = starting_date

    @abstractmethod
    def runTrial(self,saver,  seed, trigger, signal_type, idios_string, transaction_costs):
        pass

class SimpleSignalRunner(AbstractRunner):
    def runTrial(self, saver, seed, trigger, signal_type, idios_string, transaction_costs, normalization):
        idios = json.loads(idios_string)
        common_params ={
            'trigger' : trigger,
            'signal_type' : signal_type,
            'transaction_costs' : transaction_costs,
            'normalization' : normalization
        }
        common_params.update(idios)
        saving_key = json.dumps(common_params, sort_keys=True)
        saving_key = signal_utility.convert_to_sql_column_format(saving_key)
        check_run_existence = saver.checkRunExistence(saving_key)
        if check_run_existence:
            return
        if normalization and not signal_generator.is_signal_continuum(signal_type):
            print('not normalizing a not continuous signal')
            return
        print('Launching computation with parameters : '+saving_key)
        freqly_df = pd.read_pickle(self.local_root_directory+self.freqly_pkl_file_name)
        freqly_df = freqly_df.sort_index()
        print('time range before filtering ')
        print(max(freqly_df.index))
        print(min(freqly_df.index))
        freqly_df = freqly_df[freqly_df.index >= self.starting_date]
        freqly_df = freqly_df[freqly_df.index <= self.running_date]
        print('time range after filtering ')
        print(max(freqly_df.index))
        print(min(freqly_df.index))
        if signal_type == 'long_only':
            freqly_df['signal']=1.
        else:
            lookback_window = idios['lookback_window']
            skipping_size = lookback_window
            # kwargs = {**generics, **idios}
            signal_generation_method_to_call = getattr(signal_generator, signal_type)
            try:
                freqly_df = signal_utility.roll_wrapper(freqly_df, lookback_window, skipping_size,
                                                        lambda x: signal_generation_method_to_call(data=x, **idios),
                                                        trigger)
            except Exception as inst:
                print('Trouble backtesting signal')
                print(inst)
                return
        freqly_df = signal_utility.reconstitute_signal_perf(data = freqly_df, transaction_cost = transaction_costs , normalization = normalization)
        sharpe_strat = metrics.sharpe(freqly_df['perf_return'].dropna(), period= 252 * 24, from_ret=True)
        sharpe_under = metrics.sharpe(freqly_df['close_return'].dropna(), period= 252 * 24, from_ret=True)
        print('underlying sharpe')
        print(sharpe_under)
        print('strat sharpe')
        print(sharpe_strat)
        #saver.saveResults(savingKey, freqly_df[['perf_return','turn_over']])
        saver.saveAll(saving_key, freqly_df)
        return






