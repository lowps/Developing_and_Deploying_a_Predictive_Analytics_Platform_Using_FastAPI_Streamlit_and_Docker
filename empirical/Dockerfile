FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

COPY requirements.txt /src/

RUN pip install -r /src/requirements.txt

COPY ./src /src/

COPY ./data/final /data/final/ 