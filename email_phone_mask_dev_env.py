import pymongo
from bson.objectid import ObjectId
import re

def loop_client():
    K1 = '*'
    K2 = '#'

    for uta_talent in dic_uta_talents.values():
        lst_contacts = []
        lst_addresses = []
        if "contacts" in uta_talent.keys() and uta_talent.get("contacts") != None and len(
                uta_talent.get("contacts")) > 0:
            lst_contacts = uta_talent.get("contacts")
        if "addresses" in uta_talent.keys() and uta_talent.get("addresses") != None and len(
                uta_talent.get("addresses")) > 0:
            lst_addresses = uta_talent.get("addresses")
        for address in lst_addresses:
            if "address" in address.keys():
                address["address"] = re.sub('[a-z]|[A-Z]|[0-9]', K1, address["address"])

        for contact in lst_contacts:
            if "contactType" in contact.keys() and contact.get("contactType") == "Email":
                contact["contact"] = re.sub('[a-z]|[A-Z]|[0-9]', K1, contact["contact"])
            if "contactType" in contact.keys() and contact.get("contactType") == "Personal Email":
                contact["contact"] = re.sub('[a-z]|[A-Z]|[0-9]', K1, contact["contact"])
            if "contactType" in contact.keys() and contact.get("contactType") == "Assistant Email":
                contact["contact"] = re.sub('[a-z]|[A-Z]|[0-9]', K1, contact["contact"])
            if "contactType" in contact.keys() and contact.get("contactType") == "Mobile Phone":
                contact["contact"] = re.sub('[a-z]|[A-Z]|[0-9]', K2, contact["contact"])
            if "contactType" in contact.keys() and contact.get("contactType") == "Office Phone":
                contact["contact"] = re.sub('[a-z]|[A-Z]|[0-9]', K2, contact["contact"])
            if "contactType" in contact.keys() and contact.get("contactType") == "Home Phone":
                contact["contact"] = re.sub('[a-z]|[A-Z]|[0-9]', K2, contact["contact"])
            if "contactType" in contact.keys() and contact.get("contactType") == "Fax Number":
                contact["contact"] = re.sub('[a-z]|[A-Z]|[0-9]', K2, contact["contact"])
            if "contactType" in contact.keys() and contact.get("contactType") == "Unknown":
                contact["contact"] = re.sub('[a-z]|[A-Z]|[0-9]', K1, contact["contact"])


        col_people.update_one({"_id": uta_talent.get("_id")}, {"$set": {"contacts": uta_talent.get("contacts"),
                                                                        "addresses": uta_talent.get("addresses")}})

        if "phone" in uta_talent.keys() and uta_talent.get("phone") != None:
            uta_talent["phone"] = re.sub('[a-z]|[A-Z]|[0-9]', K1, uta_talent["phone"])
            col_people.update_one({"_id": uta_talent.get("_id")}, {"$set": {"phone": uta_talent.get("phone")}})

        if "email" in uta_talent.keys() and uta_talent.get("email") != None:
            uta_talent["email"] = re.sub('[a-z]|[A-Z]|[0-9]', K1, uta_talent["email"])
            col_people.update_one({"_id": uta_talent.get("_id")}, {"$set": {"email": uta_talent.get("email")}})

if __name__ == '__main__':
    mongo_connection_uta_stage = "mongodb+srv://cluster0.shzhn.mongodb.net/admin?replicaSet=atlas-y7qbzb-shard-0&readPreference=primary&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1"
    client_uta = pymongo.MongoClient(mongo_connection_uta_stage)

    db_uta = client_uta["uta"]

    col_people = db_uta["people"]

    qry_variety = {}

    cur_uta_talents = col_people.find(qry_variety, {"contacts": 1, "addresses": 1, "email": 1, "phone": 1})
    dic_uta_talents = {}
    for uta_talent in cur_uta_talents:
        dic_uta_talents[uta_talent.get("_id")] = uta_talent

    loop_client()