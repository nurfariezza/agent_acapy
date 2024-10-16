from flask_restful import Resource,request
from model import model_issuance, model_proof
import requests,json, config, re, base64, acapy_endpoints, logging

class InvitationClass(Resource):
    def issueinvitation(self, received_data):
        try:
            load_issuance_data = json.loads(received_data["data"])
            cred_def_id = load_issuance_data["data"]["credentialDefinitionId"]
            attributes = load_issuance_data["data"]["attributes"]

            url = acapy_endpoints.CREATE_INVITATION

            response = requests.post(url, headers=config.JSON_HEADER, json={})
            response.raise_for_status()

            resp_loadtojson = response.json()

            if isinstance(resp_loadtojson, dict):
                issuance_model = model_issuance.CreateInvitation()
                response_invitation = issuance_model.response_issue_invitation(resp_loadtojson)
                issuance_model.setfromdic(resp_loadtojson)

                json_temp = {
                issuance_model.connection_id: {
                    "credentialDefinitionId": cred_def_id,
                    "attributes": attributes
                   
                    }
                }

                try:
                    with open("issuance.json", "r") as infile:
                        json_list = json.load(infile)
                except FileNotFoundError:
                    json_list = []
                json_list.append(json_temp)

                with open("issuance.json", "w") as outfile:
                    json.dump(json_list, outfile, indent=6)

                try:
                    connection_invitation_callback = load_issuance_data["data"]["connectionInvitationCallback"]
                    if connection_invitation_callback:
                        requests.post(connection_invitation_callback, headers=config.JSON_HEADER, json=response_invitation)
                except:
                    return response_invitation
                
        except json.JSONDecodeError as err:
            logging.error(err)
            return {"Invalid JSON": f"{err}"}

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception: {e}")
            return {"statusCode": response.status_code, "message": response.text}
        
        except Exception as err:
            logging.error(err)
            return {"message": f"{err}"}
        
    def proofinvitation(self,received_data):
        try:
            load_proof_data = json.loads(received_data)
            proof_data = json.loads(load_proof_data["data"])            
            proof_attributes = proof_data["data"]["proofAttributes"]

            url = acapy_endpoints.CREATE_INVITATION

            response = requests.post(url, headers=config.JSON_HEADER, json={})

            response.raise_for_status()
            resp_loadtojson = response.json()
            
            if isinstance(resp_loadtojson, dict):
                proof_model = model_proof.Proof()
                response_invitation = proof_model.response_proof_invitation(resp_loadtojson)
                
                json_temp = {
                resp_loadtojson['connection_id']: {
                    "proofAttributes": proof_attributes                   
                    }
                }

                try:
                    with open("proof.json", "r") as infile:
                        json_list = json.load(infile)
                except FileNotFoundError:
                    json_list = []
                json_list.append(json_temp)

                with open("proof.json", "w") as outfile:
                    json.dump(json_list, outfile, indent=6)
                
                try:
                    connection_invitation_callback = proof_data["data"]["connectionInvitationCallback"]
                    if connection_invitation_callback:
                        requests.post(connection_invitation_callback, headers=config.JSON_HEADER, json=response_invitation)

                except:
                    return response_invitation
        
        except json.JSONDecodeError as err:
            logging.error(err)
            return {"Invalid JSON": f"{err}"}

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception: {e}")
            return {"statusCode": response.status_code, "message": response.text}
        
        except Exception as err:
            logging.error(err)
            return {"message": f"{err}"}
        
    def post(self):
        try:
            load_invitation_data = request.json
            invitation_url = load_invitation_data["connectionURL"]

            encoded_invitation_body = re.sub(r'^(https?://[^=]+)', "", invitation_url)
            decoded_invitation_body = base64.b64decode(encoded_invitation_body).decode()
            load_invitation_body = json.loads(decoded_invitation_body)
            
            url = acapy_endpoints.RECEIVE_INVITATION
        
            response = requests.post(url, headers=config.JSON_HEADER, json=load_invitation_body)
            response.raise_for_status()
            
            invitation_response = response.json()
            return invitation_response
        
        except json.JSONDecodeError as err:
            logging.error(err)
            return {"Invalid JSON": f"{err}"}

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception: {e}")
            return {"statusCode": response.status_code, "message": response.text}
        
        except Exception as err:
            logging.error(err)
            return {"message": f"{err}"}
