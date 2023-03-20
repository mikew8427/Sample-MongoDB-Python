#
# Adds a job to the HPC system
#
import sys
import pymongo
from pymongo import MongoClient

if __name__ == "__main__":
  x=len(sys.argv)
  if x < 5 :
     print(" ")
     print("Usage HPCJob <job> <app> <license> <criteria>")
     print("Criteria can be either CPU NET DISK")
     print(" ")
     exit(12)

  print("Adding Job with Application :"+sys.argv[1]+" "+sys.argv[2])
client = pymongo.MongoClient("mongodb://admin:mprcrw05@cluster0-shard-00-00.59whp.mongodb.net:27017,cluster0-shard-00-01.59whp.mongodb.net:27017,cluster0-shard-00-02.59whp.mongodb.net:27017/Cluster0?ssl=true&replicaSet=atlas-6fpmhp-shard-0&authSource=admin&retryWrites=true&w=majority")

#
# The next two lines will access or create a DB called testdb and a collection under that
# called testcol
#
db =client["HCPBase"];
testcol=db.hcpjobs

#
# Gebnerate a documemnt to insert
#
mydoc= {"job": sys.argv[1], "app": sys.argv[2], "lic":sys.argv[3], "criteria" : sys.argv[4]};

#
#Insert the doc and disply the result and ID if it was created
#
r=testcol.insert_one(mydoc);
if r != None :
   print("ID: ", r.inserted_id);
   print("Job added: " + sys.argv[1])
