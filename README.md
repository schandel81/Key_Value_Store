# Key_Value_Store
A Distributed Key Value Store with replication across 4 Process nodes. 

Prerequisites:
1. Install flask, python, virtualenv and requests before running Key_Value_Store:

On Mac:

sudo easy_install flask python virtualenv requests

On Linux:

sudo apt-get update

sudo apt-get upgrade -y

sudo apt-get install flask python virtualenv requests

2. Check versions to see if everything is installed properly:

python --version

virtualenv --version

flask --version

requests --version

3. Download the repo, unzip it and cd into Key_Value_Store directory:

https://github.com/schandel81/Key_Value_Store/archive/master.zip 

4. Make the kvstore_start_script as executable:

sudo chmod 777 kvstore_start_script

5. Run the script(kvstore_start_script):

./kvstore_start_script

6. The script will start 4 Key_Value_Process nodes on following ports:
 
   5000, 4000, 3000, 2000

7. Supported app routes:
  
    a. Set key Value: http://localhost:5000/setkey/Sandeep?value=Chandel
  
    b. Get key Value: http://localhost:4000/get/Sandeep
  
    c. Get all KV data: http://localhost:2000/get

8. The data will be returned in Json format:

{"data":{"Sandeep":{"time":1536830373.993948,"value":"Chandel"}}}

9. The time represent the exact time of write on each KV data and it would be diffent on different nodes for same KV data.

10. The set call with same key will overwrite the data.

11. Run "pkill python" on cmd before restarting.


TODO:

Add Docker File for Ubuntu 14.04.

Use pathos thread pool to make replication parallel, which will improve performance.

Handle replication in /clear app path.

Implement consistency levels(QUORUM, ALL) for kv store.

Read repair mechanism.

Partitioning using hashing.





