import json

class JsonModel(object):
    
    def tojson(self):
        return getdict(self)

class Credential(JsonModel):
    
    def setfromdic(self, data):
        self.cred_def_id = data.get('cred_def_id', '')
        self.attributes = data.get('attributes', '')
        self.auto_remove = data.get('auto_remove', '')
        self.credential_proposal = data.get('credential_proposal', '')
        self.state = data.get('state', '')
        self.comment = data.get('comment', '')
        self.cred_exc_id = data.get('cred_exc_id', '')
        self.credential_definition_id = data.get('credential_definition_id', '')

        credential_definition = data.get('credential_definition', {})
        self.ver = credential_definition.get('ver', '')
        self.id = credential_definition.get('id', '')
        self.schemaId = credential_definition.get('schemaId', '')
        self.type = credential_definition.get('type', '')
        self.tag = credential_definition.get('tag', '')

        value = credential_definition.get('value', {})
        primary = value.get('primary', {})
        self.primary = {
            "n": primary.get('n', ''),
            "s": primary.get('s', ''),
            "r": {
                "contactno": primary.get('r', {}).get('contactno', ''),
                "master_secret": primary.get('r', {}).get('master_secret', ''),
                "name": primary.get('r', {}).get('name', '')
            },
            "rctxt": primary.get('rctxt', ''),
            "z": primary.get('z', '')
        }

        revocation = value.get('revocation', {})
        self.revocation = {
            "g": revocation.get('g', ''),
            "g_dash": revocation.get('g_dash', ''),
            "h": revocation.get('h', ''),
            "h0": revocation.get('h0', ''),
            "h1": revocation.get('h1', ''),
            "h2": revocation.get('h2', ''),
            "htilde": revocation.get('htilde', ''),
            "h_cap": revocation.get('h_cap', ''),
            "u": revocation.get('u', ''),
            "pk": revocation.get('pk', ''),
            "y": revocation.get('y', '')
        }


    def schema_body_cred_definition(self,nested_data):
        schema_id = nested_data["data"]["schemaId"]
        support_revocation = nested_data["data"]["supportRevocation"]
        tag = nested_data["data"]["tag"]

        return {

            "schema_id": schema_id,
            "revocation_registry_size": 900,
            "support_revocation": False,
            "tag": tag
        }

            
    def response_cred_def_id(self,resp):
        return {
            "credential_definition_id": resp["credential_definition_id"]
        }
        


    def resp_cred_def_id(self,resp):
        return {
           
            "org_did": '',
            "name": '',
            "tag": resp["credential_definition"]["tag"],
            "schemaId":resp["credential_definition"]["schemaId"],
            "cred_def_id":resp["credential_definition"]["id"],
            "schema_id":resp["credential_definition"]["schemaId"],
            "_id": resp["credential_definition"]["id"],
            "ver": resp["credential_definition"]["ver"]
           
        }

    def resp_to_dict_cred_def_id_ex(self):
            return {
            
                    "org_did": '',
                    "name": '',
                    "tag": self.tag,
                    "schemaId":self.schemaId,
                    "cred_def_id":self.id,
                    "schema_id":self.schemaId,
                    "_id": self.id,
                    "ver": self.ver
            
        }



