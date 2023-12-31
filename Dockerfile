FROM python:3.11

RUN mkdir /purchases

WORKDIR /purchases

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /purchases/docker/*.sh

CMD ["gunicorn", "app.fast_api_programm:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]