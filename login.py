USERS={"banker":"bank123"}
def authenticate(u,p):
 return USERS.get(u)==p
