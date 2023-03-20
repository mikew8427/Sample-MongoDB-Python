#
# Adds a user and password to the HPC system
#
import sys
import pymongo
from pymongo import MongoClient

if __name__ == "__main__":
  x=len(sys.argv)
  if x < 3 :
     print("Usage HPCAddU <user> <password>")
     exit(12)

  print("Adding user with password :"+sys.argv[1]+" "+sys.argv[2])
client = pymongo.MongoClient("mongodb://admin:mprcrw05@cluster0-shard-00-00.59whp.mongodb.net:27017,cluster0-shard-00-01.59whp.mongodb.net:27017,cluster0-shard-00-02.59whp.mongodb.net:27017/Cluster0?ssl=true&replicaSet=atlas-6fpmhp-shard-0&authSource=admin&retryWrites=true&w=majority")

#
# The next two lines will access or create a DB called testdb and a collection under that
# called testcol
#
db =client["HCPBase"];
testcol=db.hcplogin

#
# Gebnerate a documemnt to insert
#
mydoc= {"name": sys.argv[1], "password": sys.argv[2], "Address":"239 N Fuquay Springs", "City":"Fuquay Varina", "Zip":"27526"};

#
#Insert the doc and disply the result and ID if it was created
#
r=testcol.insert_one(mydoc);
if r != None :
   print("ID: ", r.inserted_id);
   print("User added: " + sys.argv[1])
