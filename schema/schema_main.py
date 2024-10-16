import logging
from flask import jsonify
from flask_restful import Resource, request
from model import model_schemas
import requests,json, config, acapy_endpoints

class HealthClass(Resource):

    def get(self):
        return "API SERVICE RUNNING"

class SchemaClass(Resource):

    def createschema(self,received_data):
        try:
            requested_schema = json.loads(received_data)

            requested_schema_body= json.loads(requested_schema["data"])
            schema_model = model_schemas.Schema()
            body_schema = schema_model.create_schema_body(requested_schema_body)

            url = acapy_endpoints.CREATE_SCHEMA
        
            response = requests.post(url, headers=config.JSON_HEADER, json=body_schema)
            response.raise_for_status()

            schema_response = response.json()
            resp_body_schema = schema_model.response_schema(schema_response)
            return resp_body_schema
        
        except json.JSONDecodeError as err:
            logging.error(err)
            return {"Invalid JSON": f"{err}"}

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception: {e}")
            return {"statusCode": response.status_code, "message": response.text}
        
        except Exception as err:
            logging.error(err)
            return {"message": f"{err}"}


    def getschema(self,received_data):
        try:
            requested_schema = json.loads(received_data)
            if requested_schema is not None:
                requested_data = json.loads(requested_schema["data"])
                schema_id = requested_data["data"]          
                url = acapy_endpoints.GET_SCHEMA_BY_ID.format(schema_id)  
            
                response = requests.get(url, headers= config.JSON_HEADER, json="")
                response.raise_for_status()

                schema_response = response.json()
                schema_model = model_schemas.Schema()
                resp_body_schema = schema_model.response_fetch_schema(schema_response)
                    
                return resp_body_schema
        
        except json.JSONDecodeError as err:
            logging.error(err)
            return {"Invalid JSON": f"{err}"}

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception: {e}")
            return {"statusCode": response.status_code, "message": response.text}
        
        except Exception as err:
            logging.error(err)
            return {"message": f"{err}"}


