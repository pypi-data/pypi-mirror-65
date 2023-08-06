#!/usr/bin/env python3
# coding: utf-8

import sqlite3
import pandas as pd

from napoleontoolbox.file_saver import dropbox_file_saver
from napoleontoolbox.signal import signal_utility
import json
import hashlib

def unjsonize_mapping_dataframe(mapping_df):
    human_readable_dictionary = {}
    json_params_dictionary = {}
    for col in mapping_df.columns :
        run_json_string = signal_utility.recover_to_sql_column_format(col)
        #saving_key = signal_utility.convert_to_sql_column_format(run_json_string)
        salty = str(int(hashlib.sha1(run_json_string.encode('utf-8')).hexdigest(), 16) % (10 ** 8))
        params = json.loads(run_json_string)
        readable_label = params['signal_type'] + str(params['transaction_costs']) + str(params['normalization']) + salty
        params = json.loads(run_json_string)
        signal_name = mapping_df.iloc[0,mapping_df.columns.get_loc(col)]
        human_readable_dictionary[signal_name] = readable_label
        json_params_dictionary[signal_name] = params
    return human_readable_dictionary, json_params_dictionary

class ParallelRunResultAnalyzer():

    def __init__(self,drop_token='', dropbox_backup=True, local_root_directory='../data',user='napoleon',  db_path_suffix = '_run.sqlite'):
        self.local_root_directory = local_root_directory
        self.user = user
        self.db_path_suffix = db_path_suffix
        self.filename =  user + db_path_suffix
        self.db_path = self.local_root_directory + self.filename
        self.dbx = dropbox_file_saver.NaPoleonDropboxConnector(drop_token=drop_token,dropbox_backup=dropbox_backup)

    def getAllRuns(self):
        sqliteConnection = None
        try:
            sqliteConnection = sqlite3.connect(self.db_path, timeout=20)
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")
            sqlite_select_runs =  """PRAGMA table_info(parallel_run);"""
            cursor.execute(sqlite_select_runs)
            all_runs_tuple = cursor.fetchall()

            cursor.close()
            all_runs = [r[1] for r in all_runs_tuple if not 'date' in r[1]]
            print("Total run numbers :  ", len(all_runs))

            return all_runs
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The Sqlite connection is closed")

    def analyzeRunResults(self, run):
        runs = self.getAllRuns()
        results_df = None

        if run not in runs :
            return results_df

        sqliteConnection = None
        try:
            sqliteConnection = sqlite3.connect(self.db_path, timeout=20)
            sqlite_select_run_query = """SELECT effective_date, """ + run + """_perf_return, """ + run + """_turn_over from parallel_run order by effective_date asc"""
            results_df = pd.read_sql_query(sqlite_select_run_query, sqliteConnection)
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The Sqlite connection is closed")
        return results_df

    def analyzeAllRunResults(self,jsonized_output = True ):
        results_df = self.analyzeAllRunPerfResults(jsonized_output=jsonized_output)
        signals_df = self.analyzeAllRunSignalsResults(jsonized_output=jsonized_output)
        return results_df, signals_df

    def analyzeAllRunSignalsResults(self,jsonized_output = True):
        sqliteConnection = None
        try:
            sqliteConnection = sqlite3.connect(self.db_path, timeout=20)
            sqlite_select_run_query = """SELECT * from parallel_signal order by effective_date asc"""
            results_df = pd.read_sql_query(sqlite_select_run_query, sqliteConnection)
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The Sqlite connection is closed")

        results_df = results_df.rename(columns={"effective_date": "Date"})
        results_df['Date'] = pd.to_datetime(results_df['Date'])
        results_df = results_df.sort_values(by=['Date'])
        results_df = results_df.set_index(results_df['Date'])
        results_df = results_df.drop(['Date'], axis=1)

        run_empty_results = results_df.sum(axis = 0)
        self.empty_runs_to_investigate = list(run_empty_results.index[run_empty_results == 0])

        results_df = results_df.drop(columns=self.empty_runs_to_investigate)

        if not jsonized_output :
            renaming_dictionary = {}
            for col in results_df.columns:
                if col != 'Date':
                    run_json_string=signal_utility.recover_to_sql_column_format(col)
                    params = json.loads(run_json_string)
                    #salty = hashlib.sha256(run_json_string)
                    salty =str(int(hashlib.sha1(run_json_string.encode('utf-8')).hexdigest(), 16) % (10 ** 8))
                    if 'transaction_costs' in params.keys():
                        transacs = str(params['transaction_costs'])
                    else:
                        transacs = ''
                    if 'normalization' in params.keys():
                        normas = str(params['normalization'])
                    else:
                        normas=''
                    renaming_dictionary[col] = params['signal_type']+transacs+normas+salty

            results_df = results_df.rename(columns=renaming_dictionary, errors="raise")
        return results_df

    def analyzeAllRunPerfResults(self,jsonized_output = True):
        sqliteConnection = None
        try:
            sqliteConnection = sqlite3.connect(self.db_path, timeout=20)
            sqlite_select_run_query = """SELECT * from parallel_run order by effective_date asc"""
            results_df = pd.read_sql_query(sqlite_select_run_query, sqliteConnection)
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The Sqlite connection is closed")


        results_df = results_df.rename(columns={"effective_date": "Date"})
        results_df['Date'] = pd.to_datetime(results_df['Date'])
        results_df = results_df.sort_values(by=['Date'])
        results_df = results_df.set_index(results_df['Date'])
        results_df = results_df.drop(['Date'], axis=1)

        run_empty_results = results_df.sum(axis = 0)
        self.empty_runs_to_investigate = list(run_empty_results.index[run_empty_results == 0])

        results_df = results_df.drop(columns=self.empty_runs_to_investigate)

        if not jsonized_output :
            renaming_dictionary = {}
            for col in results_df.columns:
                if col != 'Date':
                    run_json_string=signal_utility.recover_to_sql_column_format(col)
                    params = json.loads(run_json_string)
                    #salty = hashlib.sha256(run_json_string)
                    salty =str(int(hashlib.sha1(run_json_string.encode('utf-8')).hexdigest(), 16) % (10 ** 8))
                    if 'transaction_costs' in params.keys():
                        transacs = str(params['transaction_costs'])
                    else:
                        transacs = ''
                    if 'normalization' in params.keys():
                        normas = str(params['normalization'])
                    else:
                        normas=''
                    renaming_dictionary[col] = params['signal_type']+transacs+normas+salty

            results_df = results_df.rename(columns=renaming_dictionary, errors="raise")
        return results_df




    def download_run_results(self):
        print('downloaoding from dropbox the results to '+self.db_path)
        self.dbx.local_sqlite_overwrite_from_db(sqlite_file_name=self.filename,local_root_directory = self.local_root_directory)

