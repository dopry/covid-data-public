"""
Updates all relevant files in the repo.
"""
from urllib.request import urlopen
import tempfile
import os
from zipfile import ZipFile

_JHU_MASTER = r'https://github.com/CSSEGISandData/COVID-19/archive/master.zip'
_DF = r'http://www.bay12games.com/dwarves/df_47_04_win.zip'


def download_zip_and_unpack_to_dir(dir, zip_url):
    with open(os.path.join(dir, 'temp.zip'), 'wb') as zip:
        zip.write(urlopen(zip_url).read())
    with ZipFile(os.path.join(dir, 'temp.zip')) as zf:
        zf.extractall(path=os.path.join(dir))
    return dir


new_temp_dir = tempfile.TemporaryDirectory()
print(new_temp_dir.name)
d = download_zip_and_unpack_to_dir(new_temp_dir.name, _JHU_MASTER)
daily_reports_dir = os.path.join(new_temp_dir.name, 'COVID-19-master', 'csse_covid_19_data', 'csse_covid_19_daily_reports')
print(daily_reports_dir)
print(d)