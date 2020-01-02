import numpy as np
import pandas as pd
import os
import time
import logging
import traceback
from datetime import datetime
from config import data_sentiment, data_analysis, move_data_analysis
from config import data_processed, data_error, sleep_time, wf

# Check to see if this file is being executed as the "Main" python
# script instead of being used as a module by some other python script
if __name__ == '__main__':

    # Root dir
    root_dir = os.getcwd()+'/'
    try:
        script_name = os.path.splitext(__file__)[0].split('/')
        script_name = script_name[len(script_name)-1]
    except Exception:
        script_name = 'jupyterNB'

    # MODIFY I/O
    source_dir = root_dir + data_sentiment
    target_dir = root_dir + data_analysis
    processed_dir = source_dir + wf + data_processed
    error_dir = source_dir + wf + data_error
    move = move_data_analysis

    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
    if not os.path.exists(error_dir):
        os.makedirs(error_dir)

    # Interrupt loop by pressing Strg-C
    while True:

        # get list of files from source directory
        files = os.listdir(source_dir)
        files.sort()

        # Logging
        logging.basicConfig(
                filename=target_dir+wf+script_name+'.logging',
                level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(name)s %(message)s')
        logger = logging.getLogger(__name__)
        t = open(target_dir+wf+script_name+".traceback", "w")

        for file_name in files:
            try:
                # ignore any non-relevant files
                source_file_name_full = source_dir + file_name
                target_file_name_full = target_dir + file_name
                processed_file_name_full = processed_dir + file_name
                error_file_name_full = error_dir + file_name

                print("\nProcessing ", source_file_name_full, "...")

                if file_name.startswith("_"):
                    print("... skipped - not an input file.")
                    continue

                # skip, if already present in target directory
                if os.path.isfile(target_file_name_full):
                    print("... skipped - found: ", target_file_name_full)
                    continue

                # load file into dataframe
                df = pd.read_csv(source_file_name_full)
                print("... input loaded.")

                # MODIFY PROCESSING INPUT
                df_out = df.copy()
                # filename
                df_out['filename'] = file_name

                # datetime
                df_out['datetime'] = pd.to_datetime(df_out['date'])
                df_out['year'] = df_out['datetime'].dt.year
                df_out['month'] = df_out['datetime'].dt.month
                df_out['day'] = df_out['datetime'].dt.day
                df_out['hour'] = df_out['datetime'].dt.hour
                df_out['minute'] = df_out['datetime'].dt.minute
                df_out['second'] = df_out['datetime'].dt.second

                # stance
                df_out['te_stance_ntl'] = np.where(
                        df_out['text_te_stance'] == 0, 1, np.nan
                        )
                df_out['te_stance_pos'] = np.where(
                        df_out['text_te_stance'] == 1, 1, np.nan
                        )
                df_out['te_stance_neg'] = np.where(
                        df_out['text_te_stance'] == -1, 1, np.nan
                        )

                # aggregate
                df_out = pd.DataFrame(df_out.groupby(
                        ['filename', 'year', 'month', 'day', 'hour', 'lang']
                        ).count())
                df_out['tweet_cnt'] = df_out['id']
                df_out['te_stance_cnt'] = df_out['text_te_stance']
                df_out = df_out.reset_index()
                df_out = df_out[['filename', 'year', 'month', 'day', 'hour',
                                 'lang', 'tweet_cnt', 'te_stance_cnt',
                                 'te_stance_ntl', 'te_stance_pos',
                                 'te_stance_neg']]

                print("... input processed.")

                # save file to target directory
                df_out.to_csv(target_file_name_full, index=False)
                print("... output written:\t", target_file_name_full)

                # move source file to "processed" subfolder
                if move:
                    os.rename(source_file_name_full, processed_file_name_full)
                    print("... input moved:\t", processed_file_name_full)
                else:
                    print("... input remains at:\t", source_file_name_full)

            except Exception as e:
                os.rename(source_file_name_full, error_file_name_full)
                logger.error(e)
                print("... skipped - an error occurred: ", e)

                # some errors can't be logged properly
                try:
                    traceback.print_exc(file=t)
                except Exception:
                    print("... additional logging error occurred")
                    # t.close()

                continue

        t.close()
        print(datetime.now(), ': Sleeping for ', sleep_time, ' seconds')
        time.sleep(sleep_time)
