# HeyJobs Python Assessment Task

Thank you for taking the time to complete this test task! The purpose of the task is to get an idea of your development style: the way you structure code, testing strategy, etc.

## Requirements

* Build a python application which:
   * scrapes data from our website
   * stores results in the database

#### Scraper
This part of the task implies scraping **uid** and **title** of Ads from the following page: https://www.heyjobs.de/en/jobs-in-berlin.
* Each Ad is wrapped in an **&lt;a&gt;** tag. E.g.
```
<a href="/en/jobs/1e61e323-1e90-4b0c-a4cf-949ca74bbd7a" ...>
```
* Ad **uid** is the last part of the relative url. In this case it is `1e61e323-1e90-4b0c-a4cf-949ca74bbd7a`
* Title is the bold text at the top of each Ad
* Only data from the first page is required. No need to implement pagination.

#### Database
The scraped data should be stored in the database table with the following schema:
```
id | uid | title
```

#### Docker
This project is containerized to simplify implementation and testing.
`run.py` is supposed to trigger the scraper. So it is used as an entrypoint in the Dockerfile.
However you are free to change the entrypoint and the Dockerfile to fit your needs.  
The configuration specified in `docker-compose.yml` implies the following database connection params:
```
dbname: 'heyjobs'
host: 'db'
port: 5432
user: 'test'
password: 'testpass'
```

### Running the Task
We will run your solution with these commands:
```
docker-compose run --rm start_dependencies
docker-compose up scraper
```

After the scraper command finishes we expect the corresponding table to be filled with the scraped data.

## Note
Don't fork this repository. Create your own repository and send us a link to it. You may describe some of the assumptions you had in the README file of your repository.

**Have fun!**
