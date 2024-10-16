from flask import jsonify
from flask_restful import Resource
from model import model_creddef
import requests,json, config, acapy_endpoints, logging

class CredentialDefinitionClass(Resource):

    def createcreddef(self,received_data):
        try:
            load_creddef_data = json.loads(received_data)
            creddef_data = json.loads(load_creddef_data["data"])
            creddef_model = model_creddef.Credential()
            creddef_body= creddef_model.schema_body_cred_definition(creddef_data)

            url = acapy_endpoints.CREATE_CREDDEF
        
            response = requests.post(url, headers= config.JSON_HEADER, json=creddef_body)
            response.raise_for_status()

            creddef_response = response.json()
            resp_creddef = creddef_model.response_cred_def_id(creddef_response)
            resp_creddefid_detail = CredentialDefinitionClass.extract_cred_def_id(self,resp_creddef)
            return resp_creddefid_detail
        
        except json.JSONDecodeError as err:
            logging.error(err)
            return {"Invalid JSON": f"{err}"}

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception: {e}")
            return {"statusCode": response.status_code, "message": response.text}
        
        except Exception as err:
            logging.error(err)
            return {"message": f"{err}"}


    def extract_cred_def_id(self,resp_creddef): 
        try:
            credential_definition_id = resp_creddef["credential_definition_id"]

            url = acapy_endpoints.GET_CREDDEF_BY_ID.format(credential_definition_id)
            
            response = requests.get(url, headers= config.JSON_HEADER, json="")
            response.raise_for_status()

            creddef_response = response.json()
            creddef_model = model_creddef.Credential()
            resp_creddefid = creddef_model.resp_cred_def_id(creddef_response)
            return resp_creddefid   
        
        except json.JSONDecodeError as err:
            logging.error(err)
            return {"Invalid JSON": f"{err}"}

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception: {e}")
            return {"statusCode": response.status_code, "message": response.text}
        
        except Exception as err:
            logging.error(err)
            return {"message": f"{err}"}

    def getcreddef(self,received_data): 
        try:
            load_creddef_data = json.loads(received_data)
            creddef_data = json.loads(load_creddef_data["data"])
            credential_definition_id = creddef_data["data"]               

            url = acapy_endpoints.GET_CREDDEF_BY_ID.format(credential_definition_id)
        
            response = requests.get(url, headers= config.JSON_HEADER, json="")
            response.raise_for_status()

            resp = response.json()
            creddef_model = model_creddef.Credential()
            creddef_model.setfromdic(resp)

            url = acapy_endpoints.GET_SCHEMA_BY_ID.format(creddef_model.schemaId)

            try:
                schema_response = requests.get(url, headers= config.JSON_HEADER, json="")
                schema_response.raise_for_status()

                resp_loadtojson = schema_response.json() 
                schemaid_value = resp_loadtojson['schema']['id']
                creddef_model.schemaId = schemaid_value
                resp_creddefid = creddef_model.resp_to_dict_cred_def_id_ex()

                return resp_creddefid

            except requests.exceptions.RequestException as e:
                logging.error(f"Request exception: {e}")
                return {"statusCode": schema_response.status_code, "message": "Unable to Fetch Schema ID Record"}          

        except json.JSONDecodeError as err:
            logging.error(err)
            return {"Invalid JSON": f"{err}"}

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception: {e}")
            return {"statusCode": response.status_code, "message": response.text}
        
        except Exception as err:
            logging.error(err)
            return {"message": f"{err}"}

