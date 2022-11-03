import pymongo
from datetime import datetime
from dateutil import parser


if __name__ == '__main__':
    # mongo_connection_uta_stage = "mongodb+srv://cluster0.shzhn.mongodb.net/admin?replicaSet=atlas-y7qbzb-shard-0&readPreference=primary&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1"
    # client_uta = pymongo.MongoClient(mongo_connection_uta_stage)

    mongo_connection_uta_prod = "mongodb+srv://cluster0.njccd.azure.mongodb.net/?replicaSet=Cluster0-shard-0&readPreference=primary&serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1"
    client_uta = pymongo.MongoClient(mongo_connection_uta_prod)
    db_uta = client_uta["uta"]
    # db_uta = client_uta["test"]
    col_people = db_uta["people"]
    col_variety = db_uta["variety_talents"]
    qry_uta_client = {"type": "Client"}
    lst_uta_talent = list(col_people.find(qry_uta_client, {"social": 1}))
    # lst_uta_talent = list(col_people.find(qry_uta_client, {"name": 1, "birthday": 1, "contacts": 1, "social": 1}))
    # qry_variety = {"agencies.company_id": "10039"}
    qry_variety = {}
    lst_variety_talent = list(col_variety.find(qry_variety, {"talent_id":1, "social_media":1}))
    dic_uta_talent_by_instagram_id = {}
    dic_uta_talent_by_facebook_id = {}
    dic_uta_talent_by_twitter_id = {}

    #instagram
    count = 0
    for uta_talent in lst_uta_talent:
        socials = []
        if "social" in uta_talent.keys() and uta_talent["social"] is not None:
            socials = uta_talent["social"]
        for social in socials:
            if social.get("network") == "instagram":
                instagram_url = social.get("url")
                instagram_url = instagram_url.removeprefix("https://www.instagram.com/")
                instagram_url = instagram_url.removeprefix("http://www.instagram.com/")
                instagram_id = instagram_url.removesuffix("/")
                dic_uta_talent_by_instagram_id[instagram_id] = uta_talent

    for variety_talent in lst_variety_talent:
        social_medias = []
        if "social_media" in variety_talent.keys() and variety_talent["social_media"] is not None:
            social_medias = variety_talent["social_media"]

        if isinstance(social_medias, dict):
            variety_instagram_id = ""
            if "instagram" in social_medias.keys():
                variety_instagram_url = social_medias["instagram"]
                variety_instagram_url = variety_instagram_url.removeprefix("https://www.instagram.com/")
                variety_instagram_url = variety_instagram_url.removeprefix("http://www.instagram.com/")
                variety_instagram_id = variety_instagram_url.removesuffix("/")
            if variety_instagram_id in dic_uta_talent_by_instagram_id.keys() and variety_instagram_id != "":
                uta_talent_matched = dic_uta_talent_by_instagram_id.get(variety_instagram_id)
                # results = col_people.update_one({"_id": uta_talent_matched.get("_id")}, {"$set": {"variety_talent_id": variety_talent.get("talent_id")}})
                count = count + 1
    print("instagram" + str(count))

    # facebook
    count = 0
    for uta_talent in lst_uta_talent:
        socials = []
        if "social" in uta_talent.keys() and uta_talent["social"] is not None:
            socials = uta_talent["social"]
        for social in socials:
            if social.get("network") == "facebook":
                social_url = social.get("url")
                social_url = social_url.removeprefix("https://www.facebook.com/")
                social_url = social_url.removeprefix("http://www.facebook.com/")
                social_id = social_url.removesuffix("/")
                dic_uta_talent_by_facebook_id[social_id] = uta_talent

    for variety_talent in lst_variety_talent:
        social_medias = []
        if "social_media" in variety_talent.keys() and variety_talent["social_media"] is not None:
            social_medias = variety_talent["social_media"]

        if isinstance(social_medias, dict):
            variety_instagram_id = ""
            if "facebook" in social_medias.keys():
                variety_social_url = social_medias["facebook"]
                variety_social_url = variety_social_url.removeprefix("https://www.facebook.com/")
                variety_social_url = variety_social_url.removeprefix("http://www.facebook.com/")
                variety_social_id = variety_social_url.removesuffix("/")
            if variety_social_id in dic_uta_talent_by_facebook_id.keys() and variety_social_id != "":
                uta_talent_matched = dic_uta_talent_by_facebook_id.get(variety_social_id)
                # results = col_people.update_one({"_id": uta_talent_matched.get("_id")},
                #                                 {"$set": {"variety_talent_id": variety_talent.get("talent_id")}})
                count = count + 1
    print("facebook" + str(count))

    # twitter
    count = 0
    for uta_talent in lst_uta_talent:
        socials = []
        if "social" in uta_talent.keys() and uta_talent["social"] is not None:
            socials = uta_talent["social"]
        for social in socials:
            if social.get("network") == "twitter":
                social_url = social.get("url")
                social_url = social_url.removeprefix("https://twitter.com/")
                social_url = social_url.removeprefix("http://twitter.com/")
                social_id = social_url.removesuffix("/")
                dic_uta_talent_by_twitter_id[social_id] = uta_talent

    for variety_talent in lst_variety_talent:
        social_medias = []
        if "social_media" in variety_talent.keys() and variety_talent["social_media"] is not None:
            social_medias = variety_talent["social_media"]

        if isinstance(social_medias, dict):
            variety_instagram_id = ""
            if "twitter" in social_medias.keys():
                variety_social_url = social_medias["twitter"]
                variety_social_url = variety_social_url.removeprefix("@")
                variety_social_id = variety_social_url.removesuffix("/")
            if variety_social_id in dic_uta_talent_by_twitter_id.keys() and variety_social_id != "":
                uta_talent_matched = dic_uta_talent_by_twitter_id.get(variety_social_id)
                # results = col_people.update_one({"_id": uta_talent_matched.get("_id")},
                #                                 {"$set": {"variety_talent_id": variety_talent.get("talent_id")}})
                count = count + 1

    print("twitter" + str(count))
