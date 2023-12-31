FROM python:3.11
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
COPY ./run.py /code/run.py
COPY ./test.env /code/test.env
COPY favicon.svg /code/favicon.svg
COPY ./templates /code/templates
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "15400", "--workers", "4"]