import xml.etree.cElementTree as ET
import pprint
import re
import codecs
from collections import defaultdict
from pymongo import MongoClient

def test():
    
    client = MongoClient('mongodb://localhost:27017')
    # 'examples' here is the database name. It will be created if it does not exist.
    db = client.osm_db5
    coll = db.detroit
   
    print "number of unique users: " + str(len(coll.distinct("created.user")))
    print "number of nodes: " + str(coll.find({"type":"node"}).count())
    print "number of ways: " + str(coll.find({"type":"way"}).count())
    print "number of relations: " + str(coll.find({"type":"relation"}).count())
    print "Total number of users: " + str(coll.find({"created.user": {"$exists":1}}).count())
   
    
    result = coll.aggregate([
        {"$group": {"_id": "$created.user",
                    "count": {"$sum":1}}},
        { "$sort": {"count": -1}} ])
    print list(result)
    
    business_names = coll.aggregate([
        {"$group": {"_id": "$address.businessName",
                    "count": {"$sum":1}}},
        { "$sort": {"count": -1}} ])
    print list(business_names)
    
    reviewed = coll.aggregate([
        {"$group": {"_id": "$address.reviewed",
                    "count": {"$sum":1}}},
        { "$sort": {"count": -1}} ])
    print list(reviewed)
    
    street_names = coll.aggregate([
        {"$group": {"_id": "$address.streetName",
                    "count": {"$sum":1}}},
        { "$sort": {"count": -1}} ])
    print list(street_names)
    
    road_type = coll.aggregate([
        {"$group": {"_id": "$address.highway",
                    "count": {"$sum":1}}},
        { "$sort": {"count": -1}} ])
    print list(road_type)
    
    
if __name__ == "__main__":
    test()
