import os
import sys
from urllib.request import urlopen
import urllib.request
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import Logger
from utils.helpers import get_directory_name

absolute_path = 'Developing_and_Deploying_a_Predictive_Analytics_Platform_Using_FastAPI_Streamlit_and_Docker/empirical/src/staging_raw_data.py'
logger_name = get_directory_name(absolute_path)

inspector_gadget = Logger(logger_name)

url = "https://raw.githubusercontent.com/furkankizilay/car-price-prediction/main/cars.csv"
 

dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
target_dir = os.path.join(dir, 'data', 'raw')
fetch_dir = f'{target_dir}/cars.csv'

def download_data_from_url(url, target_dir):
    if not os.path.exists(str(target_dir)):
        os.makedirs(str(target_dir))
    
    try:
        urllib.request.urlretrieve(url, fetch_dir)
        inspector_gadget.get_log().info(f'data downloaded successfully to {target_dir}')

    except Exception as e:
        inspector_gadget.get_log().error(f'error downloading data due {e}')
        traceback.print_exc()




def main():
    download_data_from_url(url, target_dir)





if __name__ == '__main__':
    main()

    
