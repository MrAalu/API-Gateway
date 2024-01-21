FROM python:3.12.1-alpine 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /order_microservice

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:9000"]

# docker build -t order_microservice .
# docker run -it --name order_microservice_container -p 9000:9000 --network=kong-net order_microservice