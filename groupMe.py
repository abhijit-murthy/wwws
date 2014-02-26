import requests

class GroupMeUser(object):
	"""Class to store group me user info and execute group me requests"""
	def __init__(self, token):
		self.token = token
		self.messages = ""

	def setGroupID(self,groupID):
		self.groupID = groupID

	def getGroups(self):
		param = {"token" : self.token}
		requestString = "https://api.groupme.com/v3/groups"
		r = requests.get(requestString,params=param)
		serverResponse = r.json()
		serverResponse = serverResponse['response']
		ret = []
		for group in serverResponse:
			groupInfo = {
				'groupName' : group['name'],
				'groupID'   : group['id']
			}
			ret.append(groupInfo)
		return ret

	def getMessages(self,before_id=None):
		if self.groupID is None:
			return None
		param = {"token" : self.token}
		if before_id is not None:
			param["before_id" ] = before_id

		requestString = "https://api.groupme.com/v3/groups/" + self.groupID +"/messages"
		r = requests.get(requestString,params = param)

		if(r.status_code == 304):
			return None

		serverResponse = r.json()
		serverResponse = serverResponse["response"]
		messages = serverResponse["messages"]
		ret = []
		for message in messages:
			if message["user_id"] != 'system':
				if message["text"] is not None:
					ret.append(message["text"])

		nextID = messages[-1]["id"]
		return (ret,nextID)

	def getAllMessages(self):
		if self.groupID is None:
			return None
		self.messages = []
		current = self.getMessages()
		ctr = 0
		while current != None and ctr < 10:
			messageList = current[0]
			nextID = current[1]
			self.messages.extend(messageList)
			current = self.getMessages(nextID)
			ctr += 1

if __name__ == '__main__':
	test = GroupMeUser("ab8b1250767b0131cfb75e1bee7e888d")
	test.setGroupID("6670487")
	test.getAllMessages()
		
