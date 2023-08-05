from canvs_toolbox.general import consolidate_data
import pandas as pd
import itertools
from scipy.spatial.distance import euclidean, pdist, squareform
import os

def audience_overlap_analysis(directory):
    df = consolidate_data(directory, file_type='csv')

    # Use file name to designate show name
    df['series_name'] = df['file_name'].apply(lambda x: os.path.basename(os.path.normpath(x))).str.replace('.csv', '')
    df.drop(columns='file_name', inplace=True)

    # Create Unique list of shows for analysis
    series_list = list(set(df['series_name']))

    # Logic to filter down to only unique users per show. Filters out dupes if added.
    master_df = pd.DataFrame()

    for i in range(len(series_list)):
        series_counter = i
        current_series = series_list[i]
        series_df = df.loc[df['series_name'] == current_series]
        filtered_df = pd.DataFrame(series_df['users'].unique())
        filtered_df['series_name'] = current_series

        master_df = master_df.append(filtered_df)

    master_df.rename(columns={0: 'users'}, inplace=True)

    audience_overlap = pd.DataFrame({'comparison': [], 'overlapping_authors': [], 'unique_authors': []})

    # Create list of all possible iterations across all possible unique shows.
    for i in range(len(series_list)):
        r = i + 1
        list_logic = list(itertools.combinations(series_list, r))

        for counter, value in enumerate(list_logic):
            compset_df = master_df.loc[master_df['series_name'].isin(list_logic[counter])]

            df_counts = compset_df['users'].value_counts()

            dupe_authors = len(df_counts[df_counts == r])
            unique_authors = len(list(set(compset_df['users'])))
            comparison = str(list_logic[counter])
            audience_overlap = audience_overlap.append({'comparison': comparison, \
                                                        'overlapping_authors': dupe_authors, \
                                                        'unique_authors': unique_authors}, ignore_index=True)

    audience_overlap['percent_overlap'] = audience_overlap.overlapping_authors / audience_overlap.unique_authors

    csv_name = 'tv_audience_overlap_' + os.path.basename(os.path.normpath(directory)) + '.csv'
    csv_name = csv_name.replace('/', '.')

    outdir = 'analytics_exports/tv'
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    fullname = os.path.join(outdir, csv_name)

    audience_overlap.to_csv(fullname, index=False)

def audience_erosion_analysis(filename):
    df = pd.read_csv(filename)

    # count the number of unique episodes in a season

    episode_list = list(set(df['episode']))
    episode_counter = list(set(df['episode']))

    # perform audience loss over season episode by episode. Note, season is not taken into account. Only episodes

    data_cols = ['users', 'season', 'episode']
    data_list = []
    for episode in episode_list:
        data_list.append(df.loc[df['episode'].isin(episode_counter)].nunique())
        del episode_counter[0]

    # build dataframe with audience loss data by episode. Episode numbers are in reverse order at this point in code

    audience_erosion = pd.DataFrame(data_list, columns=data_cols)

    # Reverse episode numbers to reflect audience behaviors. Renames to number of episodes active

    audience_erosion['episodes active'] = audience_erosion['episode'].iloc[::-1].reset_index(drop=True)
    audience_erosion.drop(['episode'], axis=1, inplace=True)

    # Run share of total audience lost per episode calculation
    max_audience = audience_erosion['users'].max()
    audience_erosion['% of total audience'] = audience_erosion['users'].divide(max_audience)

    # Reorder colums before writing to csv
    reordered_cols = ['season', 'episodes active', 'users', '% of total audience']
    audience_erosion = audience_erosion[reordered_cols]

    csv_name = 'tv_audience_erosion_' + os.path.basename(os.path.normpath(filename))
    csv_name = csv_name.replace('/', '.')

    outdir = 'analytics_exports/tv'
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    fullname = os.path.join(outdir, csv_name)

    audience_erosion.to_csv(fullname, index=False)

def similarity_func(u, v):
    return 1/(1+euclidean(u,v))

#source = direct or api
def emotional_fingerprinting_analysis(filename, format):
    if filename.split(".", 1)[1] == "csv":
        df = pd.read_csv(filename)
    elif filename.split(".", 1)[1] == "xlsx":
        df = pd.read_excel(filename, sheet_name='Programs')

        newNames = {}

        def rename(x):
            newNames[x] = str(x)[:-7].lower().replace(' ', '_')

        x = list(map(rename, list(df.columns[13:56])))
        df.rename(columns=newNames, inplace=True)
        df = df[1:]
    else:
        print("invalid source type -- please set to either 'direct' or 'api'")

    emotionCols = ['love', 'crazy', 'enjoy', 'excited', 'funny', 'hate', 'beautiful', 'happy', 'congrats', 'afraid',
                   'dislike',
                   'sad', 'angry', 'annoying', 'disappointed', 'boring', 'cried', 'unsure', 'idiot', 'awkward',
                   'brilliant',
                   'brutal', 'weird', 'interesting', 'ugly', 'badass', 'looks_good', 'sentimental', 'nervous',
                   'disgusting',
                   'jealous', 'lucky', 'worried', 'thrilling', 'embarrassing', 'fake', 'goosebumps', 'supportive',
                   'not_funny',
                   'fml', 'not_scary', 'rage', 'mixed']

    if 'pagename' in df.columns:
        nameCol = ['pagename']
    elif 'programtitle' in df.columns:
        nameCol = ['programtitle']
    elif 'postMetadata.postMessage' in df.columns:
        nameCol = ['postMetadata.postMessage']
    else:
        nameCol = ['Program Title']

    DF_var = df[emotionCols + nameCol].set_index(nameCol)

    # Runs Euclidian function
    dists = pdist(DF_var, similarity_func)

    # Creates similarity matrix
    DF_euclid = pd.DataFrame(squareform(dists), columns=DF_var.index, index=DF_var.index)

    outdir = 'analytics_exports/tv'
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    if format == 'stacked':
        euclid_stacked = DF_euclid.stack()

        euclid_stacked = pd.DataFrame(euclid_stacked, columns=['value'])
        euclid_stacked.index.names = ['asset', 'comparison']

        DF_euclid = euclid_stacked
        csv_name = 'emotional_fingerprint_stacked_' + os.path.basename(os.path.normpath(filename)) + '.csv'
    elif format == 'matrix':
        csv_name = 'emotional_fingerprint_matrix_' + os.path.basename(os.path.normpath(filename)) + '.csv'
    else:
        print("invalid format type -- please set to either 'stacked' or 'matrix'")

    csv_name = csv_name.replace('/', '.')
    fullname = os.path.join(outdir, csv_name)
    DF_euclid.to_csv(fullname, index=True)






