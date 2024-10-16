import json


class JsonModel(object):
    
    def tojson(self):
        return getdict(self)

class CreateInvitation(JsonModel):
    
    def __init__(self):
        self.connection_id = None
        self.invitation_url = None

        self.state= None
        self.invitation_key= None
        self.accept= None
        self.invitation_mode= None
        self.routing_state= None
        self.connection_id= None
        self.created_at= None
        self.their_role= None
        self.rfc23_state= None
        self.updated_at= None
        
    def setfromdic(self, data): 
        self.connection_id = data.get('connection_id', '')
        self.invitation_url = data.get('invitation_url', '')
        
        self.state= data.get('state', '')
        self.invitation_key= data.get('invitation_key', '')
        self.accept= data.get('accept', '')
        self.invitation_mode= data.get('invitation_mode', '')
        self.routing_state= data.get('routing_state', '')
        self.created_at= data.get('created_at', '')
        self.their_role= data.get('their_role', '')
        self.rfc23_state= data.get('rfc23_state', '')
        self.updated_at= data.get('updated_at', '')
    
    def response_issue_invitation(self,data):
            return {
                "connection_id": data['connection_id'],
                "state": "invitation",
                "connectionURL":data['invitation_url']
            }
    
    def response_issuance_webhook(self):
        return {
            "state": self.state,
            "invitation_key": self.invitation_key,
            "accept":self.accept,
            "invitation_mode": self.invitation_mode,
            "routing_state": self.routing_state,
            "connectionId": self.connection_id,
            "created_date": self.created_at,
            "their_role": self.their_role,
            "rfc23_state": self.rfc23_state,
            "updated_at": self.updated_at,
            "oobType": self.rfc23_state

            }

class IssuanceCredential(JsonModel):
    def __init__(self):
        # issuance model
        self.credential_exchange_id = None
        self.role = None
        self.created_at = None
        self.auto_offer = None
        self.schema_id = None
        self.auto_issue = None
        self.credential_offer_dict = None
        self.state = None
        self.credential_id = None
        

    def setfromdic(self, data):

        self.credential_definition_id = data.get('credential_definition_id', '')
        self.credential_exchange_id = data.get('credential_exchange_id', '')
        self.role = data.get('role', '')
        self.created_at = data.get('created_at', '')
        self.auto_offer = data.get('auto_offer', False)
        self.schema_id = data.get('schema_id', '')
        self.auto_issue = data.get('auto_issue', True)
        self.credential_offer_dict = data.get('credential_offer_dict', {})
        self.offers_attach = self.credential_offer_dict.get('offers~attach', [])
        self.connection_id = data.get('connection_id', '')
        self.state = data.get('state', '')
        self.credential_id = data.get('credential_exchange_id', '')


    def response_issuance(self):
        return {
            'credential_definition_id': self.credential_definition_id,
            'credential_exchange_id': self.credential_exchange_id,
            'role': self.role,
            'created_at': self.created_at,
            'auto_offer': self.auto_offer,
            'schema_id': self.schema_id,
            'auto_issue': self.auto_issue,
            'credential_offer_dict': {
                '@type': self.credential_offer_dict.get('@type', ''),
                '@id': self.credential_offer_dict.get('@id', ''),
                '~thread': self.credential_offer_dict.get('~thread', {}),
                'offers~attach': self.offers_attach
            }
        }

    def response_cred_def_id_schema_body(self,data_dict):
        connection_id = data_dict ['connection_id']
        cred_def_id = data_dict ['credentialDefinitionId']
        attributes = data_dict ['attributes']
        return {
            "auto_issue": True,
            "auto_remove": False, #set to false to preserve exchange records
            "comment": "string",
            "connection_id": connection_id,
            "cred_def_id": cred_def_id, 
            "credential_preview": {
                "@type": "issue-credential/1.0/credential-preview",
                "attributes": attributes
            },
            
            "trace": False
            }
    
    def response_issuance_payload(self):
        return {
            "state": self.state,
            "role": self.role,
            "created_at": self.created_at,
            "auto_offer": self.auto_offer,
            "schema_id": self.schema_id,
            "auto_issue": self.auto_issue,
            "credentialId": self.credential_id,
            "connectionId": self.connection_id,
            "credentialDefinitionId": self.credential_definition_id,
            }
    
