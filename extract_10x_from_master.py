# GitHub
# https://github.com/Vaslo/CS410_Team32_FinalProj

# Use this file for extracting Form 10-K and 10-Q line items from EDGAR master index files

import io
import sys


def extract10x(index_file_handle, output_file_handle):
    count10x = 0
    for line in index_file_handle:
        if line.find('.txt') > 0:
            items = line.split('|')
            # if items[2] in ('10-Q', '10-K'):
            if items[2] == '10-Q':
                output_file_handle.write(line)
                count10x += 1
    return count10x


if __name__ == '__main__':

    # Set the directory where the master indexes are saved
    dir_prefix = 'data/'

    # python extract_10x_from_master.py <start_year> <end_year>

    if len(sys.argv) < 3:
        print("Usage: {} <start_year> <end_year>".format(sys.argv[0]))
        sys.exit(1)

    start_year = int(sys.argv[1])
    end_year = int(sys.argv[2])

    if start_year > end_year:
        print('ERROR: <start_year> must be before <end_year>')
        sys.exit(1)

    result_index = dir_prefix + '10X-' + str(start_year) + '-' + str(end_year) + '.idx'

    print('Extracting filing data:')

    # Open file for appending list of 10X rows
    try:
        f_out = open(result_index, 'w')
    except IOError:
        print('Error opening file {}. Exiting.'.format(result_index))

    # Iterate over each year
    for year in range(start_year, end_year+1):

        # Iterate over each quarter
        for qtr in range(1, 5):

            master_index_file_name = dir_prefix + str(year) + 'QTR' + str(qtr) + '.idx'

            # Check whether there's a master index for a particular year/qtr. Skip if not.
            try:
                with io.open(master_index_file_name, 'r', encoding='latin-1') as f_in:
                    print('    ' + str(year) + ' Q' + str(qtr) + '... Found ' + str(extract10x(f_in, f_out)) + ' filings')
            except IOError:
                print('    No data for ' + str(year) + ' Q' + str(qtr) + '. Skipping.')
                continue

    print('Saving to {}'.format(result_index))

    f_out.close()
