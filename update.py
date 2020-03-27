"""
Updates all relevant files in the repo.
"""
from urllib.request import urlopen
import tempfile
import os
import shutil
from zipfile import ZipFile

_JHU_MASTER = r'https://github.com/CSSEGISandData/COVID-19/archive/master.zip'
_CDS_TIMESERIES = r'https://coronadatascraper.com/timeseries.csv'
_DF = r'http://www.bay12games.com/dwarves/df_47_04_win.zip'


def download_zip_and_unpack_to_dir(zip_url, _dir):
    with open(os.path.join(_dir, 'temp.zip'), 'wb') as zip:
        zip.write(urlopen(zip_url).read())
    with ZipFile(os.path.join(_dir, 'temp.zip')) as zf:
        zf.extractall(path=os.path.join(_dir))
    return _dir

def update_jhu_data():
    new_temp_dir = tempfile.TemporaryDirectory()
    download_zip_and_unpack_to_dir(_JHU_MASTER, new_temp_dir.name)
    jhu_repo_daily_reports_dir = os.path.join(new_temp_dir.name, 'COVID-19-master', 'csse_covid_19_data', 'csse_covid_19_daily_reports')
    local_daily_reports_dir = os.path.join('data', 'cases-jhu', 'csse_covid_19_daily_reports')
    # Copy the daily reports into the local directory
    for f in os.listdir(jhu_repo_daily_reports_dir):
        shutil.copyfile(
            os.path.join(jhu_repo_daily_reports_dir, f),
            os.path.join(local_daily_reports_dir, f)
        )

def update_cds_data():
    with open(os.path.join('data', 'cases-cds', 'timeseries.csv'), 'wb') as out:
        res = urlopen(_CDS_TIMESERIES)
        out.write(res.read())

update_cds_data()
