import os
import sys
import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.logger import Logger
from utils.helpers import get_directory_name
from src.iv_create_web_interface_streamlit import run

absolute_path = 'Developing_and_Deploying_a_Predictive_Analytics_Platform_Using_FastAPI_Streamlit_and_Docker/empirical/src/iii_create_API.py'
inspector_gadget = get_directory_name(absolute_path)
inspector_gadget = Logger(inspector_gadget)

def initialize_app(title:str, version:str, description:str):
    '''
    Initialize the model. This will be loaded at the start of FastAPI model server.

    Parameters:
    :title: Application title.
    :version: Application version (should be a string).
    :description: Application description.

    Returns:
    FastAPI application instance.

    '''
    app = FastAPI(title= f'{title}', version= f'{version}', description= f'{description}')
    return app


#initialize FastAPI object in order to utilize "@app" decorators below
app = initialize_app(title="Car Price Prediction", version="1.0", description="Linear Regression model is used for predictive analytics.")


def load_model(file_path: str, mmap_mode:str):
    """
    Load a model from a specified file path. This function call uses joblib to deserialize and load the model stored in the '.pkl' file.
    located at a specific directory on your system. This file is expected to be a saved model, likely serialized using 'joblib'.

    Parameters:
    :file_path: The path to the file containing the serialized model.
    :mmap_mode: Specifies how the file should be loaded into memory, particularly useful for large datasets or models. Here are the options:
        None: This is the default and will load the file into memory normally.
        'r': Opens the file in read-only mode. This is useful when you don't need to modify the data and want to avoid loading the entire file into memory.
        'r+': Opens the file in read-write mode without loading it entirely into memory. Changes can be made to the data, but they'll be written back to the file.
        'w+': Opens the file in read-write mode but truncates the file to zero length. It's generally not used unless you're rewriting the file.
        'c': Opens the file in copy-on-write mode. Modifications to the data are not written back to the original file but to a copy in memory.

    :model: The result of 'joblib.load' is assigned to the var 'model'. This variable now holds the deserialized model object that was saved previously.

    Returns:
    :model: The deserialized model object.
    """
    if not os.path.isfile(file_path):
        inspector_gadget.get_log().error(f"load_model() unsuccessful. The file at {file_path} does not exist.")
        raise FileNotFoundError(f"The file at {file_path} does not exist.")
        
    model = joblib.load(file_path)
    return model


#call load_modle to input it in 'predict' function
file_path = '/Users/ericklopez/Desktop/Developing_and_Deploying_a_Predictive_Analytics_Platform_Using_FastAPI_Streamlit_and_Docker/empirical/data/final/LinearRegressionModel.pkl'
model = load_model(file_path, 'r')


class Data(BaseModel):
    name:str
    automaker:str
    year:int
    miles_driven:int
    fuel_type:str


@app.get('/') #These decorators are used to register route handlers with the FastAPI application instance
@app.get('/home') #FastAPI, the @app decorators are used to define routes, and they need to be applied to an instance of the FastAPI app
def read_home() -> dict:
    '''
    Home endpoint which can be used to test the availability of the    application.
    
    '''
    return {'message': 'System is healthy'}


@app.post("/predict") #These decorators are used to register route handlers with the FastAPI application instance
def predict(data: Data) -> pd.DataFrame:
    '''
    ML API endpoint to predict against the request received from the client.
    When a client makes a POST request to /predict with a JSON payload, FastAPI 
    parses this JSON payload into an instance of the Data class. For example, if the JSON payload is:
        #JSON ex:
        {
            "name": "Maruti Suzuki Swift",
            "automaker": "Maruti",
            "year": 2019,
            "miles_driven": 100,
            "fuel_type": "Petrol"
        }
    FastAPI will convert this JSON into a Data object with the corresponding attributes.

    Parameters
    :data:(Class instance):(Pydantic): data parameter should be an instance of the Data class. 
    :data.name:(Class Attribute): Attr. of "Data" class, they're accessed via dot notation.
    :data.year:(Class Attribute): Attr. of "Data" class, they're accessed via dot notation.
    :data.miles_driven:(Class Attribute): Attr. of "Data" class, they're accessed via dot notation.
    :data.fuel_type:(Class Attribute): Attr. of "Data" class, they're accessed via dot notation.
    
    :data:(np.array): Var. holding an array object w/ entries from "Data" class attr.
    :result:(pd.DataFrame): Reference holding a Dataframe

    Returns:
    :result:(pd.DataFrame): 
    '''
    result = model.predict(pd.DataFrame(
        columns=['name','automaker','year','miles_driven','fuel_type'],
        data=np.array([data.name,data.automaker,data.year,data.miles_driven,data.fuel_type]).reshape(1,5)))[0]
    return result

 

def main():
    uvicorn.run("iii_create_API:app", host="127.0.0.1", port=8000, reload=True)
    

  

if __name__ == '__main__':
    main()