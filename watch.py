#
# Adds a job to the HPC system
#
import sys
import os
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps

client = pymongo.MongoClient("mongodb://admin:mprcrw05@cluster0-shard-00-00.59whp.mongodb.net:27017,cluster0-shard-00-01.59whp.mongodb.net:27017,cluster0-shard-00-02.59whp.mongodb.net:27017/Cluster0?ssl=true&replicaSet=atlas-6fpmhp-shard-0&authSource=admin&retryWrites=true&w=majority")

#
# The next two lines will access or create a DB called testdb and a collection under that
# called testcol
#
db =client["HCPBase"];
hcpjobs=db.hcpjobs.watch();
print("%20.20s %20.20s %20.20s" % ("Operation", "Fields","Value"))
for change in hcpjobs:
   fields=change['updateDescription']['updatedFields']
   for dt in fields:
      op=fields[dt]
      print("%20s \t %20s \t %20s" % (change['operationType'] ,dt,op))
