#
# Adds a job to the HPC system
#
import sys
import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb://admin:mprcrw05@cluster0-shard-00-00.59whp.mongodb.net:27017,cluster0-shard-00-01.59whp.mongodb.net:27017,cluster0-shard-00-02.59whp.mongodb.net:27017/Cluster0?ssl=true&replicaSet=atlas-6fpmhp-shard-0&authSource=admin&retryWrites=true&w=majority")

#
# The next two lines will access or create a DB called testdb and a collection under that
# called testcol
#
db =client["HCPBase"];
testcol=db.hcpjobs

#
#Perform test
#
x=testcol.count()
print("Number of records ",x)

r=testcol.find();
if r == None :
   print("Jobs not found added")
   exit(12)
print("%20.20s %20.20s %20.20s" % ("Job", "Application", "Criteria"))
for doc in r:
   print("%20.20s %20.20s %20.20s" % (doc['job'], doc['app'], doc['criteria']))


