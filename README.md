# recommender
Recommender system for movies. Combination of static metrics and visual review of recommendations.

Includes the following algorithms:
* Recommendations by popularity
* Recommendations by movie descrition
* Item/Item collaborative filtering
* User/User collaborative filtering
* Regularized SVD

## Project Setup
In the following, we will go through the steps to set up this system. 

The first thing is to download this repository. Secondly, create a themoviedb.org ID needed to run the website.

### Download source code
You have two choices for downloading the source code – downloading a zip file of the source code or using Git. 

* *Downloading a zip file*
 
   From the main [directory on GitHub](https://github.com/jug2505/recommender), 
   click the green “Clone or download” button and choose to download a zip file to your computer.
   
* *Using Git*

   Clone this repository or create a fork in your GitHub, and then clone that instead. The following command 
   will create a copy on your computer.
   `> git clone https://github.com/jug2505/recommender.git`

## Create a virtual environment for the project

Before you run the code, create a virtual environment.

```bash
> cd back
> virtualenv -p python3 venv
> source venv/bin/activate
```

### Get the required packages 
```bash
pip3 install -r requirements.txt
```

###  Configuration Django for PostGreSql connection

Open `rs_project/settings.py` 

Update this lines:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'moviegeek',                      
        'USER': 'db_user',
        'PASSWORD': 'db_user_password',
        'HOST': 'db_host',
        'PORT': 'db_port_number',
    }
}
```

Run the following commands:
```bash
> python3 manage.py makemigrations
> python3 manage.py migrate --run-syncdb
```

#### Populate the database 
Run the following scripts to download the datasets for the system. 
```bash
> python3 -m scripts.dataset_downloaders.movies_downloader
> python3 -m scripts.dataset_downloaders.raitings_downloader
> python3 -m scripts.dataset_downloaders.description_downloader
```

### Calculate recommendations
Run all scripts in scripts/calculators folder.

### Calculate static metrics
Run scripts/statistic/metrics.py script. It includes RMSE and Precision at K metrics.

### DB service run:
```
sudo service postgresql start
```

### Django server run
```bash
> python3 manage.py runserver 127.0.0.1:8081
```

### Vue.js project setup

```
npm install
```

### Vue.js developer server

```
npm run serve
```