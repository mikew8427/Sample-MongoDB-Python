#
# Adds a job to the HPC system
#
import sys
import time
from datetime import date
from datetime import datetime
import pymongo
from pymongo import MongoClient

if __name__ == "__main__":

    x=len(sys.argv)
    if x < 2 :
        print(" ")
        print("Usage simulate <system name>")
        exit(12)
    print("Start simulation for [",  sys.argv[1] , "]" )
    client = pymongo.MongoClient("mongodb://admin:mprcrw05@cluster0-shard-00-00.59whp.mongodb.net:27017,cluster0-shard-00-01.59whp.mongodb.net:27017,cluster0-shard-00-02.59whp.mongodb.net:27017/Cluster0?ssl=true&replicaSet=atlas-6fpmhp-shard-0&authSource=admin&retryWrites=true&w=majority")
    WaitFor=100
#
# The next two lines will access or create a DB called testdb and a collection under that
# called testcol
#
db =client["HCPBase"]
testcol=db.hpcschedule

def process_work(ID : str):
    #
    # Look to find am unassigned schedule that is ready to run
    #
    mydoc = {"_id": ID}
    while True :
        time.sleep(1)
        r: object
        r = testcol.find(mydoc).limit(1)
        if r == None:
            print("Unrecoverable Error Job ID no longer exits")
            return 0
        num = list(r)
        if len(num) == 0:
            print("Unrecoverable Error Job ID no longer exits")
            return 0
        stat=num[0]["status"]
        if stat == 'PAUSE':
            print("PAUSE current job for :" ,num[0]["name"])
            continue
        if stat == 'CANCEL':
            print("Cancel current job for :" ,num[0]["name"])
            return 1
        today = date.today()
        dte = "{}-{}-{}".format(today.year, today.month, today.day)
        # print("Current Date is =", dte)
        rnow = datetime.now()
        tme = rnow.strftime("%H:%M:%S")

        upd = {"$set": {"status": "RUNNING", "exedate": dte, "exetime" : tme}}
        r = testcol.find_one_and_update(mydoc, upd)

    return 1


def wait_for_work():
    #
    # This routine is called with we wait for work we can get.
    #
    time.sleep(1)
    today = date.today()
    dte = "{}-{}-{}".format(today.year, today.month, today.day)
    # print("Current Date is =", dte)

    rnow = datetime.now()
    tme = rnow.strftime("%H:%M:%S")
    # print("Current Time =", tme)

    mydoc = {"status": "Unassigned", "date": {"$lte": dte}, 'time': {"$lte": tme}}
    #
    # Look to find am unassigned schedule that is ready to run
    #
    r: object
    r = testcol.find(mydoc).limit(1)
    num = list(r)
    if len(num) == 0:
        return 0
#   print("%20.20s %20.20s %20.20s" % ("ID", "Name", "Status"))
#   print("%20.20s %20.20s %20.20s" % (num[0]["_id"], num[0]["name"], num[0]["status"]))

    upd = {"$set": {"status": "Assigned", "server": sys.argv[1]}}
    r = testcol.find_one_and_update(mydoc, upd)
    if r == None:
        print("Could not acquire resource to update:  [" + num[0]["name"] + "]")
        return 0
    print("System [" + sys.argv[1] + " has acquired job [" + num[0]["name"] + "]")
    return num[0]["_id"]


while True :
    id = wait_for_work()
    if id == 0:
        print("Waiting for work...")
        continue
    else :
        print("Work found for Object ID: ", id)
        process_work(id)
        continue
