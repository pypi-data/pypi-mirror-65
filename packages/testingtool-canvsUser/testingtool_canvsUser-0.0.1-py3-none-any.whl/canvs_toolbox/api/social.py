import http.client
import json
import pandas as pd
import time
import os
import logging

# Internal imports
# from utilities import logging_setup

# initialize logging setup
# logging_setup()

log = logging.getLogger(__name__)


# helper function
def query_increments(start_date, end_date, query_increment=None):
    """
    :param query_increment: day (str 'day'), week (str 'week), custom epoch increment (int of epoch time in
    milliseconds, or none. None will return payload in a single api call.

    :param start_date: (Int) epoch time (ms)
    :param end_date: (int) epoch time (ms)
    :return: epoch time increment (ms) to be used as the denominator of the get_facebook_posts api requests.
    """

    day = 86400000

    if query_increment == 'day':

        return day

    elif query_increment == 'week':
        return day * 7

    elif query_increment == type(int):

        return query_increment

    else:

        return int(end_date) - int(start_date)

# Query Canvs Facebook Owned Sources api
def get_facebook_posts(api_key, fb_id, org_id, start_date, end_date, query_increment=None):
    """
    :param api_key:
    :param fb_id:
    :param org_id:
    :param start_date:
    :param end_date:
    :param request_body:
    :param query_increment:
    :return:
    """

    # Default request body
    request_body = {
        "APIToken": "",
        "collectionId": "",
        "start": "1539662400000",
        "end": "1539748800000",
        "count": 29,
        "email": "david@canvs.tv",
        "orgId": "541323e78d7688d418000041",
        "filters": {
            "replies": True,
            "emotions": [],
            "postType": [],
            "brands": [],
            "messageTags": [],
            "withTags": [],
            "datasetId": []
        },
        "includes": {
            "topics": [],
            "hashtags": [],
            "authors": []
        },
        "excludes": {
            "topics": [],
            "hashtags": [],
            "authors": []
        },
        "fromCampaign": False,
        "fromCanvsWatch": False,
        "fromFacebookTV": False,
        "type": "json"
    }

    start = (str(start_date) + ' 00:00:00')
    end = (str(end_date) + ' 23:59:59')

    # Set pattern for epoch conversion
    pattern = '%m/%d/%y %H:%M:%S'

    # Convert start and end strings back to epoch time in milliseconds
    epoch_start = int(time.mktime(time.strptime(start, pattern))) * 1000
    epoch_end = int(time.mktime(time.strptime(end, pattern))) * 1000

    increment = query_increments(start_date=epoch_start, end_date=epoch_end, query_increment=query_increment)

    time_increment = int(round((epoch_end - epoch_start) / increment, 0))  # Divide by seconds of day in epoch

    # set API call params
    allowed_calls = 250
    mins_allowed = 60

    # Calculate API calls per second
    api_call_freq = (mins_allowed * 60) / allowed_calls

    # Format API Request
    connection = http.client.HTTPConnection("api.test.canvs.social")

    headers = {'content-type': "application/json"}

    request_body['APIToken'] = api_key  # Set API key

    request_body['collectionId'] = fb_id  # Set id of owned source to export

    request_body['orgId'] = org_id  # Set org ID to determine permission levels

    # Create empty dataframe for loading in api results
    api_result_df = pd.DataFrame()

    # Initialized parameters to feed into for loop
    api_query_start = epoch_start
    api_query_end = epoch_start + (increment - 1)

    # Set api start
    api_start_time = time.time()

    # Iterate by time increment across duration of start and end date
    for i in range(time_increment):

        # Modify request body start and end date
        request_body['start'] = api_query_start
        request_body['end'] = api_query_end

        # Query API with modified payload
        payload = json.dumps(request_body)

        connection.request("POST", "/catalog-owned/extract", payload, headers)

        result = connection.getresponse()
        raw_data = json.loads(result.read())

        # Navigate to the portion of the dictionary to be converted to DF
        # Normalize to Dataframe

        try:
            flattened_data = pd.io.json.json_normalize(raw_data['data']['datasetDrilldown'])

            # Append new data to master dataframe
            api_result_df = api_result_df.append(flattened_data, sort=False)

            # Update start and end date for next iteration
            api_query_start = api_query_start + increment
            api_query_end = api_query_start + (increment - 1)

            # Print out results to test time logic
            # print('start time {}. end time{}, calls per second {}'.format(request_body['start'],
            #                                                                  request_body['end'],
            #                                                                  api_call_freq))

            print(i, request_body['start'], request_body['end'], 'calls per second', api_call_freq)

            api_result_df.reset_index(inplace=True)
            api_result_df.drop(labels='index', inplace=True, axis=1)

        except Exception as e:
            print("failed to pull fb posts. {}".format(e))
            # print("failed to pull", e)

        finally:
            api_end_time = float(api_call_freq - (time.time() - api_start_time))

            if api_end_time > 0:
                time.sleep(api_end_time)

            api_start_time = time.time()


        emotions = ['love', 'crazy', 'enjoy', 'excited', 'funny', 'hate', 'beautiful', 'happy', 'congrats', 'afraid',
                    'dislike',
                    'sad', 'angry', 'annoying', 'disappointed', 'boring', 'cried', 'unsure', 'idiot', 'awkward',
                    'brilliant',
                    'brutal', 'weird', 'interesting', 'ugly', 'badass', 'looks_good', 'sentimental', 'nervous',
                    'disgusting',
                    'jealous', 'lucky', 'worried', 'thrilling', 'embarrassing', 'fake', 'goosebumps', 'supportive',
                    'not_funny',
                    'fml', 'not_scary', 'rage', 'mixed']
        emo_df = pd.DataFrame(0, columns=emotions, index=range(len(api_result_df)))

        for i in api_result_df.index:
            all_emotions = api_result_df.loc[i, "canvsMetrics.emotionsDrilldownCount"]

            for emo in all_emotions:
                field = list(emo.keys())[0]
                value = list(emo.values())[0]
                if field in emotions:
                    emo_df.loc[i, field] = value
                else:
                    emo_df.loc[i, 'mixed'] += value

        complete_df = pd.concat([api_result_df.drop(['canvsMetrics.emotionsDrilldownCount'], axis=1), emo_df], axis=1)

        # Format name of csv
        outname = 'social_fb_posts_' + fb_id + '_' + start_date + '_' + end_date + '.csv'

        outname = outname.replace('/', '.')

        outdir = os.path.abspath('api_exports/social')

        if not os.path.exists(outdir):
            os.makedirs(outdir)

        fullname = os.path.join(outdir, outname)

        # print page results to csv
        complete_df.to_csv(fullname, index=False)

        print('Successfully created {} file.'.format(fullname))

    return complete_df

