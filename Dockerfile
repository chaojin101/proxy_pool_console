FROM python:3.10-alpine

WORKDIR /home/proxy_pool_console

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "src/main.py"]