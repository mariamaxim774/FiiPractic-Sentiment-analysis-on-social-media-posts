**Step 1:**: Virtual Environment setup:
If you don't have a virtual environment created within your project run the following command (make sure you have Python 3.10 installed on your system):
_python3.10 -m venv .venv_

Activate the virtual environment:
_source .venv/bin/activate_ (on MacOS / Linux)
_.venv/Scripts/activate_ (on Windows)

**Step 2:**: Create a Docker container and make sure it works:
Open the Docker client app that you installed in the previous trainings. Then run this command in a terminal:
_docker ps_

If there is no container displayed, as in the example below:
CONTAINER ID   IMAGE      COMMAND                  CREATED       STATUS         PORTS                    NAMES
59c671a20209   postgres   "docker-entrypoint.s…"   2 weeks ago   Up 8 seconds   0.0.0.0:9000->5432/tcp   my_postgres

then you will need to create your docker container that will contain the PostgresSQL database that our Flask app will connect to (make sure you run these commands from the directory in which you copied docker-composer.yml):
_docker-compose up -d_ 

We will check if the container was created by running again docker ps. 

If the container is up and running, then we will connect to the container by running this command:
_docker exec -it my_postgres psql -U admin -d socialmediadb_

The following prompt should be displayed, meaning that the connection was done successfully:
socialmediadb=# 

Try to create a table by writing: _CREATE TABLE test ();_
You should receive a response that says: CREATE TABLE
To check that the table was created, write this command to display the tables: _\dt_

If everything worked right, a table like this should be displayed to you, in which you should see the test table you just created:

         List of relations
 Schema |   Name   | Type  | Owner 
 -------+----------+-------+-------
 public | test     | table | admin
(1 row)

**Step 3:**: Install the libraries needed for running our Flask app (make sure the venv is active):

_pip install -r requirements.txt_

**Step 4:**: Start the Flask app

_flask run_
Make some calls to the API using Postman to test that the application is up and running and the endpoints work. 

**Step 5:**: Run unit tests

Make sure you're in the base directory of your project (e.g. if you're project is called my_app, make sure you are in this directory before starting your flask app).

Run the tests by providing the test class in which the tests can be found. They will be run one by one. 
You should have virtual environment active for running the tests.
_python -m unittest tests.integration_tests.test_posts.PostDatabaseIntegrationTestCase_

Check test coverage by running the tests first, and then execute this command:
_coverage run -m unittest discover_

 _-m unittest discover_: this will run the tests using the unittest framework and search for tests automatically by taking those files that start with test_
 
To generate a report, run:
_coverage report_

Or run the following command to generate a htmlcov/index.html file. If you open it in your browser, you will find a more detailed report:
_coverage html_ 

After you're done, you can remove the coverage data with _coverage erase_. 
