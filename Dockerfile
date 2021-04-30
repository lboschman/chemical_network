FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . . 
EXPOSE 8050

CMD ["python", "./run_app.py"]
