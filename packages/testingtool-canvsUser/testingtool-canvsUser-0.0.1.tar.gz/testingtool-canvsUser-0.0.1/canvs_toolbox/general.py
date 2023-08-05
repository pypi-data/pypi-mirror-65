import pandas as pd
import glob
import os
import logging

# Internal imports
# from utilities import logging_setup
#
# # initialize logging setup
# logging_setup()
#
log = logging.getLogger(__name__)


# Create a single data file from similar type files (csv or xlsx)
def consolidate_data(file_path, file_type='csv'):
    """
    :param file_path: path to a directory of similar type and similarly structured files
    :param file_type: (str) currently only supports csv
    :return: A df of all data from files in file path of designated file type
    """

    if file_type == 'csv':
        print('csv mode enabled')

    else:
        raise Exception

    files = glob.glob(os.path.join(os.path.abspath(file_path), '*.' + file_type))  # Get filepaths of all files

    print('combining {} files'.format(len(files)))

    df = pd.DataFrame()

    counter = 1

    for file_ in files:
        # TODO implement excel support when making into larger project
        file_df = pd.read_csv(file_, dtype='str')

        log.debug('loaded file {} of {}'.format(counter, len(files)))

        file_df['file_name'] = file_

        df = df.append(file_df, sort=True)

        counter = counter + 1

    df = df.reset_index(drop=True)

    print('completed building dataframe!')

    return df