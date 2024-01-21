FROM python:3.12.1-alpine 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /product_microservice

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:9005"]

# docker build -t product_microservice .
# docker run -it --name product_microservice_container -p 9005:9005 --network=kong-net product_microservice