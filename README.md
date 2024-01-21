# API-Gateway KONG 🦍

API-Gateway in Microservice Architecture

## Get Started with Kong DOCKER

1. Create Docker Network for KONG and Kong DB (PostgreSQL)

```

docker network create kong-net

```

2. Run PostgreSql Container

```

docker run -d --name kong-database --network=kong-net -p 5432:5432 -e "POSTGRES_USER=kong" -e "POSTGRES_DB=kong" -e "POSTGRES_PASSWORD=kongpass" postgres:13

```

3. Setup Initial DB Schema for KONG using Bootstrap(create the required tables and structures)

```

docker run --rm --network=kong-net -e "KONG_DATABASE=postgres" -e "KONG_PG_HOST=kong-database" -e "KONG_PG_PASSWORD=kongpass" -e "KONG_PASSWORD=test" kong/kong-gateway:3.5.0.2 kong migrations bootstrap

```

4. Run KONG Container

```

docker run -d --name kong-gateway --network=kong-net -e "KONG_DATABASE=postgres" -e "KONG_PG_HOST=kong-database" -e "KONG_PG_USER=kong" -e "KONG_PG_PASSWORD=kongpass" -e "KONG_PROXY_ACCESS_LOG=/dev/stdout" -e "KONG_ADMIN_ACCESS_LOG=/dev/stdout" -e "KONG_PROXY_ERROR_LOG=/dev/stderr" -e "KONG_ADMIN_ERROR_LOG=/dev/stderr" -e "KONG_ADMIN_LISTEN=0.0.0.0:8001" -e "KONG_ADMIN_GUI_URL=http://localhost:8002" -e KONG_LICENSE_DATA -p 8000:8000 -p 8443:8443 -p 8001:8001 -p 8444:8444 -p 8002:8002 -p 8445:8445 -p 8003:8003 -p 8004:8004 kong/kong-gateway:3.5.0.2

```

### Services and Routes

1. Create **SERVICES** using IPV4 Address where KONG is running with the Microservices PORT's. For Eg : If we run Django Microservice using `python3 manage.py runserver 0.0.0.0:9000` than the SERVICES URL will be `http://IPV4_address:9000`
*Note : If you want to Run the Microservice on Container than make sure its on the Same Docker network as Kong and You can find the Microservice Container IP using `docker inspect kong-net` where,'kong-net' is the Docker Network where all the KongGateway,Kong DB, Microservices are Running! than the SERVICES URL will be `http://Microservices_Container_IPV4_address:PORT`. DONT FORGET TO EXPOSE THE PORT!

2. Create **ROUTES** for the SERVICE and SELECT the DESIRED HTTP Methods i.e. Get,Post,etc. Access the Django URLs at `http://localhost:8000/django_url/`

*Note : If you put path '/route_path_name' on ROUTES than to access the Django URL's you have to goto `http://localhost:8000/route_path_name/django_url/`
