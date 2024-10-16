from flask import Flask, jsonify, request 
from flask_restful import Resource, Api
from PIL import Image
import os,sys,flask,io,requests,qrcode,json, config
import qrcode.image.svg
from io import StringIO,BytesIO
from schema.schema_main import SchemaClass, HealthClass
from credentialdefinition.credentialdefinition_main import CredentialDefinitionClass
from connection.connection_main import InvitationClass
from issuance.issuance_main import IssuanceClass
from proof.proof_main import ProofClass, ProofVerifyClass
from wh.webhook_main import WebhookConnectionsClass, WebhookIssueCredentialClass,WebhookPresentProofClass
import logging
import asyncio
import nats
import re, json
import schedule
from nats.aio.client import Client as NATS
from apscheduler.schedulers.background import BackgroundScheduler
from nats_conf import NatsService

loop = asyncio.get_event_loop()
app = Flask(__name__)
api = Api(app)

logging.basicConfig(filename='acapy_api.log', level=logging.ERROR, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

api.add_resource(SchemaClass, '/schemas')
api.add_resource(NatsService, '/')
api.add_resource(HealthClass, '/get/')
api.add_resource(InvitationClass, '/create-invitation', '/accept')
api.add_resource(CredentialDefinitionClass, '/cred-def')
api.add_resource(IssuanceClass, '/issue-credential')
api.add_resource(ProofClass, '/presentproof-sendrequest')
api.add_resource(ProofVerifyClass, '/proof-verifypresentation')
api.add_resource(WebhookConnectionsClass, '/topic/connections/')
api.add_resource(WebhookIssueCredentialClass, '/topic/issue_credential/')
api.add_resource(WebhookPresentProofClass, '/topic/present_proof/')



def scheduled_api_call():
    with app.test_client() as client:
       client.get('/')

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(scheduled_api_call, 'interval', seconds=3)


if __name__ == "__main__":
    scheduler.start()
    app.run(host=config.ALLOWED_HOSTS,debug=False, port=config.PORT)
 
    
 
    

    
 
    
