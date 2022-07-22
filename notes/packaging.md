# Creating Dockerfile

* If we don't have a `requirements.txt` then create one on the project root folder, by running this command:

```sh
# this freezes the dependencies and stores them in a requirements.txt file
pip freeze > requirements.txt
```

* Create a new file called `Dockerfile` also inside the project root folder (same as manage.py)
* This generic recipe writen in the Dockerfile, for Django:
    - select a base image with `FROM <base_image_name>`
    - select a folder where to store your app with `WORKDIR <folder_name>`
    - copy `requirements.txt` into the image
    - run `pip install`
    - copy the rest of the files

* You can see [an example here](../Dockerfile)
* **NOTE:** we don't want the sqlite3 to be packaged, so we need to ignore it

## Ignoring files when building the image

* Create a `.dockerignore` in the root folder of your project
* Inside it, put the files you want Docker to ignore
* You can see [an example here](../.dockerignore)

## Declaring the services our app needs using `docker compose`

* **Version**: (most people use `3` as default')
* **Services** list all the services that make part of this project
* The first part is the django project services (eg.tweets_project)
* Within the service we need to build it;
* then pass on all the commands necessary to run the django app;
* finally declare the port

## Important shell commands

* To build the docker image (if not using docker-compose build)

```sh
docker build . -t <image_name>

# for the tweets_project this becomes
docker build . -t tweets_project
```

* to start the docker containers described in the `docker-compose.yml` file

```sh
# the -d flag detaches the containers so they start in the background
docker compose up -d
```

* to see the logs of a container

```sh
# -f flag is for following the output
docker compose logs -f <service_name>

# e.g. to check the logs of the tweets_project
docker compose logs -f tweets_project
```

* to stop and remove all containers

```sh
docker compose down
```
