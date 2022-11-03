import pymongo
from datetime import datetime
from dateutil import parser
from bson.objectid import ObjectId


def upsert_agency_relationalship():
    for variety_talent_id in dic_variety_uta_talents.keys():
        uta_talent = {}
        variety_talent = dic_variety_uta_talents[variety_talent_id]

        if variety_talent:
            uta_talent = dic_uta_talents[variety_talent_id]
            dic_internalTeam = {}
            lst_internal_team = []
            if "internalTeam" in uta_talent.keys() and uta_talent.get("internalTeam") != None and len(uta_talent.get("internalTeam")) > 0:
                lst_internal_team = uta_talent.get("internalTeam")
                for internalTeam_agent in lst_internal_team:
                    dic_internalTeam[internalTeam_agent["utaEmployee"]] = internalTeam_agent
            else:
                lst_internal_team = []
            if "agencies" in variety_talent.keys() and len(variety_talent.get("agencies")) > 0:
                lst_variety_talent_agencies = variety_talent.get("agencies")
                for variety_talent_agencies in lst_variety_talent_agencies:
                    if variety_talent_agencies["company_id"] == "10039" and "agents" in variety_talent_agencies.keys():
                        lst_variety_talent_agents = variety_talent_agencies.get("agents")
                        for variety_talent_agent in lst_variety_talent_agents:
                            if "point_agent" in variety_talent_agent and variety_talent_agent.get(
                                    "point_agent") == "Yes":
                                agent_type = "Point Agent"
                            else:
                                agent_type = "Agent"
                            if variety_talent_agent.get("first_name") + " " + variety_talent_agent.get(
                                    "last_name") in dic_uta_people_not_talents.keys():
                                    # and dic_uta_people_not_talents[
                                    # variety_talent_agent.get("first_name") + " " + variety_talent_agent.get(
                                    #     "last_name")].get("_id") not in dic_internalTeam.keys():
                                if dic_uta_people_not_talents[
                                    variety_talent_agent.get("first_name") + " " + variety_talent_agent.get(
                                        "last_name")].get("_id") not in dic_internalTeam.keys():
                                    merge_agent = {"utaEmployee": dic_uta_people_not_talents[
                                            variety_talent_agent.get("first_name") + " " + variety_talent_agent.get(
                                                "last_name")].get("_id"), \
                                         "type": agent_type, \
                                         "createdAt": datetime.utcnow(), "_id": ObjectId()}
                                    col_people.update_one({"_id": uta_talent["_id"]},
                                                          {"$push": {"internalTeam": merge_agent}})
                                    dic_internalTeam[dic_uta_people_not_talents[
                                        variety_talent_agent.get("first_name") + " " + variety_talent_agent.get(
                                            "last_name")].get("_id")] = merge_agent

                                #relationships
                                peopleid1 = dic_uta_people_not_talents[
                                    variety_talent_agent.get("first_name") + " " + variety_talent_agent.get(
                                        "last_name")].get("_id")
                                peopleid2 = uta_talent.get("_id")
                                if agent_type == "Point Agent":
                                    relationship_type = "ResponsibleAgent"
                                else:
                                    relationship_type = "Agent"
                                relationship = col_relationships.find_one(
                                    {"personId2": peopleid2, "personId1": peopleid1, "type": relationship_type})

                                if not relationship:
                                    result = col_relationships.insert_one(
                                        {"personId2": peopleid2, "personId1": peopleid1, "type": relationship_type})
                                    relationship_id = result.inserted_id
                                else:
                                    relationship_id = relationship.get("_id")

                                relationships = dic_uta_people_not_talents[
                                        variety_talent_agent.get("first_name") + " " + variety_talent_agent.get(
                                            "last_name")].get("relationships")
                                if relationships is None or relationship_id not in relationships:
                                    col_people.update_one({"_id": peopleid1},
                                                              {"$push": {"relationships": relationship_id}})
                                    dic_uta_people_not_talents[
                                        variety_talent_agent.get("first_name") + " " + variety_talent_agent.get(
                                            "last_name")]["relationships"].append(relationship_id)

                                relationships = uta_talent.get("relationships")
                                if relationships is None or relationship_id not in relationships:
                                    col_people.update_one({"_id": peopleid2}, {"$push": {"relationships": relationship_id}})
                                    uta_talent["relationships"].append(relationship_id)

                                #utaEmployee.internalTeam
                                personRelationships = dic_uta_people_not_talents[
                                    variety_talent_agent.get("first_name") + " " + variety_talent_agent.get(
                                        "last_name")].get("utaEmployeeInfo").get("internalTeam").get("personRelationships")
                                lst_personRelationships = []
                                if personRelationships != None:
                                    lst_personRelationships = [client.get("person") for client in personRelationships if client]
                                if peopleid2 not in lst_personRelationships:
                                    new_obj_id = ObjectId()
                                    col_people.update_one({"_id": peopleid1},
                                                          {"$push": {"utaEmployeeInfo.internalTeam.personRelationships": {"_id": new_obj_id, "person": peopleid2, "type": "Client", "createdAt": datetime.utcnow()}}})
                                    dic_uta_people_not_talents[
                                    variety_talent_agent.get("first_name") + " " + variety_talent_agent.get(
                                        "last_name")]["utaEmployeeInfo"]["internalTeam"]["personRelationships"].append({"_id": new_obj_id, "person": peopleid2, "type": "Client", "createdAt": datetime.utcnow()})
                            # else:
                            #     uta_employee = dic_variety_employee_contacts[variety_talent_agent.get("employee_id")]
                            #     uta_employee["variety_employee_id"] = uta_employee.pop("employee_id")
                            #     uta_employee["type"] = "Employee"
                            #     uta_employee["origin"] = "Variety Insert"
                            #     uta_employee["updateAt"] = datetime.utcnow()
                            #     uta_employee["name"] = variety_talent_agent.get(
                            #         "first_name") + " " + variety_talent_agent.get("last_name")
                            #     uta_employee["hasClients"] = True
                            #     uta_employee["vocations"] = ["Agent"]
                            #     doc = col_people.insert_one(uta_employee)
                            #     id = doc.inserted_id
                            #     uta_employee["_id"] = id
                            #     dic_uta_people_not_talents[uta_employee["name"]] = uta_employee
                            #
                            #     merge_agent = {"utaEmployee": id, "type": agent_type,
                            #                             "createdAt": datetime.utcnow(), "_id": ObjectId()}
                            #     dic_internalTeam[id] = merge_agent
                            #     # lst_internal_team = [dic_internalTeam[key] for key in dic_internalTeam.keys()]
                            #     # uta_talent["internalTeam"] = lst_internal_team
                            #     col_people.update_one({"_id": uta_talent["_id"]}, {"$push": {"internalTeam": merge_agent}})
                            #     peopleid1 = id
                            #     peopleid2 = variety_talent.get("_id")
                            #     if agent_type == "Point Agent":
                            #         relationship_type = "ResponsibleAgent"
                            #     else:
                            #         relationship_type = "Agent"
                            #     relationship = col_relationships.find_one(
                            #         {"personId2": peopleid2, "personId1": peopleid1, "type": relationship_type})
                            #
                            #     if not relationship:
                            #         result = col_relationships.insert_one(
                            #             {"personId2": peopleid2, "personId1": peopleid1, "type": relationship_type})
                            #         relationship_id = result.inserted_id
                            #     else:
                            #         relationship_id = relationship.get("_id")
                            #     relationships = []
                            #     relationships.append(relationship_id)
                            #
                            #     col_people.update_one({"_id": peopleid1}, {"$set": {"relationships": relationships}})
            # lst_internal_team = [dic_internalTeam[key] for key in dic_internalTeam.keys()]
            # uta_talent["internalTeam"] = lst_internal_team
            # col_people.update_one({"_id": uta_talent["_id"]}, {"$set": {"internalTeam": lst_internal_team}})
            # lst_internal_team = [dic_internalTeam[key] for key in dic_internalTeam.keys()]
            # for internal_team in lst_internal_team:
            #     if internal_team.get("type") == "Point Agent":
            #         tmp_internal_team = internal_team
            #         lst_internal_team.remove(internal_team)
            #         lst_internal_team.insert(0, tmp_internal_team)
            # uta_talent["internalTeam"] = lst_internal_team
            # if "_id" in uta_talent.keys():
            #     col_people.update_one({"_id": uta_talent["_id"]}, {"$set": uta_talent})



