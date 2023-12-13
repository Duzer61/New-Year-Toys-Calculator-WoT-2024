FROM python:3.12

RUN pip3 install --upgrade pip

WORKDIR /calculator_app

RUN pip install gunicorn==20.1.0

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "calculator.wsgi"]
