import pymongo
from datetime import datetime
from dateutil import parser


if __name__ == '__main__':
    mongo_connection_uta_stage = "mongodb+srv://cluster0.shzhn.mongodb.net/admin?replicaSet=atlas-y7qbzb-shard-0&readPreference=primary&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1"
    client_uta = pymongo.MongoClient(mongo_connection_uta_stage)

    db_uta = client_uta["uta"]
    # db_uta = client_uta["test"]
    col_people = db_uta["people"]
    col_variety = db_uta["variety_talents"]
    qry_uta_client = {"type": "Client"}
    cur_uta_talent = col_people.find(qry_uta_client, {"name": 1, "birthday":1})
    qry_variety = {"agencies.company_id": "10039"}
    lst_variety = list(col_variety.find(qry_variety, {"first_name": 1, "middle_name": 1, "last_name": 1, "talent_id":1, "birthdate":1}))
    dic_people = {}

    for uta_talent in cur_uta_talent:
        dic_people[uta_talent.get("name")] = uta_talent

    # if dic_people["21 Savage"].get("birthdate") == None:
    # print(len(lst_variety))

    count = 0
    for variety_talent in lst_variety:
        if variety_talent.get("middle_name") == "" and variety_talent.get("last_name") != "":
            name = variety_talent.get("first_name") + " " + variety_talent.get("last_name")
            if name in dic_people.keys():
                results = col_people.update_one({"_id": dic_people[name].get("_id")}, {"$set": {"variety_talent_id": variety_talent.get("talent_id")}})
                count = count + 1
    print(count)

    count = 0
    for variety_talent in lst_variety:
        if variety_talent.get("middle_name") == "" and variety_talent.get("last_name") == "":
            name = variety_talent.get("first_name")
            if name in dic_people.keys():
                col_people.update_one({"_id": dic_people[name].get("_id")}, {"$set": {"variety_talent_id": variety_talent.get("talent_id")}})
                count = count + 1
    print(count)

    count = 0
    for variety_talent in lst_variety:
        if variety_talent.get("middle_name") != "" and variety_talent.get("last_name") == "":
            name = variety_talent.get("first_name") + " " + variety_talent.get("middle_name")
            if name in dic_people.keys():
                print(name)
                col_people.update_one({"_id": dic_people[name].get("_id")}, {"$set": {"variety_talent_id": variety_talent.get("talent_id")}})
                count = count + 1
                print(count)

    count = 0
    for variety_talent in lst_variety:
        if variety_talent.get("middle_name") != "" and variety_talent.get("last_name") != "":
            name = variety_talent.get("first_name") + " " + variety_talent.get("middle_name") + " " + variety_talent.get("last_name")
            if name in dic_people.keys():
                print(name)
                col_people.update_one({"_id": dic_people[name].get("_id")}, {"$set": {"variety_talent_id": variety_talent.get("talent_id")}})
                count = count + 1
    print(count)

    #
    # count1 = 0
    # count2 = 0
    # for variety_talent in lst_variety:
    #     if variety_talent.get("middle_name") != "" and variety_talent.get("last_name") != "":
    #         name1 = variety_talent.get("first_name") + " " + variety_talent.get("last_name")
    #         name2 = variety_talent.get("first_name") + " " + variety_talent.get("middle_name") + " " + variety_talent.get("last_name")
    #         if name1 in dic_people.keys():
    #             print("without middle name: " + name1)
    #             col_people.update_one({"_id": dic_people[name].get("_id")}, {"$set": {"variety_talent_id": variety_talent.get("talent_id")}})
    #             count1 = count1 + 1
    #         elif name2 in dic_people.keys():
    #             print("with middle name: "  + name2)
    #             count2 = count2 + 1
    #         else:
    #             print("New to UTA: " + name2)
    # print(count1)
    # print(count2)

    # count = 0
    # for variety_talent in lst_variety:
    #     if variety_talent.get("middle_name") != "" and variety_talent.get("last_name") != "":
    #         name = variety_talent.get("first_name") + " " + variety_talent.get("last_name")
    #         if name in dic_people.keys() and dic_people[name].get("birthday") is not None and variety_talent.get("birthdate") != "" and dic_people[name].get("birthday") == parser.parse(variety_talent.get("birthdate")):
    #             #print(name)
    #             col_people.update_one({"_id": dic_people[name].get("_id")}, {"$set": {"variety_talent_id": variety_talent.get("talent_id")}})
    #             count = count + 1
    # print(count)
    #




