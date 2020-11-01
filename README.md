# Colens3DevTask
Before running the app make sure to set valid AWS access and private keys on lines 20 and 21 inside of docker-compose.yml

The run the app start docker-compose.yml using **docker-compose up** command 
This will install the necessary python libs and Redis inside Docker containers
and start the Flask Server

The Server has three POST endpoints:  
    - **http://localhost:5000/load** - fetches single key from S3 and stores it in Redis  
        HTTP Request Body Example:  
        ```json
        {
            "bucket": "bucket_name",
            "key": "path/to/file.txt"
        }
        ```  
    - **http://localhost:5000/loadAll** - fetches all keys from an S3 bucket and stores them in Redis  
        HTTP Request Body Example:  
        ```json
        {
            "bucket": "bucket_name"
        }
        ```  
    - **http://localhost:5000/fetch** - fetches stored data from redis by bucket name  
        HTTP Request Body Example:  
        ```json
        {
            "bucket": "bucket_name"
        }
        ```  

To run the cli:
    - first ssh into the app container:
        **docker exec -it cpt_app /bin/sh**
    - then run the cli script with appropriate arguments, example:
        **python cli.py -option [load | loadAll | fetch] -bucket [bucket_name] -key [key_name]**


You can run the tests in two ways:  
    - you will need a virtual environment and you will have to install the libs from requirements.txt or  
    - you can run them from the docker container

creating virtual environment:
**python -m venv ./venv**  

activating virtual environment - powershell:
**./venv/Scripts/activate.ps1**

deactivating virtual environment - powershell:
**deactivate**  

installing dependencies:
**pip install -r requirements.txt**

At the moment, there is one unit and one integration test, you can run those with:  
**python -m unittest services/aws_s3_service_test.py**  
**python -m unittest services/redis_service_integration_test.py**


