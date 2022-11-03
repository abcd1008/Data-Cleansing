import pymongo
from datetime import datetime
from dateutil import parser
from bson.objectid import ObjectId


def upsert_new_talents_from_variety():
    count = 0
    for variety_talent_id in dic_variety_uta_talents.keys():
        uta_talent = {}
        variety_talent = dic_variety_uta_talents[variety_talent_id]

        if variety_talent:
            if variety_talent_id in dic_uta_talents.keys():
                uta_talent = dic_uta_talents[variety_talent_id]

            if variety_talent_id not in dic_uta_talents.keys():
                uta_talent["origin"] = "Variety Insert"
                uta_talent["variety_talent_id"] = variety_talent_id
                lst_uta_talent_agencies_ids = []
                if variety_talent.get("middle_name") == '' and variety_talent.get("last_name") == '':
                    talent_name = variety_talent.get("first_name")
                elif variety_talent.get("middle_name") == '' and variety_talent.get("last_name") != '':
                    talent_name = variety_talent.get("first_name") + " " + variety_talent.get("last_name")
                elif variety_talent.get("middle_name") != '' and variety_talent.get("last_name") == '':
                    talent_name = variety_talent.get("first_name") + " " + variety_talent.get("middle_name")
                else:
                    talent_name = variety_talent.get("first_name") + " " + variety_talent.get(
                        "middle_name") + " " + variety_talent.get("last_name")
            else:
                talent_name = uta_talent.get("name")
            uta_talent["name"] = talent_name
            if "legalName" not in uta_talent.keys() or ("legalName" in uta_talent.keys() and uta_talent["legalName"] == ""):
                uta_talent["legalName"] = talent_name

            # dic_internalTeam = {}
            # lst_internal_team = []
            # if "internalTeam" in uta_talent.keys() and len(uta_talent.get("internalTeam")) > 0:
            #     lst_internal_team = uta_talent.get("internalTeam")
            #     for internalTeam_agent in lst_internal_team:
            #         dic_internalTeam[internalTeam_agent["utaEmployee"]] = internalTeam_agent
            # else:
            #     lst_internal_team = []
            # if "agencies" in variety_talent.keys() and len(variety_talent.get("agencies")) > 0:
            #     lst_variety_talent_agencies = variety_talent.get("agencies")
            #     for variety_talent_agencies in lst_variety_talent_agencies:
            #         if variety_talent_agencies["company_id"] == "10039" and "agents" in variety_talent_agencies.keys():
            #             lst_variety_talent_agents = variety_talent_agencies.get("agents")
            #             for variety_talent_agent in lst_variety_talent_agents:
            #                 if "point_agent" in variety_talent_agent and variety_talent_agent.get(
            #                         "point_agent") == "Yes":
            #                     agent_type = "Point Agent"
            #                 else:
            #                     agent_type = "Agent"
            #                 if variety_talent_agent.get("first_name") + " " + variety_talent_agent.get(
            #                         "last_name") in dic_uta_people_not_talents.keys():
            #                     dic_internalTeam[dic_uta_people_not_talents[
            #                         variety_talent_agent.get("first_name") + " " + variety_talent_agent.get(
            #                             "last_name")].get("_id")] = \
            #                         {"utaEmployee": dic_uta_people_not_talents[
            #                             variety_talent_agent.get("first_name") + " " + variety_talent_agent.get(
            #                                 "last_name")].get("_id"), \
            #                          "type": agent_type, \
            #                          "createdAt": datetime.utcnow()}
            #                 else:
            #                     uta_employee = dic_variety_employee_contacts[variety_talent_agent.get("employee_id")]
            #                     uta_employee["variety_employee_id"] = uta_employee.pop("employee_id")
            #                     uta_employee["type"] = "Employee"
            #                     uta_employee["origin"] = "Variety Insert"
            #                     uta_employee["updateAt"] = datetime.utcnow()
            #                     uta_employee["name"] = variety_talent_agent.get(
            #                         "first_name") + " " + variety_talent_agent.get("last_name")
            #                     uta_employee["hasClients"] = True
            #                     uta_employee["vocations"] = ["Agent"]
            #                     doc = col_people.insert_one(uta_employee)
            #                     id = doc.inserted_id
            #                     uta_employee["_id"] = id
            #                     dic_uta_people_not_talents[uta_employee["name"]] = uta_employee
            #
            #                     dic_internalTeam[id] = {"utaEmployee": id, "type": agent_type,
            #                                             "createdAt": datetime.utcnow()}
            #
            # lst_internal_team = [dic_internalTeam[key] for key in dic_internalTeam.keys()]
            # for internal_team in lst_internal_team:
            #     if internal_team.get("type") == "Point Agent":
            #         tmp_internal_team = internal_team
            #         lst_internal_team.remove(internal_team)
            #         lst_internal_team.insert(0, tmp_internal_team)
            # uta_talent["internalTeam"] = lst_internal_team

            # obj_external_team = {}
            # if "externalTeam" in uta_talent.keys():
            #     obj_external_team = uta_talent.get("externalTeam")
            # if "personRelationships" in obj_external_team.keys():
            #     lst_external_team_people = [attorney.get("people") for attorney in
            #                                 obj_external_team.get("personRelationships")]
            # else:
            #     lst_external_team_people = []
            #     obj_external_team["personRelationships"] = []
            # lst_law_firms = uta_talent["law_firms"]
            # for law_firm in lst_law_firms:
            #     if "lawfirms" in law_firm:
            #         for attorney in law_firm.get("lawfirms"):
            #             attorney_name = attorney.get("first_name") + " " + attorney.get("last_name")
            #             if attorney_name in dic_uta_people_not_talents.keys() and dic_uta_people_not_talents[
            #                 attorney_name] not in lst_external_team_people:
            #                 obj_external_team.get("personRelationships").append(
            #                     {"people": dic_uta_people_not_talents[attorney_name].get("_id"), "type": "Attorney",
            #                      "createdAt": datetime.utcnow()})
            # uta_talent["externalTeam"] = obj_external_team
            #
            # obj_external_team = {}
            # if "externalTeam" in uta_talent.keys():
            #     obj_external_team = uta_talent.get("externalTeam")
            # if "personRelationships" in obj_external_team.keys():
            #     lst_external_team_people = [attorney.get("people") for attorney in
            #                                 obj_external_team.get("personRelationships")]
            # else:
            #     lst_external_team_people = []
            #     obj_external_team["personRelationships"] = []
            # lst_managements = uta_talent["managements"]
            # for management in lst_managements:
            #     if "managers" in management:
            #         for manager in management.get("managers"):
            #             manager_name = manager.get("first_name") + " " + manager.get("last_name")
            #             if manager_name in dic_uta_people_not_talents.keys() and dic_uta_people_not_talents[
            #                 manager_name] not in lst_external_team_people:
            #                 obj_external_team.get("personRelationships").append(
            #                     {"people": dic_uta_people_not_talents[manager_name].get("_id"),
            #                      "type": "Personal Manager", "createdAt": datetime.utcnow()})
            # uta_talent["externalTeam"] = obj_external_team
            #
            # obj_external_team = {}
            # if "externalTeam" in uta_talent.keys():
            #     obj_external_team = uta_talent.get("externalTeam")
            # if "personRelationships" in obj_external_team.keys():
            #     lst_external_team_people = [publicist.get("people") for publicist in
            #                                 obj_external_team.get("personRelationships")]
            # else:
            #     lst_external_team_people = []
            #     obj_external_team["personRelationships"] = []
            # lst_publicists = uta_talent["publicists"]
            # for publicist in lst_publicists:
            #     if "publicist" in publicist:
            #         for publicist in publicist.get("publicist"):
            #             publicist_name = publicist.get("first_name") + " " + publicist.get("last_name")
            #             if publicist_name in dic_uta_people_not_talents.keys() and dic_uta_people_not_talents[
            #                 publicist_name] not in lst_external_team_people:
            #                 obj_external_team.get("personRelationships").append(
            #                     {"people": dic_uta_people_not_talents[publicist_name].get("_id"), "type": "Publicist",
            #                      "createdAt": datetime.utcnow()})
            # uta_talent["externalTeam"] = obj_external_team

            if "lgbtq" in variety_talent.keys() and variety_talent.get("lgbtq") != "":
                if variety_talent.get("lgbtq") == "Y":
                    uta_talent["lgbtq"] = "Yes"
                elif variety_talent.get("lgbtq") == "N":
                    uta_talent["lgbtq"] = "No"

            if "ethnicity_new" in variety_talent.keys() and variety_talent.get("ethnicity_new") != "":
                if variety_talent.get("ethnicity_new") == "2+ Race":
                    uta_talent["ethnicities"] = variety_talent.get("talent_2_ethnicities")
                else:
                    uta_talent["ethnicities"] = variety_talent.get("ethnicity_new")

            if "social_media" in variety_talent.keys() and isinstance(variety_talent.get("social_media"), dict) and len(
                    variety_talent.get("social_media")) > 0:
                # uta_talent["social_network"] = variety_talent.get("social_media")
                if "social" in uta_talent.keys() and isinstance(uta_talent["social"], list):
                    lst_social = uta_talent["social"]
                else:
                    lst_social = []
                dic_social = {}
                if len(lst_social) > 0:
                    for socialnetwork in lst_social:
                        dic_social[socialnetwork.get("network")] = socialnetwork
                if len(dic_social.keys()) > 0:
                    lst_social = [social for social in dic_social.values()]
                for network in variety_talent["social_media"].keys():
                    if network not in dic_social.keys() and variety_talent["social_media"].get(network) != "":
                        lst_social.append({"network": network, "url": variety_talent["social_media"].get(network)})
                    # if network in dic_social.keys() and variety_talent["social_media"].get(network) != "":
                    #     lst_social.append({"network": network, "url": variety_talent["social_media"].get(network)})
                for social_item in lst_social:
                    if social_item.get("network") == "twitter" and social_item["url"].startswith("@"):
                        social_item["url"] = social_item["url"].replace("@", "https://twitter.com/")
                    if social_item.get(
                            "network") == "twitter" and "twitter_followers" in variety_talent.keys() and variety_talent.get(
                            "twitter_followers") != "":
                        social_item["web_followers"] = variety_talent.get("twitter_followers").replace(",", "")
                        social_item["followers"] = int(variety_talent.get("twitter_followers").replace(",", ""))
                    if social_item.get(
                            "network") == "facebook" and "facebook_likes" in variety_talent.keys() and variety_talent.get(
                            "facebook_likes") != "":
                        social_item["web_followers"] = variety_talent.get("facebook_likes").replace(",", "")
                        social_item["followers"] = int(variety_talent.get("facebook_likes").replace(",", ""))
                    if social_item.get("network") == "webpage":
                        if "url" in social_item.keys():
                            uta_talent["artistWebsite"] = social_item["url"]
                        lst_social.remove(social_item)
                uta_talent["social"] = lst_social

            if "birthdate" in variety_talent.keys() and variety_talent.get("birthdate") != "":
                uta_talent["birthday"] = parser.parse(variety_talent.get("birthdate"))

            if "country_of_origin" in variety_talent.keys() and variety_talent.get("country_of_origin") != "":
                uta_talent["originCountry"] = variety_talent.get("country_of_origin")
                uta_talent["nationalities"] = [variety_talent.get("country_of_origin")]

            if "talent_photo_high_res_source" in variety_talent.keys() and variety_talent.get(
                    "talent_photo_high_res_source") != "":
                uta_talent["talent_photo_high_res_source"] = variety_talent.get("talent_photo_high_res_source")

            if "talent_photo_high_res" in variety_talent.keys() and variety_talent.get(
                    "talent_photo_high_res") != "":
                uta_talent["profile_pic"] = variety_talent.get("talent_photo_high_res")

            if "gender_new" in variety_talent.keys() and variety_talent.get("gender_new") != "":
                uta_talent["gender"] = variety_talent.get("gender_new")

            if "languages" in variety_talent.keys() and variety_talent.get("languages") != "":
                uta_talent["primaryLanguage"] = variety_talent.get("languages")

            if "modified_date" in variety_talent.keys() and variety_talent.get("modified_date") != "":
                uta_talent["variety_update_at"] = parser.parse(variety_talent.get("modified_date"))

            vocations = []
            if "role" in uta_talent.keys() and uta_talent["role"] != "":
                if "vocations" in uta_talent.keys():
                    vocations = uta_talent["vocations"]
            if "role" in uta_talent.keys() and uta_talent["role"] not in set(vocations):
                vocations.append(uta_talent["role"])
            uta_talent["vocations"] = vocations

            uta_talent["type"] = "Client"
            uta_talent["updateAt"] = datetime.utcnow()
            uta_talent["source"] = "Variety"

            # lst_publicists = variety_talent.get("publicists")
            # for publicist in lst_publicists:
            #     publicist["variety_company_id"] = publicist.pop("company_id")
            #     for publicist_people in publicist.get("publicist"):
            #         publicist_people["variety_employee_id"] = publicist_people.pop("employee_id")
            # uta_talent["publicists"] = lst_publicists
            #
            # lst_law_firms = variety_talent.get("law_firms")
            # for law_firm in lst_law_firms:
            #     law_firm["variety_company_id"] = law_firm.pop("company_id")
            #     for attorney in law_firm.get("lawfirms"):
            #         attorney["variety_employee_id"] = attorney.pop("employee_id")
            # uta_talent["law_firms"] = lst_law_firms
            #
            # lst_managements = variety_talent.get("managements")
            # for management in lst_managements:
            #     management["variety_company_id"] = management.pop("company_id")
            #     for manager in management.get("managers"):
            #         manager["variety_employee_id"] = manager.pop("employee_id")
            # uta_talent["managements"] = lst_managements


            if "_id" in uta_talent.keys():
                col_people.update_one({"_id": uta_talent["_id"]}, {"$set": uta_talent})
            else:
                col_people.insert_one(uta_talent)

            # col_people.insert_one(
            #     {"name": talent_name,
            #      "social_network": variety_talent.get("social_media"),
            #      "originCountry": variety_talent.get("country_of_origin"),
            #      "ethnicities": ethnicities,
            #      "talent_photo_high_res_source": variety_talent.get("talent_photo_high_res_source"),
            #      "talent_photo_high_res": variety_talent.get("talent_photo_high_res"),
            #      "lgbtq": lgbtq,
            #      "gender": variety_talent.get("gender_new"),
            #      "variety_talent_id": variety_talent.get("talent_id"),
            #      "origin": "Variety Insert",
            #      "type": "Client",
            #      "primaryLanguage": variety_talent.get("languages"),
            #      "publicists": variety_talent.get("publicists"),
            #      "law_firms": variety_talent.get("law_firms")})
            # if variety_talent.get("birthdate") is not None and variety_talent.get("birthdate") != "":
            #     col_people.update_one({"_id": uta_talent.get("_id")},
            #                           {"$set": {"birthday": parser.parse(variety_talent.get("birthdate"))}})
            count = count + 1
            print(count)


