from flask import jsonify
from flask_restful import Resource
import json, config
from schema.schema_main import SchemaClass
from credentialdefinition.credentialdefinition_main import CredentialDefinitionClass
from issuance.issuance_main import IssuanceClass
from connection.connection_main import InvitationClass
from proof.proof_main import ProofClass
import asyncio, json
from nats.aio.client import Client as NATS

loop = asyncio.get_event_loop()


class NatsService(Resource):
    is_nats_connected = False
    nats_client = None
    
    def __init__(self):
        self.nats_client = NATS()

    async def nats_connect(self):
        nc = self.nats_client
        
        await nc.connect(servers=["nats://localhost:4222"])

        AGENT_TYPE = config.AGENT_TYPE
       
        await nc.subscribe(AGENT_TYPE+".schemas.create", cb=self.cb)
        await nc.subscribe(AGENT_TYPE+".schemas.fetch.id",cb=self.cb)
        await nc.subscribe(AGENT_TYPE+".credDef.create",cb=self.cb)
        await nc.subscribe(AGENT_TYPE+".credDef.fetch.id",cb=self.cb) 
        await nc.subscribe(AGENT_TYPE+".credential.issue.oob",cb=self.cb)
        await nc.subscribe(AGENT_TYPE+".proof.generate.oob",cb=self.cb)
        await nc.subscribe(AGENT_TYPE+".credential.fetch.id",cb=self.cb)
        await nc.subscribe(AGENT_TYPE+".proof.fetch.id",cb=self.cb)
        return nc

    async def cb(self, msg):  
        subject = msg.subject
        data = msg.data.decode('utf-8')
        nc = self.nats_client
        AGENT_TYPE = config.AGENT_TYPE

        
        resp_message = {
            'subject': subject,
            'data': data
        } 
        message_json = json.dumps(resp_message)
        pre_message = resp_message

        if subject == AGENT_TYPE+".schemas.create":
            resp = SchemaClass.createschema(self, message_json)
        elif (subject == AGENT_TYPE+".schemas.fetch.id"):
            resp = SchemaClass.getschema(self, message_json)
        elif (subject == AGENT_TYPE+".credDef.create"):
            resp = CredentialDefinitionClass.createcreddef(self, message_json)        
        elif (subject == AGENT_TYPE+".credDef.fetch.id"):
            resp = CredentialDefinitionClass.getcreddef(self, message_json)
        elif (subject == AGENT_TYPE+".credential.issue.oob"):
            resp = InvitationClass.issueinvitation(self,pre_message)
        elif (subject == AGENT_TYPE+".proof.generate.oob"):
            resp = InvitationClass.proofinvitation(self,message_json)
        elif (subject == AGENT_TYPE+".credential.fetch.id"):
            resp = IssuanceClass.getissuedcredential(self, message_json)
        elif (subject == AGENT_TYPE+".proof.fetch.id"):
             resp = ProofClass.getproofdetails(self, message_json)
        else:
            resp = pre_message


        json_data = resp
        json_string = json.dumps(json_data)
        json_bytes = json_string.encode('utf-8')
        try:
            await msg.respond(json_bytes)
            
        except Exception as e:
            print("An error occurred:", e)

        while True:
            await nc.flush()
            return 


    def get(self):
        if not NatsService.is_nats_connected:
            loop.run_until_complete(self.nats_connect())
            NatsService.is_nats_connected = True
        else:
            loop.run_until_complete(self.get_existing_nats_client())

        return jsonify({"result": "Connected"})
    
    async def get_existing_nats_client(self):
        if NatsService.is_nats_connected:
            
            return NatsService.nats_client
        return None


    async def callback(topic, msg):

        nc = NATS()
        await nc.connect(servers=["nats://localhost:4222"])
        payload = json.dumps(msg).encode('utf-8')
        sub = await nc.subscribe(topic)
        await nc.publish(topic, payload)

        await sub.next_msg()
        await nc.close()
        print('Message Published')

