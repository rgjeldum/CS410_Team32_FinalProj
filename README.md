
# Discovering Industry Trends in SEC Filings Using Topic Analysis 

The goal of this project was to use statistical methods to help discover noticeable industry trends in SEC filings. Using certain sections of quarterly and annual filings made by companies in specific industries, one may be able to gain insight into which topics are the most prevelent over the course of several years. Groups of companies were picked based on their Standard Industrial Classification ([SIC](https://en.wikipedia.org/wiki/Standard_Industrial_Classification)) code. This project focused on computer-related services (SIC 7370-7374).

### A Brief Overview of the EDGAR Service

The Electronic Data Gathering, Analysis, and Retrieval system ([EDGAR](https://www.sec.gov/oiea/Article/edgarguide.html)) managed by the U.S. Securities and Exchange Commission (SEC) is a repository for vast amounts of public disclosure data regarding certain parties, typically companies, individuals with substantial equity holdings and mutual funds (“filers” hereafter). The SEC requires these disclosures in the form of "filings" in order to ensure that investors are sufficiently informed before making investment decisions. Filings must be organized according to specific form documents which are governed by SEC rules and regulations. For example, each publically traded company is required to file a Form 10-Q and Form 10-K on a quarterly and annual basis respectively, outlining the financial performance and other key indicators during that period.

### Accessing EDGAR Data

There are two primary methods for retrieving large amounts of EDGAR data:

- Compressed files containing every public filing for a given day
- Quarterly CSV index files containing basic data for each filing and a URL to the actual document

Because the former method requires up to 2GB of disk space for each day, this project uses the index method to download and extract individual filings as needed.

Below is an example of a CSV index file:

```
CIK|Company Name|Form Type|Date Filed|Filename
--------------------------------------------------------------------------------
1000180|SANDISK CORP|10-K|2009-02-25|edgar/data/1000180/0001000180-09-000011.txt
1001039|WALT DISNEY CO/|10-Q|2009-02-03|edgar/data/1001039/0001193125-09-017678.txt
1652044|Alphabet Inc.|10-Q|2016-08-04|edgar/data/1652044/0001652044-16-000032.txt
320193|APPLE INC|10-Q|2017-08-02|edgar/data/320193/0000320193-17-000009.txt
```

CIK numbers are unique identifiers assigned to each company making a public filing. Also included in each line is the Form Type and URL to the filing document. We will focus on Form 10-Q and 10-K respectively. All publically traded companies are required to file these documents. 

### Focus Area

In each quarterly and annual filing, the SEC requires a section entitled "_Management’s Discussion and Analysis of Financial Condition and Results of Operations_" (MD&A). This section typically includes a description of the company's products, services and growth plans, making it a good target for learning more about the trajectory of an industry. This project parses each filing in an attempt to locate the start and end points of this section and feed it into our topic modeling libraries.

### Project Code Files

The following are the primary Python files for downloading EDGAR data and parsing it into a bag of words representation:

1. ```download_master.py``` - Downloads master index files for a given range of years. Make sure to set start and end year.

2. ```extract_10x_from_master.py``` - Extracts quarterly and annual filings (Form 10-Q and Form 10-K respectively) from the master index files for a given range of years, then builds a combined index into one file.

3. ```build_edgar_mda_files.py``` -  Iterates through the combined index from above, downloads the raw text filing, strips HTML tags and other garbage then dumps a file containing the MD&A text.

> **Note:**
>
> This project assumes the user has Python 3.6, although Python 2.7 can likely be used as well.

### Setup

This project uses [Gensim](https://radimrehurek.com/gensim/), a topic modelling library, and [pyLDAvis](https://github.com/bmabey/pyLDAvis) for visualizations. If you have not installed these two packages, use the following commands to get started.

```
# Make sure pip is up to date
pip install --upgrade pip

# Install Gensim and pyLDAvis
pip install gensim pyLDAvis
```

### Tutorials

- [Downloading and Extracting MD&A Text](Downloading_and_Extracting_MDA_Text.ipynb)
- [Topic Modeling and Visualizations Using Latent Dirichlet Allocation](Visualizations.ipynb)
