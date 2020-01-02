# TwitterSentimentOnPi

An (almost) complete pipeline of machine-learning preprocessing and  to analyze sentiments on twitter data pulled continually using a Raspberry Pi.


Documentation
-------------

* Uses Tweepy API to pull data from Twitter API
* For setting up a Twitter dev account and getting access to the API see Marcello's introduction (link below)
* All jobs fire up as a standalone while-True loop
* Collect jobs should be executed on Raspberry Pi (jobs A, B, C can be run in parallel)
* All jobs create their own input and output directories where they pick up input data from the previous job and store output data for the following job; processed input data will be stored in `./_processed`
* Config.py for configuration of all jobs and filter_track.csv to define keywords to search twitter for


Install
--------

Install requirements:

```Python
pip install requirements.txt
```


Usage
--------

Configure jobs using: config.py and filter_track.csv

Start collect jobs on your Raspberry Pi, each in a separate python console:

```Python
python 01_collect_job_A.py
python 01_collect_job_B.py
python 01_collect_job_C.py
```

Start preprocessing jobs, each in a separate python console:

```Python
python 01_collect_job_A.py
python 02_clean_job.py
python 04_translate_job.py
python 05_sentiment_job.py
python 100_analysis_job.py
```

More Information
----------------

* Preprocessing jobs should run on separate machine since they may be too resource intensive for a Pi

Issues
----------------
* Data transfer from Pi to analytics machine must be done manually (although a job could be easily set up in a similar manner as the other jobs using a network storage
* Translation is not implemented due to GoogleTranslate costs. Pipeline is working on english data only.
* Data transfer between Pi and analytics machine must be done manually

Contributing
------------

Credit goes out to Marcello Rovai and his awesome [introduction to vaderSentiment](https://towardsdatascience.com/almost-real-time-twitter-sentiment-analysis-with-tweep-vader-f88ed5b93b1c).


License
-------

Public domain work. Feel free to do whatever you want with it.
