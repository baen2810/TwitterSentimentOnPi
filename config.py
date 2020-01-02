# =============================================================================
# General settings
# =============================================================================

# Prefix for working-file
wf = "_"

# =============================================================================
# Collector
# =============================================================================

# Collector (Dev)
consumer_key = 'Rg2TfOuIDTmzCQBudEWjKfZzb'
consumer_secret = 'RdD4CTQn7pDYQqa0bjQ23had7vc4fgX7BjlXmmCZp9pLJ6ixt0'
access_token = '214211525-70IkmKMEwW7Oh1zDmiH7IigfIBAE0FzUfoTudpOg'
access_token_secret = '5UUfFB9pdFTvYPxYUjDNEFZ3wmCUadAVZG1yNcg39XXaB'

# Collector A
consumer_key_A = 'PqEgbVvc8t7UMVzROYwChuUkF'
consumer_secret_A = 'wXJxpXfjQmaaspJWvC4tYuW4FP6NnvXRrJvAkP0WcIMieU9J8r'
access_token_A = '214211525-Mmi1TNst5nAXXAfgF9j9preim6ANmWPEnLQVg6Oj'
access_token_secret_A = '8NGeOWu524p5dHV5Gk5sG8kziMuHkcIoh3Hqj1uG2utSK'

# Collector B
consumer_key_B = '29VUFo7ecuxIdnqg1DV1CVmxi'
consumer_secret_B = 'TKVbl2wl7Euy4EEkfcEt66qlFJM6SiXWXBOzgOgbef4W4mQbIT'
access_token_B = '214211525-SoOp86afIq9NuA5Hx1VXuXLUWMKuqbUjPMr4iU5L'
access_token_secret_B = '0tzMgQZl5UbkWNExmSmqE3Hs4OyYc6tA4JXi5vxZ1rNoI'

# Collector C
consumer_key_C = 'gzUiov5FA5xft6hXi4ApO5rb2'
consumer_secret_C = 'tZLNGufNiNEaRr8JGaErMwkv6mNfqF32XEnd9MPcofqE0DuZtA'
access_token_C = '214211525-xRpgIQuSuvD6YZhRIUzRfU2Bhu8ZfWx6HdaS3dxF'
access_token_secret_C = 'ttGaqibc9T01YlO4lSPaAaInYceE6jC1lSeqrIlA04kP2'

# Batch processing time limit in seconds
time_limit = 900

# Filename of file search parameter for collector
filter_file = 'filter_track.csv'

# =============================================================================
# Preprocessing settings
# =============================================================================

# Sleep time for a job in seconds
sleep_time = 300

# I/O variables
topic_name_A = 'ENTERTAINMENT'
topic_name_B = 'POLITICS'
topic_name_C = 'POL_EVAL'
data_raw = '01_collect/'
data_cleaned = '02_clean/'
data_translated = '04_translate/'
data_sentiment = '05_sentiment/'
data_analysis = '100_analysis/01_tweet_count_analysis/'

# Move to processed?
data_processed = 'processed/'
data_error = 'error/'
move_data_raw = False
move_data_cleaned = True
move_data_translated = True
move_data_sentiment = True
move_data_analysis = True

# Languages to translate
languages = ['en']
