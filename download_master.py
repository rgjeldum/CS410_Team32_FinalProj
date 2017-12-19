# GitHub
# https://github.com/Vaslo/CS410_Team32_FinalProj

# Use for downloading master index files for given year(s) from EDGAR system


import shutil
import sys

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
    from urllib.error import HTTPError
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
    from urllib2 import HTTPError


def download_master(start_year, end_year, dir_stem, URLstem):
    for year in range(start_year, end_year+1):
        for qtr in range(1, 5):
            currURL = URLstem + str(year) + '/QTR' + str(qtr) + '/master.idx'
            local_file = dir_stem + str(year) + 'QTR' + str(qtr) + '.idx'
            print('Downloading ' + str(year) + ' Q' + str(qtr) + ' master index.')

            try:
                response = urlopen(currURL)
                out_file = open(local_file, 'wb')
                shutil.copyfileobj(response, out_file)
                out_file.close()
            except HTTPError:
                print('URL not found.')


# __MAIN__

if __name__ == '__main__':

    # Set the directory where to save master indexes
    dir_stem = 'data/'

    # python download_master.py <start_year> <end_year>

    if len(sys.argv) < 3:
        print("Usage: {} <start_year> <end_year>".format(sys.argv[0]))
        sys.exit(1)

    start_year = int(sys.argv[1])
    end_year = int(sys.argv[2])

    if start_year > end_year:
        print('ERROR: <start_year> must be before <end_year>')
        sys.exit(1)

    URLstem = 'https://www.sec.gov/Archives/edgar/full-index/'

    # Download Form 10-K and 10-Q documents from SEC for given years
    download_master(start_year, end_year, dir_stem, URLstem)
