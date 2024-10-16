import logging
from flask import request 
from flask_restful import Resource
from model import model_issuance, model_proof, model_connection
import json
from issuance.issuance_main import IssuanceClass
from proof.proof_main import ProofClass, ProofVerifyClass
import json
import asyncio
from nats_conf import NatsService


class WebhookConnectionsClass(Resource):

    def post(self):
        payload = request.json  
        if payload is not None:
            connection_id = payload.get('connection_id')
            state = payload.get('state')
            print("=======WebhookConnections========")
            print("State: ", state)

            topic = "event.credential.connection.id."+connection_id
            connection_model = model_connection.CreateInvitation()
            connection_model.setfromdic(payload)
            resp_payload = connection_model.response_connection_webhook()

            asyncio.run(NatsService.callback(topic=topic, msg=resp_payload))

            if state == 'active':
                
                target_key = connection_id
                with open('issuance.json', 'r') as file:
                    data = json.load(file)
                
                extracted_value = None

                for item in data:
                    if target_key in item:                       
                        extracted_value = item[target_key]
                        if extracted_value is not None:
                            extracted_value["connection_id"]= target_key
                            updated_json_str = json.dumps(extracted_value, indent=4)

                            IssuanceClass.issue_cred_webhook(self, updated_json_str)
                           
                            key_to_remove = target_key
                            json_list = [item_n for item_n in data if key_to_remove not in item_n]
                            with open('issuance.json', "w") as outfile:
                                json.dump(json_list, outfile, indent=6)
                        break

                with open('proof.json', 'r') as file:
                    data = json.load(file)
                
                extracted_value = None

                for item in data:
                    if target_key in item:                       
                        extracted_value = item[target_key]
                        if extracted_value is not None:
                            extracted_value["connection_id"]= target_key
                            updated_json_str = json.dumps(extracted_value, indent=4)
                            ProofClass.request_proof_webhook(updated_json_str)

                        break
            return payload, 200
        return '', 204  
    

class WebhookIssueCredentialClass(Resource):

    def post(self):
        payload = request.json
        if payload is not None:
            connection_id = payload.get('connection_id')
            state = payload.get('state')
            role = payload.get('role')
            credential_exchange_id = payload.get('credential_exchange_id')
            print("=======WebhookIssueCredential========")
            topic = "event.credential.issuance.id."+connection_id
            print("State: ", state)
            print("Role: ", role)

            issuance_model = model_issuance.IssuanceCredential()
            issuance_model.setfromdic(payload)
            resp_payload = issuance_model.response_issuance_payload()
            
            asyncio.run(NatsService.callback(topic=topic, msg=resp_payload))
            
            if state == 'offer_received':
                IssuanceClass.accept_credential(credential_exchange_id)

            elif state == 'credential_received':
                IssuanceClass.store_credential_wallet(credential_exchange_id)

            return resp_payload, 200
        return '', 204 


class WebhookPresentProofClass(Resource):

    def post(self):
        payload = request.json  
        if payload is not None:
            connection_id = payload.get('connection_id')
            credential_definition_id = payload["presentation_request"]["requested_attributes"]["additionalProp1"]["credentialDefinitionId"]
            state = payload.get('state')
            role = payload.get('role')
            presentation_exchange_id = payload.get('presentation_exchange_id')

            proof_model = model_proof.Proof()
            proof_model.setfromdic(payload)
            print("=======WebhookPresentProof========")
            print("State: ", state)
            print("Role: ", role)

            if state == "request_sent":
                topic = "event.proof.connection.id."+connection_id
                resp_proof = proof_model.response_proof_verify_issuance()

                asyncio.run(NatsService.callback(topic=topic, msg=resp_proof))

            elif state == 'request_received':
                req_attr = payload['presentation_request']['requested_attributes']
                req_num_attr = len(req_attr)
                ProofClass.present_proof_webhook(presentation_exchange_id, credential_definition_id, req_num_attr)
                
            elif state == "presentation_received":
                ProofVerifyClass.verify_proof_webhook(presentation_exchange_id)

            elif state == "presentation_acked":
                topic = "event.proof.generate.id."+presentation_exchange_id
                
                proof_attr = payload["presentation_request"]["requested_attributes"]
                resp_proof = proof_model.response_proof_acked(proof_attr)

                asyncio.run(NatsService.callback(topic=topic, msg=resp_proof))
                
            elif state == "verified":
                topic = "event.proof.generate.id."+presentation_exchange_id
                target_key = connection_id
                with open('proof.json', 'r') as file:
                    data = json.load(file)
                
                extracted_value = None

                for item in data:
                    if target_key in item:
                       
                        extracted_value = item[target_key]
                        proofattr = extracted_value['proofAttributes']
                        resp_proof = proof_model.response_proof_verified(proofattr)

                        if extracted_value is not None:

                            key_to_remove = target_key
                            json_list = [item_n for item_n in data if key_to_remove not in item_n]
                    
                            with open('proof.json', "w") as outfile:
                                json.dump(json_list, outfile, indent=6)

                        break
                asyncio.run(NatsService.callback(topic=topic, msg=resp_proof))
            
            return payload, 200
        return '', 204 
