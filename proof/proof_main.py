import logging
from flask_restful import Resource
from model import model_proof
from urllib.parse import quote
import requests,json, config, acapy_endpoints

class ProofClass(Resource):
    def request_proof_webhook(received_data):
        try:
            proof_data = json.loads(received_data)    
            proof_model = model_proof.Proof()
            proof_body = proof_model.body_proof_sent(proof_data)

            url = acapy_endpoints.REQUEST_PROOF

            response = requests.post(url, headers= config.JSON_HEADER, json=proof_body)
            response.raise_for_status()

            present_proof_resp = response.json()
            proof_model.setfromdic(present_proof_resp)
            proof_resp = proof_model.response_proof_sent()

            return proof_resp
        
        except json.JSONDecodeError as err:
            logging.error(err)
            return {"Invalid JSON": f"{err}"}

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception: {e}")
            return {"statusCode": response.status_code, "message": response.text}
        
        except Exception as err:
            logging.error(err)
            return {"message": f"{err}"}
        
    def present_proof_webhook(present_exchange_id, cred_def_id, req_num_attr):
        if len(present_exchange_id) == 0 or len(cred_def_id) == 0 or req_num_attr == 0:
            return {'message': 'NO VALUE'}
        
        try:
            proof_data = ProofClass.extract_credential(cred_def_id, req_num_attr)

            if proof_data is None:
                raise Exception("No credential results found")
            
            proof_model = model_proof.Proof()
            proof_body = proof_model.body_present_proof(proof_data)

            url = acapy_endpoints.SEND_PROOF.format(present_exchange_id)
            response = requests.post(url, headers=config.JSON_HEADER, json=proof_body)
            response.raise_for_status
            
            proof_response = response.json()
            return proof_response

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception: {e}")
            return {"statusCode": response.status_code, "message": response.text}
        
        except Exception as err:
            logging.error(err)
            return {"message": f"{err}"}
        
    def extract_credential(cred_def_id, req_num_attr):
        input_parameter = {
                "cred_def_id": cred_def_id
            }
        try:
            json_parameter = json.dumps(input_parameter)
            url_encoded_parameter = quote(json_parameter)

            url = acapy_endpoints.GET_CREDENTIAL.format(url_encoded_parameter)
        
            response = requests.get(url, headers=config.JSON_HEADER, json="")
            response.raise_for_status()

            credential_response = response.json()

            if len(credential_response['results']) != 0:
                credential_id = credential_response['results'][0]['referent']
                
                present_proof_data = {
                    "credentialId": credential_id,
                    "numAttributes": req_num_attr
                }
                return present_proof_data
        
        except json.JSONDecodeError as err:
            logging.error(err)
            return {"Invalid JSON": f"{err}"}

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception: {e}")
            return {"statusCode": response.status_code, "message": response.text}
        
        except Exception as err:
            logging.error(err)
            return {"message": f"{err}"}

    def getproofdetails(self, received_data):
        try:
            requested_proof_record = json.loads(received_data) 
            
            requested_data = json.loads(requested_proof_record["data"])
            pres_ex_id = requested_data["data"]
            
            url = acapy_endpoints.GET_PROOF_REC_BY_ID.format(pres_ex_id)  

            response = requests.get(url, headers= config.JSON_HEADER, json="")
            response.raise_for_status()

            response_proof = response.json() 
            return response_proof

        except json.JSONDecodeError as err:
            logging.error(err)
            return {"Invalid JSON": f"{err}"}

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception: {e}")
            return {"statusCode": response.status_code, "message": response.text}
        
        except Exception as err:
            logging.error(err)
            return {"message": f"{err}"}
        
class ProofVerifyClass (Resource):
    def verify_proof_webhook(present_exchange_id):
        if len(present_exchange_id) == 0:
            return {'message': 'NO VALUE'}
        
        url = acapy_endpoints.VERIFY_PROOF.format(present_exchange_id)

        try:
            response = requests.post(url, headers=config.JSON_HEADER, json={})
            response.raise_for_status()

            verify_presentation_response = response.json()
            proof_model = model_proof.Proof()
            proof_model.setfromdic(verify_presentation_response)
            return proof_model.response_proof_sent()

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception: {e}")
            return {"statusCode": response.status_code, "message": response.text}
        
        except Exception as err:
            logging.error(err)
            return {"message": f"{err}"}