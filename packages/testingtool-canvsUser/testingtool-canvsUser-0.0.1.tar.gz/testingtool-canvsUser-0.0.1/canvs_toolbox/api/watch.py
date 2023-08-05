import http.client
import json
import pandas as pd
import datetime
import time
import os

def post_backfill(api_key, data_mode, start_date, end_date):
    # Dict to formatted request body (To be converted to JSON String Payload)

    request_body = {
        "APIToken": "2cfddfbfb565f846395a3dc98c2c59da658a25a6d5b835196c10059d1dbe240c",
        "start": "1506484800000",
        "end": "1506830399999",
        "type": "json",
        "replies": True,
        "displayMode": "volume",
        "ranker": "Posts",
        "includes": {
            "parentCompanies": [],
            "genres": [],
            "shows": [],
            "posts": [],
            "postTypes": [],
            "creators": [],
            "creatorTypes": [],
            "withTags": [],
            "messageTags": [],
            "brandedContent": [],
            "dayOfWeek": []
        },
        "excludes": {
            "parentCompanies": [],
            "genres": [],
            "shows": [],
            "posts": [],
            "postTypes": [],
            "creators": [],
            "creatorTypes": [],
            "withTags": [],
            "messageTags": [],
            "brandedContent": [],
            "dayOfWeek": []
        }
    }

    day = 86400000  # Duration of day in epoch time
    week = day * 7
    year = day * 365

    increment_type = day  # What increment to pull data e.g. daily, weekly

    start = (str(start_date) + ' 00:00:00')
    end = (str(end_date) + ' 23:59:59')

    # Set pattern for epoch converssion
    pattern = '%m/%d/%y %H:%M:%S'

    # Convert start and end strings back to epoch time in miliseconds
    epoch_start = int(time.mktime(time.strptime(start, pattern))) * 1000
    epoch_end = int(time.mktime(time.strptime(end, pattern))) * 1000

    time_increment = int(round((epoch_end - epoch_start) / increment_type, 0))

    # set API call params
    allowed_calls = 250
    mins_allowed = 60

    # Calculate API calls per second
    api_call_freq = (mins_allowed * 60) / allowed_calls

    # API Request

    connection = http.client.HTTPConnection("api.test.canvs.social")

    headers = {'content-type': "application/json"}

    request_body['APIToken'] = api_key

    # Create empty dataframe for loading in api results
    api_result_df = pd.DataFrame()

    # Initialized parameters to feed into for loop
    api_query_start = epoch_start
    api_query_end = epoch_start + (increment_type - 1)

    # Set api start
    api_start_time = time.time()

    # Iterate by time increment across duration of start and end date
    for i in range(time_increment):

        # Modify request body start and end date
        request_body['start'] = api_query_start
        request_body['end'] = api_query_end

        # Query API with modified payload
        payload = json.dumps(request_body)
        connection.request("POST", "/explore/canvs-watch", payload, headers)

        result = connection.getresponse()
        raw_data = json.loads(result.read())

        # Navigate to the portion of the dictionary to be converted to DF
        show_data = raw_data['data']['posts']

        # Convert dict to df
        df = pd.DataFrame(show_data)
        df.drop(df.index[0], inplace=True)  # drop average column from results
        df['timestamp_epoch'] = api_query_start
        df['date_est'] = time.strftime('%m/%d/%y',
                                       time.localtime((api_query_start / 1000)))  # strftime takes arg in seconds

        # Append new data to master dataframe
        api_result_df = api_result_df.append(df)

        # Update start and end date for next iteration
        api_query_start = api_query_start + increment_type
        api_query_end = api_query_start + (increment_type - 1)

        # Print out results to test time logic
        print(i, request_body['start'], request_body['end'], "calls per second", api_call_freq)

        api_end_time = float(api_call_freq - (time.time() - api_start_time))

        if api_end_time > 0:
            time.sleep(api_end_time)

        api_start_time = time.time()

    api_result_df.reset_index(inplace=True)
    api_result_df.drop(labels='index', inplace=True, axis=1)

    # convert dict of emotion results to emotional dataframe
    elem = api_result_df.loc[0, "emotionsDrilldownVolume"]

    emo_df = pd.DataFrame([[list(elem.values())[0] for elem in api_result_df.loc[i, "emotionsDrilldownVolume"]] for i in
                           api_result_df.index])

    emotions = ['love', 'crazy', 'enjoy', 'excited', 'funny', 'hate', 'beautiful', 'happy', 'congrats', 'afraid',
                'dislike', \
                'sad', 'angry', 'annoying', 'disappointed', 'boring', 'cried', 'unsure', 'idiot', 'awkward',
                'brilliant', \
                'brutal', 'weird', 'interesting', 'ugly', 'badass', 'looks_good', 'sentimental', 'nervous',
                'disgusting', \
                'jealous', 'lucky', 'worried', 'thrilling', 'embarrassing', 'fake', 'goosebumps', 'supportive',
                'not_funny', \
                'fml', 'not_scary', 'rage', 'mixed']

    emo_df.columns = emotions

    complete_df = pd.concat([api_result_df.drop(['emotionsDrilldownVolume'], axis=1), emo_df], axis=1)

    complete_df['query_date'] = datetime.datetime.now().timestamp()

    # replace spaces with underscores and lowercase all columns
    complete_df.columns = complete_df.columns.str.replace(' ', '_')
    complete_df.columns = map(str.lower, complete_df.columns)

    # Format name of csv
    csv_name = 'watch_post_backfill_' + start_date + '_' + end_date + '.csv'

    csv_name = csv_name.replace('/', '.')

    # Drop file in data pull folder. Create folder if it does not currently exist
    outdir = 'api_exports/watch'
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    fullname = os.path.join(outdir, csv_name)

    # Print resuts to CSV
    complete_df.to_csv(fullname, index=False, encoding='utf-8-sig')

