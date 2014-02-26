from flask import Flask,render_template,request,jsonify
from groupMe import GroupMeUser
from textgen import MarkovTextGen
import json
app = Flask(__name__)

@app.route("/",methods=['GET'])
def start():
	if(request.method == 'GET'):
		state = '0'
		if 'state' in request.args:
			state = request.args['state'] 
		if 'access_token' in request.args and state != '2':
			return render_template('home.html',access_token=request.args['access_token'],state=1)
		elif 'access_token' in request.args and 'groupid' in request.args and state == '2':
			return render_template('home.html',access_token=request.args['access_token'],groupid=request.args['groupid'],state=2)
		else:	
			return render_template('home.html',state=0)
	return "OOPS!"

@app.route("/get_groups",methods=['GET'])
def get_groups():
	if request.method == 'GET':
		if 'access_token' in request.args:
			g = GroupMeUser(request.args['access_token'])
			groups = g.getGroups()
			return jsonify(groups=groups)
	return "OOPS!"

@app.route("/generate_message",methods=['GET'])
def generate_message():
	if request.method != 'GET':
		return "OOPS!"
	g = None
	if 'access_token' in request.args:
		g = GroupMeUser(request.args['access_token'])

	if 'groupid' in request.args:
		g.setGroupID(request.args['groupid'])

	g.getAllMessages()
	textgen = MarkovTextGen(g.messages)
	textgen.buildMatrix()
	sentence = {'sentence' : textgen.genSentence()}

	return jsonify(sentence=sentence)
if __name__ == '__main__':
	app.run(debug=True)