if __name__ == '__main__':
    # mongo_connection_uta_stage = "mongodb+srv://cluster0.shzhn.mongodb.net/admin?replicaSet=atlas-y7qbzb-shard-0&readPreference=primary&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1"
    # client_uta = pymongo.MongoClient(mongo_connection_uta_stage)

    # db_uta = client_uta["uta"]
    db_uta = client_uta["test"]
    col_people = db_uta["people"]
    col_variety_talents = db_uta["variety_talents"]
    col_logs = db_uta['dc_logs']
    # col_archives = db_uta["people_archives"]
    col_variety_talent_contacts = db_uta["variety_talent_contacts"]
    col_variety_companies = db_uta["variety_companies"]
    col_variety_employee_contacts = db_uta["variety_employee_contacts"]
    col_variety_company_contacts = db_uta["variety_company_contacts"]
    col_uta_companies = db_uta["companies"]
    qry_variety = {"agencies.company_id": "10039"}

    cur_variety_uta_talents = col_variety_talents.find(qry_variety).sort("modified_date", pymongo.ASCENDING)
    dic_variety_uta_talents = {}
    for variety_uta_talent in cur_variety_uta_talents:
        dic_variety_uta_talents[variety_uta_talent.get("talent_id")] = variety_uta_talent

    cur_uta_talents = col_people.find({"variety_talent_id": {"$exists": True}})
    dic_uta_talents = {}
    for uta_talent in cur_uta_talents:
        dic_uta_talents[uta_talent.get("variety_talent_id")] = uta_talent

    cur_uta_people_not_talents = col_people.find({"$or": [{"type": "Employee"}, {"type": "Industry Contact"}]},
                                                 {"name": 1})
    dic_uta_people_not_talents = {}
    for uta_people_not_talent in cur_uta_people_not_talents:
        dic_uta_people_not_talents[uta_people_not_talent.get("name")] = uta_people_not_talent

    cur_variety_uta_talent_contacts = col_variety_talent_contacts.find()
    dic_variety_uta_talent_contacts = {}
    for variety_uta_talent_contact in cur_variety_uta_talent_contacts:
        dic_variety_uta_talent_contacts[variety_uta_talent_contact.get("talent_id")] = variety_uta_talent_contact

    cur_uta_companies = col_uta_companies.find({}, {"name": 1})
    dic_uta_companies = {}
    for uta_company in cur_uta_companies:
        dic_uta_companies[uta_company.get("name")] = uta_company

    lst_variety_companies = cur_variety_companies = col_variety_companies.find()
    dic_variety_companies = {}
    for variety_company in lst_variety_companies:
        dic_variety_companies[variety_company.get("company_name")] = variety_company
    dic_variety_companies_byid = {}
    for variety_company_byid in lst_variety_companies:
        dic_variety_companies_byid[variety_company_byid.get("company_id")] = variety_company

    cur_variety_company_contacts = col_variety_company_contacts.find({}, {"_id": 0})
    dic_variety_company_contacts = {}
    for variety_company_contact in cur_variety_company_contacts:
        dic_variety_company_contacts[variety_company_contact.get("company_id")] = variety_company_contact

    cur_variety_employee_contacts = col_variety_employee_contacts.find({}, {"_id": 0})
    dic_variety_employee_contacts = {}
    for variety_employee_contact in cur_variety_employee_contacts:
        dic_variety_employee_contacts[variety_employee_contact.get("employee_id")] = variety_employee_contact

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

    upsert_new_talents_from_variety()
