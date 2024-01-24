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

*Note : If you want to Run the Microservice on Container than make sure its on the Same Docker network as Kong and You can find the Microservice Container IP using `docker inspect kong-net` where,'kong-net' is the Docker Network where all the KongGateway,Kong DB, Microservices are Running! than the SERVICES URL will be `http://Microservices_Container_IPV4_address:PORT`*

**DONT FORGET TO EXPOSE THE PORT!**

2. Create **ROUTES** for the SERVICE and SELECT the DESIRED HTTP Methods i.e. Get,Post,etc. Access the Django URLs at `http://localhost:8000/django_url/`

*Note : If you put path '/route_path_name' on ROUTES than to access the Django URL's you have to goto `http://localhost:8000/route_path_name/django_url/`*


### JWT Token/Cookie Authentication Plugin

1. First Install the JWT Token Plugin. `KEY` = `JWT Header 'iss' (issuerClaim)` and  `SIGNING_KEY (SECRET_KEY)` = `JWT SECRET_KEY`.
2. Can setup the Cookie name i.e. access_token etc.
3. In Django we can Setup simple-JWT to create a JWT Token with Custom 'ISS' Header and 'JWT SECRET_KEY' where, the 'SECRET_KEY' of Token Creation should match the 'SECRET_KEY' of the KONG GATEWAY.
4. URL 
```
 path("api/token/", CustomTokenObtainPairView.as_view(), 
```
5. Settings.py
```
 # In Settings.py we have to create our own JWT SECRET_KEY/Signing_Key  
  SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=15),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": "KongJWT Credential SecretKey HERE",
}
```
6. Views
```
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

# Custom Class to modify JWT Token Headers
class CustomAccessToken(AccessToken):
    def __init__(self, token, *args, **kwargs):
        super().__init__(token, *args, **kwargs)
        self.payload["iss"] = "KongJWT Credential Key HERE"


# Custom Login View 
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Customize the response to set tokens in cookies
        if "access" and "refresh" in response.data:
            access_token = response.data["access"]
            refresh_token = response.data["refresh"]

            # Use your custom access token class
            custom_access_token = CustomAccessToken(access_token)

            # Get the modified access token
            modified_access_token = custom_access_token.__str__()

            # Set the access token in a cookie
            response.set_cookie(
                "access_token", modified_access_token, httponly=True, secure=True
            )

            # Set the refresh token in a cookie
            response.set_cookie(
                "refresh_token", refresh_token, httponly=True, secure=True
            )

        return response
```
*Note : If we are not using Cookie and if we are using Request Headers for JWT Authentication then, the Token should be created in same way i.e. 'iss' and 'signing_key'*.