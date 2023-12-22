FROM python:3.11.7-alpine3.19

WORKDIR /service
COPY . ./
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "app.py"]