def series_backfill(api_key, data_mode, start_date, end_date):
    # Dict to formatted request body (To be converted to JSON String Payload)

    request_body = {
        "APIToken": "2cfddfbfb565f846395a3dc98c2c59da658a25a6d5b835196c10059d1dbe240c",
        "start": "1506484800000",
        "end": "1506830399999",
        "type": "json",
        "replies": True,
        "displayMode": "volume",
        "ranker": "Shows, Parent Company",
        "includes": {
            "parentCompanies": [],
            "genres": [],
            "shows": [],
            "posts": [],
            "postTypes": [],
            "creators": [],
            "creatorTypes": [],
            "withTags": [],
            "messageTags": [],
            "brandedContent": [],
            "dayOfWeek": []
        },
        "excludes": {
            "parentCompanies": [],
            "genres": [],
            "shows": [],
            "posts": [],
            "postTypes": [],
            "creators": [],
            "creatorTypes": [],
            "withTags": [],
            "messageTags": [],
            "brandedContent": [],
            "dayOfWeek": []
        }
    }

    day = 86400000  # Duration of day in epoch time
    week = day * 7
    year = day * 365

    increment_type = day  # What increment to pull data e.g. daily, weekly

    start = (str(start_date) + ' 00:00:00')
    end = (str(end_date) + ' 23:59:59')

    # Set pattern for epoch converssion
    pattern = '%m/%d/%y %H:%M:%S'

    # Convert start and end strings back to epoch time in miliseconds
    epoch_start = int(time.mktime(time.strptime(start, pattern))) * 1000
    epoch_end = int(time.mktime(time.strptime(end, pattern))) * 1000

    time_increment = int(round((epoch_end - epoch_start) / increment_type, 0))

    # set API call params
    allowed_calls = 250
    mins_allowed = 60

    # Calculate API calls per second
    api_call_freq = (mins_allowed * 60) / allowed_calls

    # API Request
    connection = http.client.HTTPConnection("api.test.canvs.social")

    headers = {'content-type': "application/json"}

    request_body['APIToken'] = api_key

    # Create empty dataframe for loading in api results
    api_result_df = pd.DataFrame()

    # Initialized parameters to feed into for loop
    api_query_start = epoch_start
    api_query_end = epoch_start + (increment_type - 1)

    # Set api start
    api_start_time = time.time()

    # Iterate by time increment across duration of start and end date
    for i in range(time_increment):

        # Modify request body start and end date
        request_body['start'] = api_query_start
        request_body['end'] = api_query_end

        # Query API with modified payload
        payload = json.dumps(request_body)
        connection.request("POST", "/explore/canvs-watch", payload, headers)

        result = connection.getresponse()
        raw_data = json.loads(result.read())

        # Navigate to the portion of the dictionary to be converted to DF
        show_data = raw_data['data']['shows']

        # Convert dict to df
        df = pd.DataFrame(show_data)
        df.drop(df.index[0], inplace=True)  # drop average column from results
        df['timestamp_epoch'] = api_query_start
        df['date_est'] = time.strftime('%m/%d/%y',
                                       time.localtime((api_query_start / 1000)))  # strftime takes arg in seconds

        # Append new data to master dataframe
        api_result_df = api_result_df.append(df)

        # Update start and end date for next iteration
        api_query_start = api_query_start + increment_type
        api_query_end = api_query_start + (increment_type - 1)

        # Print out results to test time logic
        print(i, request_body['start'], request_body['end'], "calls per second", api_call_freq)

        api_end_time = float(api_call_freq - (time.time() - api_start_time))

        if api_end_time > 0:
            time.sleep(api_end_time)

        api_start_time = time.time()

    api_result_df.reset_index(inplace=True)
    api_result_df.drop(labels='index', inplace=True, axis=1)

    # convert dict of emotion results to emotional dataframe
    elem = api_result_df.loc[0, "emotionsDrilldownVolume"]

    emo_df = pd.DataFrame([[list(elem.values())[0] for elem in api_result_df.loc[i, "emotionsDrilldownVolume"]] for i in
                           api_result_df.index])

    emotions = ['love', 'crazy', 'enjoy', 'excited', 'funny', 'hate', 'beautiful', 'happy', 'congrats', 'afraid',
                'dislike', \
                'sad', 'angry', 'annoying', 'disappointed', 'boring', 'cried', 'unsure', 'idiot', 'awkward',
                'brilliant', \
                'brutal', 'weird', 'interesting', 'ugly', 'badass', 'looks_good', 'sentimental', 'nervous',
                'disgusting', \
                'jealous', 'lucky', 'worried', 'thrilling', 'embarrassing', 'fake', 'goosebumps', 'supportive',
                'not_funny', \
                'fml', 'not_scary', 'rage', 'mixed']

    emo_df.columns = emotions

    complete_df = pd.concat([api_result_df.drop(['emotionsDrilldownVolume'], axis=1), emo_df], axis=1)

    complete_df['query_date'] = datetime.datetime.now().timestamp()

    # replace spaces with underscores and lowercase all columns
    complete_df.columns = complete_df.columns.str.replace(' ', '_')
    complete_df.columns = map(str.lower, complete_df.columns)

    # Format name of csv
    csv_name = 'watch_series_backfill_' + start_date + '_' + end_date + '.csv'

    csv_name = csv_name.replace('/', '.')

    # Drop file in data pull folder. Create folder if it does not currently exist
    outdir = 'api_exports/watch'
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    fullname = os.path.join(outdir, csv_name)

    # Print resuts to CSV
    complete_df.to_csv(fullname, index=False, encoding='utf-8-sig')