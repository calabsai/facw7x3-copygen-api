## Backend API

This API is built using Flask micro server. You can run API using following commands. All major modules are in `src` directory.

### Run Locally
```
python main.py
# or
flask run # add config in .env for specify in cmd
```

### Using Docker
Using docker makes it easier to run API on any environment
```
docker build -t api .
docker run -p 8080:8080 api
```

### Deploy to GCloud
You can also send build to gcloud container registry using GCloud console. Change `PROJECT_ID` and `REPO_NAME` according to your requirements.
```
gcloud builds submit --tag gcr.io/PROJECT_ID/REPO_NAME
```
Then you can either deploy using `CLI` or `Console`

For more details, follow this tutorial.
[Deploy Flask app to GCloud Run](https://mlhive.com/2022/02/deploy-deep-learning-models-using-flask-docker-and-github-on-google-cloud)