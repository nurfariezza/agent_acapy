import json

class JsonModel(object):
    
    def tojson(self):
        return getdict(self)
        
class Proof(JsonModel):
            
    def setfromdic(self, data):

        self.schema_id = data.get('schema_id', '')    
        self.comment = data.get('comment', '')
        self.name = data.get('name', '')
        self.non_revoked = data.get('non_revoked', '')
        self.to = data.get('to', '')
        self.nonce = data.get('nonce', '')
        self.requested_attributes = data.get('requested_attributes', '')
        self.additionalProp1 = data.get('additionalProp1', '')
        self.contactno = data.get('contactno', '')
        self.requested_predicates = data.get('requested_predicates', '')
        self.restrictions = data.get('restrictions', '')
        self.version = data.get('version', '')

        # proof verify####### 
        self.auto_present = data.get('auto_present', '')
        self.created_at = data.get('created_at', '')
        self.connection_id = data.get('connection_id', '')
        self.presentation_exchange_id = data.get('presentation_exchange_id', '')
        self.role = data.get('role', '')
        self.updated_at = data.get('updated_at', '')
        self.verified = data.get('verified', '')
        self.state = data.get('state', '')
        self.thread_id = data.get('thread_id', '')
        self.initiator = data.get('initiator', '')
        self.trace = data.get('trace', '')
        self.type = data.get('@type', '')
        self.base64 = data.get('base64', '')    
      
    
    def body_proof_sent(self,received_data): 
        attrvalue = len(received_data["proofAttributes"])
        datax = {} 

        for x in range(attrvalue):
            attribute_list = received_data["proofAttributes"][x]
            i = x + 1
            append_attribute = f"additionalProp{i}" 
            datax[append_attribute] = attribute_list 

        
        requested_attr= json.dumps(datax)

        data = {
        "comment": "string",
        "connection_id": received_data["connection_id"],
        "proof_request": {
            "name": "Proof request",
            "non_revoked": {
            "to": 1687422247
            },
            "nonce": "1234567890",
            "requested_attributes":json.loads(requested_attr),
            "requested_predicates": {},
            "version": "1.0"
        },
        "trace": False
        }

        return data


    def response_proof_sent(self):
        return {
            "auto_present": self.auto_present,
            "created_at": self.created_at,
            "role": self.role,
            "presentation_exchange_id": self.presentation_exchange_id,
            "connection_id": self.connection_id,
            "verified": self.verified,
            "updated_at": self.updated_at,
            "state": self.state,
            "thread_id": self.thread_id,
            "initiator": self.initiator,
            "trace": self.trace
        }

  


    def response_proof_verify_issuance(self):
        return  {
            "updated_at": self.updated_at,
            "presentation_request_dict": {
                "request_presentations~attach": [
                {
                    "mime-type": "application/json",
                    "data": {
                    }
                }
                ],
                "comment": self.comment
            },
            "auto_present": self.auto_present,
            "trace": self.trace,
            "role": self.role,
            "initiator": self.initiator,
            "created_at": self.created_at,
            "presentation_request": {
                "name": self.name,
                "non_revoked": {
                "to": self.to
                },
                "nonce": self.nonce,
                "requested_attributes": {
                "additionalProp1": {
                    "name": self.name,
                    "non_revoked": {
                    "to": self.to
                    },
                    "restrictions": self.restrictions
                }
                },
                "requested_predicates": self.requested_predicates,
                "version": self.version
            },
            "connectionId": self.connection_id,
            "state": self.state,
            "oobType": self.state,

       
            "connection_state": self.state,
            "presentation_exchange_id": self.presentation_exchange_id,
            "thread_id": self.thread_id


    }

    def response_proof_acked(self, proofattr):
        proof_attributes =[]
        proof_attributes_dict ={}

        for i in range(len(proofattr)):
            proof_attributes_dict ={
                "name": proofattr[f'additionalProp{i+1}']['name'],
                "credentialDefinitionTag" : proofattr[f'additionalProp{i+1}']['credentialDefinitionTag'],
                "credentialDefinitionId" : proofattr[f'additionalProp{i+1}']['credentialDefinitionId']
            }
            proof_attributes.append(proof_attributes_dict)

        return  {
            "updated_at": self.updated_at,
            "presentation_request_dict": {
                "request_presentations~attach": [
                {
                    "mime-type": "application/json",
                    "data": {
                    }
                }
                ],
                "comment": self.comment
            },
            "auto_present": self.auto_present,
            "trace": self.trace,
            "role": self.role,
            "initiator": self.initiator,
            "created_at": self.created_at,
            "presentation_request": {
                "name": self.name,
                "non_revoked": {
                "to": self.to
                },
                "nonce": self.nonce,
                "requested_attributes": {
                "additionalProp1": {
                    "name": self.name,
                    "non_revoked": {
                    "to": self.to
                    },
                    "restrictions": self.restrictions
                }
                },
                "requested_predicates": self.requested_predicates,
                "version": self.version
            },
            "proofId": self.presentation_exchange_id,
            "connectionId": self.connection_id,
            "state": self.state,
            "oobType": self.state,

       
            "presentation_exchange_id": self.presentation_exchange_id,
            "thread_id": self.thread_id,
            "proofAttributes":
                proof_attributes
    }

    def response_proof_verified(self,proofattr):

        return  {
            "updated_at": self.updated_at,
            "presentation_request_dict": {
                "request_presentations~attach": [
                {
                    "mime-type": "application/json",
                    "data": {
                    }
                }
                ],
                "comment": self.comment
            },
            "auto_present": self.auto_present,
            "trace": self.trace,
            "role": self.role,
            "initiator": self.initiator,
            "created_at": self.created_at,
            "presentation_request": {
                "name": self.name,
                "non_revoked": {
                "to": self.to
                },
                "nonce": self.nonce,
                "requested_attributes": {
                "additionalProp1": {
                    "name": self.name,
                    "non_revoked": {
                    "to": self.to
                    },
                    "restrictions": self.restrictions
                }
                },
                "requested_predicates": self.requested_predicates,
                "version": self.version
            },
            "proofId": self.presentation_exchange_id, #change from connection_id to pres_ex_id
            "connectionId": self.connection_id,
            "state": self.state,
            "oobType": self.state,
            "presentation_exchange_id": self.presentation_exchange_id,
            "thread_id": self.thread_id,
            "proofAttributes":
                proofattr

    }

    def response_proof_invitation(self,data):
            return {
                "connection_id": data['connection_id'],
                "state": "invitation",
                "connectionURL":data['invitation_url']
            }
    
    def body_present_proof(self, received_data):
        credential_id = received_data['credentialId']
        attributes = received_data['numAttributes']
        
        requested_attributes_dict = {}
        self_attested_attributes_dict = {}

        for i in range(attributes):
            requested_attributes_dict[f'additionalProp{i+1}'] = {
                    "cred_id": credential_id,
                    "revealed": True
            }
            self_attested_attributes_dict[f'additionalProp{i+1}'] = "self_attested_value"

        return {
                "requested_attributes": requested_attributes_dict,
                "requested_predicates": {},
                "self_attested_attributes": self_attested_attributes_dict,
                "trace": False
            }

   