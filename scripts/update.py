"""
Updates all relevant files in the repo.
"""
import datetime
import json
import logging
import os
import shutil
import tempfile
from zipfile import ZipFile
from urllib.request import urlopen
import pandas as pd
import argparse

logger = logging.Logger('data update logger')

parser = argparse.ArgumentParser()
parser.add_argument('-cds', '--cds', help='Update data from the Corona Data Scraper', action='store_true')
parser.add_argument('-jhu', '--jhu', help='Update data from John Hopkins University', action='store_true')
args = parser.parse_args()


class CovidDatasetAutoUpdater:
    """Provides all functionality to auto-update the datasets in the data repository"""
    _JHU_MASTER = r'https://github.com/CSSEGISandData/COVID-19/archive/master.zip'
    _JHU_MASTER_API = r'https://api.github.com/repos/CSSEGISandData/COVID-19/branches/master'
    _JHU_DATA_DIR = os.path.join('data', 'cases-jhu', 'csse_covid_19_daily_reports')

    _CDS_TIMESERIES = r'https://coronadatascraper.com/timeseries.csv'
    _CDS_DATA_DIR = os.path.join('data', 'cases-cds')

    @staticmethod
    def _stamp():
        #  String of the current date and time.
        #  So that we're consistent about how we mark these
        return datetime.datetime.now().strftime('%A %b %d %I:%M:%S %p')

    def clone_repo_to_dir(self, url, _dir):
        with open(os.path.join(_dir, 'temp.zip'), 'wb') as zip:
            zip.write(urlopen(url).read())
        with ZipFile(os.path.join(_dir, 'temp.zip')) as zf:
            zf.extractall(path=os.path.join(_dir))
        return _dir

    def update_jhu_data(self):
        new_temp_dir = tempfile.TemporaryDirectory()
        self.clone_repo_to_dir(self._JHU_MASTER, new_temp_dir.name)
        repo_dir = os.path.join(new_temp_dir.name, 'COVID-19-master')
        jhu_repo_daily_reports_dir = os.path.join(repo_dir, 'csse_covid_19_data', 'csse_covid_19_daily_reports')
        # Copy the daily reports into the local directory
        for f in os.listdir(jhu_repo_daily_reports_dir):
            shutil.copyfile(
                os.path.join(jhu_repo_daily_reports_dir, f),
                os.path.join(self._JHU_DATA_DIR, f)
            )
        with open(os.path.join(self._JHU_DATA_DIR, 'version.txt'), 'w') as log:
            log.write('{}\n'.format(json.loads(urlopen(self._JHU_MASTER_API).read())['commit']['sha']))
            log.write('Updated on {}'.format(self._stamp()))

    def update_cds_data(self):
        pd.read_csv(self._CDS_TIMESERIES).to_csv(os.path.join(self._CDS_DATA_DIR, 'timeseries.csv'), index=False)
        # Record the date and time of update in versions.txt
        with open(os.path.join(self._CDS_DATA_DIR, 'version.txt'), 'w') as log:
            log.write('Updated on {}'.format(self._stamp()))

    def update_all_data_files(self):
        self.update_cds_data()
        self.update_jhu_data()

if __name__ == '__main__':
    update = CovidDatasetAutoUpdater()
    something_specified = False

    if args.cds:
        logger.info('Updating data from the Corona Data Scraper')
        update.update_cds_data()
        something_specified = True

    if args.jhu:
        logger.info('Updating data from John Hopkins University')
        update.update_jhu_data()
        something_specified = True

    if not something_specified:
        #  If nothing was specified, then we assume that the user wants all datasets updated
        logger.info('Updating all data sources')
        update.update_all_data_files()
