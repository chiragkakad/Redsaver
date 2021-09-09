"""
Redsaver v0.1: tool for local SubReddit archive creation

Copyright (c) 2017-2021 Chirag Kakad

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

# !/usr/bin/env python3
import argparse
import time
import json
import os
import sys
from psaw import PushshiftAPI


def to_json(data, name):
    """
        Saves the subreddit archive as a JSON object.
        Parameters:
            data (dict): The archived data.
            Name (str): The name of the file.
    """
    name += '.json'
    # Loads the data in the memory if the file exists
    if os.path.isfile(name):
        with open(name, 'r') as in_file:
            data_tmp = json.load(in_file)
            for post in data_tmp.keys():
                data[post] = {}
                for key in data_tmp[post].keys():
                    data[post][key] = data_tmp[post][key]
    with open(name, 'w') as out_file:
        json.dump(data, out_file)


def save_config(time_config):
    """
    Saves the config to file in the current working directory.
    Parameters:
        time_config (dict):The config dict.
    """
    with open('config.json', 'w') as outfile:
        json.dump(time_config, outfile)


def load_config():
    """
        Loads the config file which stores the last archive date of the sub.
    """
    time_config = {}
    open('config.json', 'a').close()  # Creates the file if it does not exist.
    if os.stat("config.json").st_size != 0:
        with open('config.json', 'r') as json_file:
            try:
                time_config = json.load(json_file)
            except ValueError:
                print('Decoding JSON has failed')
    else:
        time_config = {}
    return time_config


def archive(sub, time_config):
    """
    Archives the given subReddit.
    Parameters:
        sub (str): Name of the sub Reddit to archive.
        time_config (dict): A dictionary consisting of the last archive date.
    Returns:
        Dict:
            Dictionary containing post and meta-data from the subReddit.
    """
    data = {}
    api = PushshiftAPI()
    # Start here and go backwards
    start_epoch = int(time.time())
    after = 0000
    if sub in time_config.keys():
        after = int(time_config[sub])  # Continues from last update.
    time_config[sub] = start_epoch
    print('Archiving /r/' + sub + '.')
    for i in range(1):
        # Generator that will only give you 2000 at a time
        post_list = api.search_submissions(
            before=start_epoch,
            after=after,
            subreddit=sub,
            filter=['id', 'title', 'selftext', 'score'],
            limit=2000)
        if api.metadata_.get('total_results') == 0:
            break
        for post in post_list:
            # Some posts don't have .selftext
            selftext = ""
            if hasattr(post, "selftext"):
                selftext = post.selftext

            data[post.id] = {}
            data[post.id]['time'] = post.created_utc
            data[post.id]['score'] = post.score
            data[post.id]['title'] = post.title
            data[post.id]['text'] = selftext

        # next search to start where the last entry
            start_epoch = post.created_utc
        print(i)
    # be nice to rate limits
        time.sleep(1)
    return data


# Initiate the parser
parser = argparse.ArgumentParser(description="Redsaver: a tool to archive text posts from Subreddits.")

# Add long and short argument
parser.add_argument("--subreddit", "-s", help="The subreddit to archive.")
# Read arguments from the command line
args = parser.parse_args()
# Loads the config file. If the file does not exist it will be created.
config = load_config()

if args.subreddit:
    raw_data = archive(sub=args.subreddit, time_config=config)
    to_json(data=raw_data, name=args.subreddit)
    save_config(config)  # Saves the config to file.
else:
    sys.exit()
