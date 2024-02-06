# "Async Weather Checker"

"Async Weather Checker" is a simple application 
for getting data from several weather providers, 
calculating average temperature and storing all 
the results to a file. This logic will repeat itself a 
certain number of times, specified by the user. 
After each iteration the application will sleep for a 
certain amount of time, also specified by the user.

### Configure application:

Application can be configured in two points:
1. Number of times, used for requesting weather providers, 
and interval between each iteration. 
These settings are configured in 
<b><i>src/configs/yaml_configs/customized_settings.yaml</i></b> 
file;

2. Weather providers, which would be used by 
application during each iteration, and location, which weather will be monitored. 
These settings are configured in 
<b><i>src/configs/yaml_configs/weather_resources.yaml</i></b> 
file. Also, this file contains templates 
for several weather providers. For each template user 
can paste his token for correct provider usage or delete 
the template. Also, user can add his own template, 
if he/she wants to.



## All the instructions below should be run from project's root directory.</b>

### Run app using source files:

There are two ways to run application using source 
files:<br>

1. By running created for automation bash file, which will 
call other bash files to:
   1) configure environment;
   2) clean last launch files, if exists;
   3) run tests;
   4) run app, if all tests were successfully passed.


    bash start.sh

2. Using standard python way by installing 
requirements:


    pip install -r requirements.txt

and run main python script:

    python src/main.py


### Run app via docker:

There are two ways to run application via docker:<br>
1. By running created for automation Makefile file,
which will:
   1) Clean last docker launch data 
   (container, image and volumes), if exists;
   2) Build docker image and it's environment;
   3) Run app via docker.


    make -C docker clean && make -C docker build && make -C docker run

2. Using docker commands directly:

   
    cd ./docker && sudo docker-compose build && sudo docker-compose up

Before using docker commands, file with future results
(<b><i>weather_results.csv</i></b>) should be created
(also in project's root directory) locally on 
docker-host for correct binding of docker mount:
    

    touch weather_results.csv

### Run tests:

There are two ways to run tests for current application:<br>
1. By running created for tests bash file:


    bash run_tests.sh

2. Using <a href="https://docs.pytest.org/en">PyTest</a> 
to run tests directly.
