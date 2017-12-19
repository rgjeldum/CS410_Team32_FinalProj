# GitHub
# https://github.com/Vaslo/CS410_Team32_FinalProj

# Use this file for downloading and extracting Management's Discussion and Analysis
# sections from Form 10-Q and Form 10-K raw text filings found using the EDGAR service.

from bs4 import BeautifulSoup
import sys
import re
import csv
import pickle


try:
    # For Python 3.0 and later
    from urllib.request import urlopen
    from urllib.error import HTTPError
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
    from urllib2 import HTTPError


''' EDGAR_filing class creates an object that holds all the filing data.
    Attempts to grab raw filing data from EDGAR site then passes through
    BeautifulSoup in order to isolate the MD&A section. MD&A section stored
    in class variable.'''


class EDGAR_filing:
    filing_raw_text = None
    filing_clean_text = None
    filing_mda_text = None
    sic = 'NONE'
    accession = 'NONE'
    success = False
    
    # Constructor
    def __init__(self, filing_tuple):
        (self.cik,
        self.company_name,
        self.form_type,
        self.filing_date,
        self.filing_url) = filing_tuple
        self.filing_url = self.filing_url
        self.get_filing_raw_text()
        self.find_sic()
        self.find_accession()
        self.find_mda_text()
        self.dump_raw_filing_text() # entire filing, HTML and all
        self.dump_clean_filing_text() # text after cleaned by Beautiful Soup
        self.dump_mda_text() # just the MD&A section, stopwords removed
        self.flush_raw_text() # removes raw text from object for use if pickling


    # Provides quick summary of each EDGAR_filing object
    def get_filing_summary(self):

        f_data = "{}    {}  {}  {}  {}".format(
        self.cik, self.company_name, 
        self.form_type, self.filing_date, self.filing_url)
        return f_data


    # Downloads text from SEC site
    def get_filing_raw_text(self):

        print('Downloading raw filing text')
        try:
            results = urlopen(url_stem + self.filing_url)
            self.filing_raw_text = results.read()
        except HTTPError:
            print('\tFAILED. Skipping.')
            self.filing_raw_text = ''


    # Attempts to find MD&A text
    def find_mda_text(self):

        print('Searching for MD&A text'),

        try:
            text = BeautifulSoup(self.filing_raw_text, 'html.parser')
            text = re.sub(r'[^\x00-\x7F]+|\W{2,}', ' ', text.document.get_text())
            self.filing_clean_text = text
        except:
            text = ''

        mda_start = 0
        found = True
        success = False

        # Look for the start of MD&A text
        while found is True:
            mda_start = re.search(r'item[\s\w\&\.\;\,\:]*management[\s\']*s discussion and analysis', text, re.I | re.M)
            if mda_start:
                print('\tTrimming M&DA START to {}.'.format(mda_start.start()))
                # Trim string to latest occurrence of MD&A section
                text = text[mda_start.end():]
                self.success = True
            else:
                found = False

        # Look for end of MD&A text by attempting to find the next section
        if self.success:
            mda_end = re.search(r'item[\s\w\&\.\;\,\:]*quantitative and qualitative', text, re.I | re.M)
            if mda_end:
                print('\tTrimming MD&A END to {}.'.format(mda_end.start()))
                # Remove any text below the end of the MD&A section
                text = text[:mda_end.start()]
            print('\tSuccess!')
        else:
            # if there is no MD&A, use the cleaned filing text instead
            text = str(self.filing_clean_text)
            print('\tNone found.')

        text = remove_stopwords_list(text.split())
        self.filing_mda_text = ' '.join(text)


    # Save MD&A text to file
    def dump_mda_text(self):

        if len(self.filing_mda_text) > 0:

            if self.success:
                fname = mda_dir + "mda_{}_{}_{}_{}.txt".format(self.sic, self.filing_date, self.cik,
                                                                        self.accession)
            else:
                fname = mda_dir + "NO_mda_{}_{}_{}_{}.txt".format(self.sic, self.filing_date, self.cik,
                                                                        self.accession)

            try:
                f = open(fname, 'w')
                f.write(self.filing_mda_text)
                f.close()
                print('Saving MD&A text to {}'.format(fname)),
            except IOError:
                print('Unable to write MD&A text to file.')
                exit(1)
        else:
            print('\tNo MD&A found. Skipping.')


    # Save cleaned filing text to file
    def dump_clean_filing_text(self):

        if self.filing_clean_text:

            fname = filing_dir + "filing_{}_{}_{}_{}.txt".format(self.sic, self.filing_date, self.cik,
                                                                        self.accession)

            try:
                f = open(fname, 'w')
                f.write(self.filing_clean_text)
                f.close()
                print('Saving cleaned filing text to {}'.format(fname)),
            except IOError:
                print('Unable to write cleaned filing text to file.')
                exit(1)
        else:
            print('\tNo cleaned filing text found. Skipping.')


    # Save raw filing text to file
    def dump_raw_filing_text(self):

        if self.filing_raw_text:

            fname = raw_dir + "raw_{}_{}_{}_{}.txt".format(self.sic, self.filing_date, self.cik,
                                                                        self.accession)

            try:
                f = open(fname, 'wb')
                f.write(self.filing_raw_text)
                f.close()
                print('Saving raw filing text to {}'.format(fname)),
            except IOError:
                print('Unable to write raw filing text to file.')
                exit(1)
        else:
            print('\tNo cleaned raw text found. Skipping.')


    # Locate Standard Industrial Classification code in the raw filing text
    def find_sic(self):

        print('Searching for SIC code'),
        for line in str(self.filing_raw_text).split('\n'):
            if line.find('STANDARD INDUSTRIAL CLASSIFICATION') > 0:
                m = re.search('\[\d*\]', line)
                if m:
                    self.sic = m.group(0).strip('[]')
                    print('\tFound {}'.format(self.sic))
                else:
                    print('\tMISSING!')


    # Locate the unique identifier for each EDGAR filing -- accession number
    def find_accession(self):

        print('Searching for Accession Number... '),
        p = self.filing_url.split('/')
        self.accession = p[3].split('.')[0].replace('-', '')
        print('\tFound {}'.format(self.accession))


    # Purging raw filing text variable to reduce object size
    def flush_raw_text(self):

        self.filing_raw_text = None

