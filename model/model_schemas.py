import json

class JsonModel(object):
    
    def tojson(self):
        return getdict(self)


class Schema(JsonModel):
    
    def __init__(self):
        self.schema_id = None
        self.schema = None
        self.id = None
        self.name = None
        self.ver = None


    def response_schema(self,resp):
        return {
            "schema_id": resp["schema_id"],
            "name": resp["schema"]["name"],
            "version": resp["schema"]["version"],
            "attrNames": resp["schema"]["attrNames"],
            "seqNo": resp["schema"]["seqNo"]
           
        }

    def create_schema_body(self, resp):

        return {
                "attributes": resp["data"]["attributes"],
                "schema_name": resp["data"]["name"],
                "schema_version": resp["data"]["version"]
            }

    def response_fetch_schema(self,resp):
        return {
            "schemaId": resp["schema"]["id"],
            "name": resp["schema"]["name"],
            "version": resp["schema"]["ver"],
            "attrNames": resp["schema"]["attrNames"],
            "seqNo": resp["schema"]["seqNo"]
        }
      
