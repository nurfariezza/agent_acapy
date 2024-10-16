import config

# Invitation
CREATE_INVITATION = config.AGENT_PATH + '/connections/create-invitation?auto_accept=true'
RECEIVE_INVITATION = config.AGENT_PATH + '/connections/receive-invitation?auto_accept=true'

# Schema
CREATE_SCHEMA = config.AGENT_PATH + '/schemas'
GET_SCHEMA_BY_ID = config.AGENT_PATH +'/schemas/{0}' 

# Cred Def
CREATE_CREDDEF  = config.AGENT_PATH + '/credential-definitions'
GET_CREDDEF_BY_ID = config.AGENT_PATH +'/credential-definitions/{0}'

# Issuance
ISSUE_CREDENTIAL = config.AGENT_PATH +'/issue-credential/send-offer'
REQUEST_CREDENTIAL = config.AGENT_PATH +'/issue-credential/records/{0}/send-request'
STORE_CREDENTIAL = config.AGENT_PATH +'/issue-credential/records/{0}/store'
GET_CRED_BY_ID = config.AGENT_PATH +'/issue-credential/records/{0}'

# Proof
REQUEST_PROOF = config.AGENT_PATH +'/present-proof/send-request'
VERIFY_PROOF = config.AGENT_PATH +'/present-proof/records/{0}/verify-presentation' 
SEND_PROOF = config.AGENT_PATH +'/present-proof/records/{0}/send-presentation'
GET_PROOF_REC_BY_ID = config.AGENT_PATH +'/present-proof/records/{0}'  

# Credential
GET_CREDENTIAL = config.AGENT_PATH +'/credentials?wql={0}'