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
    
    def response_invitation(self,data):
            return {
                "connection_id": data['connection_id'],
                "state": "invitation",
                "connectionURL":data['invitation_url']
            }
    
    def response_connection_webhook(self):
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