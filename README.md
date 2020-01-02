# TwitterSentimentOnPi

An (almost) complete pipeline of machine-learning steps to analyze sentiments on twitter data pulled continually using a Raspberry Pi.
If you want to use factory_bot with Rails, see

Documentation
-------------

tbd

Install
--------

Install requirements:

```ruby
pip install requirements.txt
```


More Information
----------------

* Uses Tweepy API to pull data from Twitter API
* For setting up a Twitter dev account and getting access to the API see Marcello's introduction (link below)
* All jobs fire up as a standalone while-True loop
* Collect jobs should be executed on Raspberry Pi (jobs A, B, C can be run in parallel)
* All jobs create their own input and output directories where they pick up input data from the previous job and store output data for the following job
* Config.py for configuration of all jobs and filter_track.csv to define keywords to search twitter for
* Preprocessing jobs should run on separate machine
* Data transfer between Pi and analytics machine must be done manually

Issues
----------------
* Data transfer from Pi to analytics machine must be done manually (although a job could be easily set up in a similar manner as the other jobs using a network storage
* Translation is not implemented due to GoogleTranslate costs. Pipeline is working on english data only.

Contributing
------------

Credit goes out to Marcello Rovai and his awesome [introduction to vaderSentiment] (https://towardsdatascience.com/almost-real-time-twitter-sentiment-analysis-with-tweep-vader-f88ed5b93b1c).


License
-------

Public domain work. Feel free to do whatever you want with it.


