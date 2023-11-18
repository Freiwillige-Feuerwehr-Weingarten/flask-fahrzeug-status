FROM python:3.11
RUN pip3 install psycopg psycopg-binary psycopg-pool asyncio uvicorn fastapi pydantic-settings python-dotenv jinja2 MarkupSafe websockets
COPY ./app /app
COPY ./test.env /test.env
COPY favicon.svg /
COPY ./templates /templates
CMD ["uvicorn", "app.run:app", "--host", "0.0.0.0", "--port", "15400"]