# Send a list of page IDs and query all pages for the time range
def get_page_collection(api_key, org_id, start_date, end_date, fb_pages, query_increment=None):
    """
    :param api_key:
    :param org_id:
    :param start_date:
    :param end_date:
    :param fb_pages: (list) list of fb page IDs
    :param query_increment:
    :return:
    """
    final_result = pd.DataFrame()

    for i in fb_pages:

        try:
            # Pull pages one by one
            result = get_facebook_posts(api_key=api_key, fb_id=i, org_id=org_id,
                                        start_date=start_date, end_date=end_date, query_increment=query_increment)
        except Exception as e:
            print('A page could not be loaded {} raised {}'.format(i, e))
            # print('A page could not be loaded {} raised {}'.format(i, e))

        # Print each page's result to a new file

        # Format name of csv
        outname = 'social_fb_posts_' + i + '_' + start_date + '_' + end_date + '.csv'

        outname = outname.replace('/', '.')

        outdir = os.path.abspath('api_exports/social')

        if not os.path.exists(outdir):
            os.makedirs(outdir)

        fullname = os.path.join(outdir, outname)

        # print page results to csv
        result.to_csv(fullname, index=False)

        print('Successfully created {} file.'.format(outname))

        # Append values to master file
        final_result = final_result.append(result, sort=False)

    return final_result
