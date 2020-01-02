from helpers import twitter_stream_listener_extended
import pandas as pd
import tweepy as tp
import os
from datetime import datetime
import logging
import traceback

# Check to see if this file is being executed as the "Main" python
# script instead of being used as a module by some other python script
if __name__ == '__main__':
	# Get authorization
	# To get keys and secrets: https://developer.twitter.com
	# - register twitter account as developer
	# - create new app
	# - receive oauth-tokens from dev portal
	
    # Root dir
    root_dir = os.getcwd()+'/'
    try:
        script_name =os.path.splitext(__file__)[0]
    except:
        script_name ='jupyterNB'
	
	# Interrupt loop by pressing Strg-C
	while True:
		try:
			from config import *
			df = pd.read_csv(root_dir+filter_file)
			
			# CONFIGURE TOPIC
			topic_name = topic_name_B
			consumer_key = consumer_key_B
			consumer_secret = consumer_secret_B
			access_token = access_token_B
			access_token_secret = access_token_secret_B

			# Logging
			logging.basicConfig(filename=root_dir+data_raw+'_'+script_name+'_'+topic_name+'.logging', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
			logger=logging.getLogger(__name__)
			t = open(root_dir+data_raw+'_'+script_name+'_'+topic_name+".traceback", "w")

			# File timestamp
			sec= datetime.now().strftime('%S')
			min = datetime.now().strftime('%M') 
			hour = datetime.now().strftime('%H')
			day = datetime.now().strftime('%d')
			month = datetime.now().strftime('%m')
			year = datetime.now().strftime('%y')
			
			ts = year+month+day+"_"+hour+min+sec

			auth = tp.OAuthHandler(consumer_key, consumer_secret)
			auth.set_access_token(access_token, access_token_secret)
			api = tp.API(auth)

			filter_track = list(df[script_name])
			filter_track_cleaned = [x for x in filter_track if str(x) != 'nan']
			full_working_filename= root_dir+data_raw+wf+topic_name+'_'+str(time_limit)+'s_'+ts+'.csv'
			full_filename= root_dir+data_raw+topic_name+'_'+str(time_limit)+'s_'+ts+'.csv'

			twitter_stream_listener_extended(auth, full_working_filename, filter_track_cleaned, time_limit=time_limit, verbose=1)
			
			os.rename(full_working_filename, full_filename)
			
			del topic_name, topic_name_A, topic_name_B, topic_name_C, filter_track, filter_track_cleaned, time_limit, sleep_time
			#t.close()
			
		except Exception as e:
			logger.error(e)
			traceback.print_exc(file=t)
			#t.close()
			continue
			
		finally:
			# optional clean up code
			#t.close()
			pass