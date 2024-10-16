import logging
from flask_restful import Resource
from model import model_issuance
import requests,json, config, acapy_endpoints

class IssuanceClass(Resource):
    def issue_cred_webhook(self, data):
        try:
            load_issuance_data = json.loads(data) 
            issuance_model = model_issuance.IssuanceCredential()
            issuance_body = issuance_model.response_cred_def_id_schema_body(load_issuance_data)

            url = acapy_endpoints.ISSUE_CREDENTIAL

            response = requests.post(url, headers=config.JSON_HEADER, json=issuance_body)
            response.raise_for_status()

            issuance_response = response.json()
            return issuance_response
                
        except json.JSONDecodeError as err:
            logging.error(err)
            return {"Invalid JSON": f"{err}"}

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception: {e}")
            return {"statusCode": response.status_code, "message": response.text}
        
        except Exception as err:
            logging.error(err)
            return {"message": f"{err}"}
            

    def accept_credential(credential_exchange_id):
        if len(credential_exchange_id) == 0:
            return {'message': 'NO VALUE'}
        
        url = acapy_endpoints.REQUEST_CREDENTIAL.format(credential_exchange_id)

        try:
            response = requests.post(url, headers=config.JSON_HEADER, json={})
            response.raise_for_status()

            issuance_response = response.json()
            return issuance_response

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception: {e}")
            return {"statusCode": response.status_code, "message": response.text}
        
        except Exception as err:
            logging.error(err)
            return {"message": f"{err}"}
        
    def store_credential_wallet(credential_exchange_id):
        if len(credential_exchange_id) == 0:
            return {'message': 'NO VALUE'}
        
        url = acapy_endpoints.STORE_CREDENTIAL.format(credential_exchange_id)
        
        try:
            response = requests.post(url, headers=config.JSON_HEADER, json={})
            response.raise_for_status()

            resp_loadtojson = response.json()
            return resp_loadtojson
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception: {e}")
            return {"statusCode": response.status_code, "message": response.text}
        
        except Exception as err:
            logging.error(err)
            return {"message": f"{err}"}
           
    def getissuedcredential(self, received_data):
        try:
            requested_credential = json.loads(received_data)
            
            requested_data = json.loads(requested_credential["data"])
            cred_ex_id = requested_data["data"]          

            url = acapy_endpoints.GET_CRED_BY_ID.format(cred_ex_id) 
        
            response = requests.get(url, headers=config.JSON_HEADER, json={})
            response.raise_for_status()

            resp_loadtojson = response.json()
            return resp_loadtojson
        
        except json.JSONDecodeError as err:
            logging.error(err)
            return {"Invalid JSON": f"{err}"}

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception: {e}")
            return {"statusCode": response.status_code, "message": response.text}
        
        except Exception as err:
            logging.error(err)
            return {"message": f"{err}"}




