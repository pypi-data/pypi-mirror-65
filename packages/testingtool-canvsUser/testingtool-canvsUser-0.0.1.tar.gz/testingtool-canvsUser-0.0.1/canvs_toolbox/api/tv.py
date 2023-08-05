import http.client
import json
import pandas as pd
import datetime
import os
import time

def twitter_daily_export(api_key, data_mode, start_date, end_date):
    # Dict to formatted request body (To be converted to JSON String Payload)

    request_body = {
        "247": True,
        "APIToken": "921680db55851173cb6d88d0354f33a27916e24087fc6e3c28508725d57071a8",
        "start": "1501560000000",
        "end": "1504151999999",
        "type": "json",
        "retweets": True,
        "live": False,
        "displayMode": "volume",
        "ranker": "Programs",
        "includes": {
            "programs": [],
            "networks": [],
            "dayparts": [],
            "genres": [],
            "airings": [],
            "dayOfWeek": [],
            "seriesTypes": [],
            "networkTypes": ["OTT"]
        },
        "excludes": {
            "programs": [],
            "networks": [],
            "dayparts": [],
            "genres": [],
            "airings": [],
            "dayOfWeek": [],
            "seriesTypes": [],
            "networkTypes": []
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
    connection = http.client.HTTPConnection("api.canvs.social")

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
        connection.request("POST", "/explore/twitter", payload, headers)

        result = connection.getresponse()
        raw_data = json.loads(result.read())

        # Navigate to the portion of the dictionary to be converted to DF
        show_data = raw_data['data']['programs']

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
    csv_name = 'tv_twitter_daily_export_' + start_date + '_' + end_date + '.csv'

    csv_name = csv_name.replace('/', '.')

    # Drop file in data pull folder. Create folder if it does not currently exist
    outdir = 'api_exports/tv'
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    fullname = os.path.join(outdir, csv_name)

    # Print resuts to CSV
    complete_df.to_csv(fullname, index=False, encoding='utf-8-sig')

def twitter_emotional_authors(api_key, series_id, start_date, end_date):
    # Canvs syndicated landscape series api
    request_body_airing_id = {
        "APIToken": "2cfddfbfb565f846395a3dc98c2c59da658a25a6d5b835196c10059d1dbe240c",
        "seriesId": "3267_FOX",
        "start": "1501560000000",
        "end": "1504151999999"
    }

    # Format parameterized start and end date datetimestamp string, rounded to start and end of day
    start = (str(start_date) + ' 00:00:00')
    end = (str(end_date) + ' 23:59:59')

    # Set pattern for epoch converssion
    pattern = '%m/%d/%y %H:%M:%S'

    # Convert start and end strings back to epoch time in miliseconds
    epoch_start = int(time.mktime(time.strptime(start, pattern))) * 1000
    epoch_end = int(time.mktime(time.strptime(end, pattern))) * 1000

    # Modify JSON request body start and end time in epoch before converting to JSON pyload.
    request_body_airing_id['seriesId'] = series_id
    request_body_airing_id['start'] = epoch_start
    request_body_airing_id['end'] = epoch_end

    connection = http.client.HTTPConnection("api.canvs.social")

    payload_ids = json.dumps(request_body_airing_id)

    headers = {'content-type': "application/json"}

    connection.request("POST", "/catalog-syndicated/landscape-extract", payload_ids, headers)

    result_airing_ids = connection.getresponse()
    raw_data_ids = json.loads(result_airing_ids.read())

    raw_ids_list = raw_data_ids['data']['datasetDrilldown']

    airing_ids = [airing['airingId'] for airing in raw_ids_list]

    master_df = pd.DataFrame([])

    for i in airing_ids:
        request_body_audience_export = {
            "api_key": "2cfddfbfb565f846395a3dc98c2c59da658a25a6d5b835196c10059d1dbe240c",
            "airingId": "EP007517000313_FOX_08142017",
            "type": "json"
        }

        request_body_audience_export['airingId'] = i

        audience_connection = http.client.HTTPConnection("api.test.canvs.social")

        payload_exports = json.dumps(request_body_audience_export)

        headers = {'content-type': "application/json"}

        audience_connection.request("POST", "/catalog-syndicated/users", payload_exports, headers)

        result_user_export = audience_connection.getresponse()
        raw_data_user_export = json.loads(result_user_export.read())

        airing_df = pd.DataFrame()
        airing_df['users'] = raw_data_user_export['data']['users']
        airing_df['season'] = raw_data_user_export['data']['summary']['season']
        airing_df['episode'] = raw_data_user_export['data']['summary']['episode']

        master_df = master_df.append(airing_df, ignore_index=True)

        # Format name of csv
        csv_name = 'tv_twitter_emotional_authors_' + series_id + '_' + start_date + '_' + end_date + '.csv'

        csv_name = csv_name.replace('/', '.')

        # Drop file in data pull folder. Create folder if it does not currently exist
        outdir = 'api_exports/tv'
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        fullname = os.path.join(outdir, csv_name)

        # Print resuts to CSV
        master_df.to_csv(fullname, index=False, encoding='utf-8-sig')

def airings_backfill(api_key, data_mode, start_date, end_date):
    # Dict to formatted request body (To be converted to JSON String Payload)

    request_body = {
        "247": False,
        "APIToken": "921680db55851173cb6d88d0354f33a27916e24087fc6e3c28508725d57071a8",
        "start": "1501560000000",
        "end": "1504151999999",
        "type": "json",
        "retweets": True,
        "live": False,
        "displayMode": "volume",
        "ranker": "Airings",
        "includes": {
            "programs": [],
            "networks": [],
            "dayparts": [],
            "genres": [],
            "airings": [],
            "dayOfWeek": [],
            "seriesTypes": [],
            "networkTypes": []
        },
        "excludes": {
            "programs": [],
            "networks": [],
            "dayparts": [],
            "genres": [],
            "airings": [],
            "dayOfWeek": [],
            "seriesTypes": [],
            "networkTypes": []
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
        connection.request("POST", "/explore/twitter", payload, headers)

        result = connection.getresponse()
        raw_data = json.loads(result.read())

        # Navigate to the portion of the dictionary to be converted to DF
        show_data = raw_data['data']['airings']

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
                'dislike',
                'sad', 'angry', 'annoying', 'disappointed', 'boring', 'cried', 'unsure', 'idiot', 'awkward',
                'brilliant',
                'brutal', 'weird', 'interesting', 'ugly', 'badass', 'looks_good', 'sentimental', 'nervous',
                'disgusting',
                'jealous', 'lucky', 'worried', 'thrilling', 'embarrassing', 'fake', 'goosebumps', 'supportive',
                'not_funny',
                'fml', 'not_scary', 'rage', 'mixed']

    emo_df.columns = emotions

    complete_df = pd.concat([api_result_df.drop(['emotionsDrilldownVolume'], axis=1), emo_df], axis=1)

    complete_df['query_date'] = datetime.datetime.now().timestamp()

    # replace spaces with underscores and lowercase all columns
    complete_df.columns = complete_df.columns.str.replace(' ', '_')
    complete_df.columns = map(str.lower, complete_df.columns)

    # Format name of csv
    csv_name = 'tv_airings_backfill_' + start_date + '_' + end_date + '.csv'

    csv_name = csv_name.replace('/', '.')

    outdir = 'api_exports/tv'
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    fullname = os.path.join(outdir, csv_name)

    # Print results to CSV
    complete_df.to_csv(fullname, index=False, encoding='utf-8-sig')

def facebook_backfill(api_key, data_mode, start_date, end_date):
    # Dict to formatted request body (To be converted to JSON String Payload)

    request_body = {
        "APIToken": "2cfddfbfb565f846395a3dc98c2c59da658a25a6d5b835196c10059d1dbe240c",
        "start": "1506484800000",
        "end": "1506830399999",
        "type": "json",
        "replies": True,
        "displayMode": "volume",
        "ranker": "Programs",
        "includes": {
            "parentCompanies": [],
            "genres": [],
            "shows": [],
            "posts": [],
            "postType": [],
            "networks": [],
            "networkTypes": ["OTT"],
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
            "postType": [],
            "networks": [],
            "networkTypes": [],
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
        connection.request("POST", "/explore/facebook-tv", payload, headers)

        result = connection.getresponse()
        raw_data = json.loads(result.read())

        # Navigate to the portion of the dictionary to be converted to DF
        show_data = raw_data['data']['programs']

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
                'dislike',
                'sad', 'angry', 'annoying', 'disappointed', 'boring', 'cried', 'unsure', 'idiot', 'awkward',
                'brilliant',
                'brutal', 'weird', 'interesting', 'ugly', 'badass', 'looks_good', 'sentimental', 'nervous',
                'disgusting',
                'jealous', 'lucky', 'worried', 'thrilling', 'embarrassing', 'fake', 'goosebumps', 'supportive',
                'not_funny',
                'fml', 'not_scary', 'rage', 'mixed']

    emo_df.columns = emotions

    complete_df = pd.concat([api_result_df.drop(['emotionsDrilldownVolume'], axis=1), emo_df], axis=1)

    complete_df['query_date'] = datetime.datetime.now().timestamp()

    # replace spaces with underscores and lowercase all columns
    complete_df.columns = complete_df.columns.str.replace(' ', '_')
    complete_df.columns = map(str.lower, complete_df.columns)

    # Format name of csv
    csv_name = 'tv_facebook_backfill_' + start_date + '_' + end_date + '.csv'

    csv_name = csv_name.replace('/', '.')

    outdir = 'api_exports/tv'
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    fullname = os.path.join(outdir, csv_name)

    # Print results to CSV
    complete_df.to_csv(fullname, index=False, encoding='utf-8-sig')