from pymongo import MongoClient
from config import Config
import json

client = MongoClient(Config.MONGO_URI)

db = client["collegeDB"]
collection = db["results"]


def execute_query(query_string):

    try:

        query = json.loads(query_string)

        result = list(collection.find(query))

        for record in result:

            record["_id"] = str(record["_id"])

            if record["grade"] == "D":
                record["status"] = "Fail"
            else:
                record["status"] = "Pass"

        return result

    except Exception as e:
        return {"error": str(e)}