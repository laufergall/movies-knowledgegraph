FROM python:3.6.5-slim

WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip && \
    pip install --trusted-host pypi.python.org -r requirements.txt

COPY main.py /app/
COPY apis /app/apis/

RUN chmod 644 main.py

EXPOSE 8001

CMD ["python", "main.py"]