# Iterate through each word and remove if it is a stopword
def remove_stopwords_list(word_list):

    print('Removing stopwords and garbage.'),

    filtered_word_list = []
    global stopwords

    for word in word_list:
        foo = re.sub(r'[\d\,\(\)\.\$\'\_]', '', word.lower())
        if foo[-2:].lower() == 'ed':
            continue
        if len(foo) > 1 and foo not in stopwords:
            filtered_word_list.append(foo)

    return filtered_word_list


''' Open index and iterate through each line
    Creates a list of tuples. Each tuple has the filing data from each line
    Create new EDGAR_filing object for each line and populate with tuple
    Outputs the list of EDGAR_filing objects'''


def load_index(idx_name, cik_list=None, max_count=None):
    filing_list = [] # index of tuples
    filing_items = () # tuple of filing items (cik, url, etc.)
    c = 1 # count of filings retrieved
    ciks = None
    global stopwords

    # Load CIK mask file
    if cik_list:
        try:
            with open(cik_list) as f:
                ciks = f.readlines()
            ciks = [x.strip() for x in ciks]
        except IOError:
            print('ERROR opening CIK list {}'.format(cik_list))

    # Read in stopwords
    try:
        with open(stopwords_file, 'r') as f:
            stopwords = f.readlines()
        stopwords = [x.strip() for x in stopwords]
        print('Loading {} stopwords.'.format(len(stopwords)))
    except IOError:
        print('Error opening stopwords file.')

    # Open index file, treating like a CSV file that is pipe delimited
    # Limit to max_count number of filings to download, parse and analyze
    try:
        with open(idx_name, 'r') as csv_file:
            filing_reader = csv.reader(csv_file, delimiter="|")
            for row in filing_reader:
                if ciks:
                    if row[0] not in ciks:
                        continue
                if (max_count is not None and c <= max_count) or max_count is None:
                    for item in row:
                        filing_items += (item, )
                    print('-'*64)
                    print('{}. Processing {}'.format(c, filing_items))
                    temp_filing = EDGAR_filing(filing_items) # Create class object
                    filing_list.append(temp_filing)
                    filing_items = () # reset tuple
                else:
                    return filing_list
                c += 1
        return filing_list
    except IOError:
        print('ERROR opening index {}'.format(idx_name))
        exit()


if __name__ == '__main__':

    # Set data file directories
    filing_dir = 'data/'
    mda_dir = 'data/'
    raw_dir = 'data/'
    stopwords_file = 'stopwords.txt'

    filings_max_count = None
    cik_list_filename = None

    # Syntax: python build_edgar_mda_files.py <index_filename> [cik_maskfile] [max_count]

    if len(sys.argv) < 2:
        print("Usage: {} <IndexFilename> [cik_maskfile] [max_count]".format(sys.argv[0]))
        sys.exit(1)
        
    if (len(sys.argv) > 2):
        cik_list_filename = sys.argv[2]

    # Check to see if a max_count was provided from the command line. Set 100 as default just in case.
    if (len(sys.argv) > 3):
        filings_max_count = int(sys.argv[3])

    index_fname = sys.argv[1]
    url_stem = 'http://www.sec.gov/Archives/'
    stopwords = []

    # Grab all EDGAR filings listed in index, up to max_count if specified
    print('Loading index {}.'.format(index_fname))
    edgar_filings = load_index(index_fname, cik_list_filename, filings_max_count)
    print('='*64)
    print('Done. {} filing(s) loaded.'.format(len(edgar_filings)))

    # Remove comment below to dump all EDGAR_Filing class objects to disc
    # pickle.dump(edgar_filings, open('data/EDGAR_Filings.objects', 'wb'), protocol=2)

    # Remove comment below to load EDGAR_Filing class objects file
    # edgar_filings = pickle.load(open('EDGAR_Filings.objects','r'))
