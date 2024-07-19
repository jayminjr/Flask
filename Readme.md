# FLASK APP

### Created flask app for learning purpose.
#### Below are steps to setup and run app locally.
##### Create virtualenv
``` virtualenv --python=/Users/upforcetech/.pyenv/versions/3.9.1/bin/python venv ```
##### Install requirements
```pip install -r requirements.txt```
##### Perform db migration
```flask db upgrade```
##### Run flask app
```flask run```

#### To run in docker
```docker compose up -d```

#### Swagger ui endpoint
```/swagger-ui```

#### Below are steps to build local docker image and push to local docker registry
``` docker build -t localhost:5000/flask-store-app:latest . ```

``` docker push localhost:5000/flask-store-app:latest ```