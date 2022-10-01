class API_Messages():
    EMAIL_EXISTS="Email Already exists. Please Login"
    EMAIL_DOESNOT_EXIST="EMAIL doesn't exist, please Register"
    SUCCESSFUL_REGISTRATION="Successfully Registered"
    INCORRECT_PASSWORD="Password is incorrect. Please check it"
    SUCCESSFUL_LOGIN="Successfully LoggedIn"
    SUCCESSFUL_LOGOUT="Successfully LoggedOut"
    SESSION_EXPIRED="Session Expired"
    PROFILE_UPDATED="Profile Updated Successfully"
    USER_PROFILE="User Profile"
    HIRER_PROFILE="User Profile"
    LINK_BROKEN="Link Broken"
    ADDED_OPPORTUNITY="Successfully Added Opportunity"
    OPPORTUNITIES="Opportunities"
    UPDATED_OPPORTUNITY="Updated Opportunity"
    APPLIED="Successfully Applied"
    APPLIED_TO="Applications List"
    ARCHIEVED="Archieved Applications"
    WITHDRAWN="Application Withdrawn Successfully"

def api_response(response_type,api_message,data=None):
    d={}
    d['response_type']=response_type
    d['api_message']=api_message
    if(data):
        d['data']=data
    return d