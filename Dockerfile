FROM python:3.9

WORKDIR /main-bot

COPY ./* .

RUN pip install -r requirements.txt

# make sure all files available??
# RUN ls .

ENTRYPOINT ["python", "./main.py"]