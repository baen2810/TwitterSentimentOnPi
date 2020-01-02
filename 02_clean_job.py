import pandas as pd
import os
import time
import logging
import traceback
from datetime import datetime
from helpers import clean_tweets
from config import data_raw, data_cleaned, move_data_cleaned
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
    source_dir = root_dir + data_raw
    target_dir = root_dir + data_cleaned
    processed_dir = source_dir + wf + data_processed
    error_dir = source_dir + wf + data_error
    move = move_data_cleaned

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
                df_out = clean_tweets(df)
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
                print("... skipped - an error occurred: ", e)
                logger.error(e)
                traceback.print_exc(file=t)
                os.rename(source_file_name_full, error_file_name_full)
                # t.close()
                continue

        t.close()
        print(datetime.now(), ': Sleeping for ', sleep_time, ' seconds')
        time.sleep(sleep_time)
