from flask import Flask, request
from flask_cors import CORS
#import data as ipozdata
import json
import subprocess
import hashlib
import os
import random
import string 
app = Flask(__name__)
CORS(app)

workdir=os.getcwd()

persistance_names = {}

persistance_applications = {}


hashfunc = lambda x: hashlib.sha1(x.encode("UTF-8")).hexdigest()[:10]
hashfunclong = lambda x: hashlib.sha1(x.encode("UTF-8"))

@app.route("/makeaccount", methods=['GET'])
def makeaccount():
    #app.logger.debug(request.json)
    # wallet must be unlocked already
    #data = request.json['name']
    data = request.args.get('name')
    name = ''.join(random.choices('.12345abcdefghijklmnopqrstuvwxyz', k=11))
    os.chdir(workdir+"/accounts")
    print(name)
    output = subprocess.check_output('./makeaccount.sh %s' % name, shell=True) 
    myjson = json.loads(output)
    mykey = myjson["processed"]["action_traces"][0]['act']['data']['owner']['keys'][0]['key']
    if (data not in persistance_names):
        persistance_names[data] = {"exists": True, "pubkey" : mykey, "accname" : name, "privkey" : privkey[16:]}
        persistance_applications[privkey[16:]] = {"abn": data, "accname" : name, "applications" : []}
        with open(workdir+"/accounts/dataStore_User_"+name, "r") as f:
            lines = f.readlines()
            privkey = lines[-2]
        output = {"exists": False, "pubkey" : mykey, "accname" : name, "privkey" : privkey[16:]}
        return json.dumps(output)
    else:
        temp = persistance_names[data]
        temp["privkey"] = ""
        return json.dumps(temp)

@app.route("/addapplication", methods=['GET'])
def addapplication():
    privkey = request.args.get("privkey")
    appdoc = request.args.get("appdoc")
    persistance_applications[privkey]["applications"].append(appdoc)
    return json.dumps({"transactionlabel" : hashfunclong(appdoc)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5100, threaded=True, debug=True)
