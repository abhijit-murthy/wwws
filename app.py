from flask import Flask,render_template,request,jsonify
from groupMe import GroupMeUser
import json
app = Flask(__name__)

@app.route("/",methods=['GET'])
def start():
	if(request.method == 'GET'):
		if 'access_token' in request.args:
			return render_template('home.html',access_token=request.args['access_token'],state=1)
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
if __name__ == '__main__':
	app.run(debug=True)