if __name__ == '__main__':
    mongo_connection_uta_stage = "mongodb+srv://cluster0.shzhn.mongodb.net/admin?replicaSet=atlas-y7qbzb-shard-0&readPreference=primary&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1"
    client_uta = pymongo.MongoClient(mongo_connection_uta_stage)
    # mongo_connection_uta_prod = "mongodb+srv://cluster0.njccd.azure.mongodb.net/?replicaSet=Cluster0-shard-0&readPreference=primary&serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1"
    # client_uta = pymongo.MongoClient(mongo_connection_uta_prod)
    db_uta = client_uta["uta"]
    col_people = db_uta["prod_people"]
    col_variety_talents = db_uta["variety_talents"]
    col_logs = db_uta['dc_logs']
    col_relationships = db_uta['relationships']
    col_archives = db_uta["people_backup"]
    col_variety_talent_contacts = db_uta["variety_talent_contacts"]
    col_variety_companies = db_uta["variety_companies"]
    col_variety_employee_contacts = db_uta["variety_employee_contacts"]
    col_variety_company_contacts = db_uta["variety_company_contacts"]
    col_uta_companies = db_uta["companies"]
    qry_variety = {"agencies.company_id": "10039"}
    # qry_variety = {"talent_id": "7112"}

    cur_variety_uta_talents = col_variety_talents.find(qry_variety).sort("modified_date", pymongo.ASCENDING)
    dic_variety_uta_talents = {}
    for variety_uta_talent in cur_variety_uta_talents:
        dic_variety_uta_talents[variety_uta_talent.get("talent_id")] = variety_uta_talent

    cur_uta_talents = col_people.find({"variety_talent_id": {"$exists": True}})
    dic_uta_talents = {}
    for uta_talent in cur_uta_talents:
        dic_uta_talents[uta_talent.get("variety_talent_id")] = uta_talent

    cur_uta_people_not_talents = col_people.find({"$or": [{"type": "Employee"}]},
                                                 {"name": 1, "relationships":1, "utaEmployeeInfo":1})
    dic_uta_people_not_talents = {}
    for uta_people_not_talent in cur_uta_people_not_talents:
        dic_uta_people_not_talents[uta_people_not_talent.get("name")] = uta_people_not_talent

    # relationships_cur = col_relationships.find({})
    # for i in dic_variety_uta_talents:
    #     for j in i.get("agencies"):
    #         for k in j.get("agents"):
    #             if k.get("middle_name"):
    #                 name = k.get("first_name") + " " + k.get("middle_name") + " " + k.get("last_name")
    #             else:
    #                 name = k.get("first_name") + " " + k.get("last_name")
    #             person = dic_uta_people_not_talents.get(name)
    #             person2 = dic_uta_talents.get(i.get("talent_id"))
    #             relationship = col_relationships.find_one({"personId2": person2.get("_id"), "personId1": person.get("_id")})
    #             if relationship:
    #                 result = col_relationships.insert_one({"personId2": person2.get("_id"), "personId1": person.get("_id"), "type": "Agent"})
    #                 col_people.update_one({"_id": person.get("_id")}, {"$push": {result.inserted_id}})
    #             list_clients = [client.get("person") for client in
    #             col_people.find({"_id": person.get("_id")}, {"utaEmployeeInfo.internalTeam.personRelationships": 1})]
    #             if person2.get("_id") in list_clients:
    #                 col_people.update_one({"_id": person.get("_id")}, {"$push" : {"utaEmployeeInfo.internalTeam.personRelationships": {"person": person2.get("_id"), "type": person2.get("type")}}})



    # if col_logs.count_documents({}) == 0:
    #     a = 1
    # else:
    #     a = list(col_logs.find().sort('batch_id', -1).limit(1))[0].get('batch_id') + 1
    # col_people.update_many({"variety_talent_id": {"$exists": True}}, {'$set': {'batch_id': a}})
    # lst_people = list(col_people.find({"variety_talent_id": {"$exists": True}}))
    # col_archives.insert_many(lst_people)
    # col_people.update_many({"variety_talent_id": {"$exists": True}}, {'$unset': {'batch_id': ""}})
    # col_logs.insert_one({'batch_id': a, 'dc_code': "variety merge", 'affected_number': len(lst_people), 'rollbacked': 'No',
    #                      'cleansing_ts': datetime.utcnow()})

    upsert_agency_relationalship()