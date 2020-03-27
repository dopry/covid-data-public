"""
Updates all relevant files in the repo.
"""
import os
import shutil
import tempfile
from zipfile import ZipFile
from urllib.request import urlopen


class CovidDatasetAutoUpdater:
    """Provides all functionality to auto-update the datasets in the data repository"""
    _JHU_MASTER = r'https://github.com/CSSEGISandData/COVID-19/archive/master.zip'
    _CDS_TIMESERIES = r'https://coronadatascraper.com/timeseries.csv'

    @staticmethod
    def download_zip_and_unpack_to_dir(zip_url, _dir):
        with open(os.path.join(_dir, 'temp.zip'), 'wb') as zip:
            zip.write(urlopen(zip_url).read())
        with ZipFile(os.path.join(_dir, 'temp.zip')) as zf:
            zf.extractall(path=os.path.join(_dir))
        return _dir

    def update_jhu_data(self):
        new_temp_dir = tempfile.TemporaryDirectory()
        self.download_zip_and_unpack_to_dir(self._JHU_MASTER, new_temp_dir.name)
        jhu_repo_daily_reports_dir = os.path.join(new_temp_dir.name, 'COVID-19-master', 'csse_covid_19_data', 'csse_covid_19_daily_reports')
        local_daily_reports_dir = os.path.join('data', 'cases-jhu', 'csse_covid_19_daily_reports')
        # Copy the daily reports into the local directory
        for f in os.listdir(jhu_repo_daily_reports_dir):
            shutil.copyfile(
                os.path.join(jhu_repo_daily_reports_dir, f),
                os.path.join(local_daily_reports_dir, f)
            )

    def update_cds_data(self):
        with open(os.path.join('data', 'cases-cds', 'timeseries.csv'), 'wb') as out:
            res = urlopen(self._CDS_TIMESERIES)
            out.write(res.read())

    def update_all_data_files(self):
        self.update_cds_data()
        self.update_jhu_data()


CovidDatasetAutoUpdater().update_all_data_files()
