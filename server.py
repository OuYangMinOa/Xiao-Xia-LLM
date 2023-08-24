from flask import Flask, jsonify, render_template, request
import threading
import dotenv
import time
import json

dotenv.load_dotenv()

from LLm import LOAD_LLM_MODEL


model = lambda x:"hi"
# model = LOAD_LLM_MODEL()
print(model("init"))

app   = Flask(__name__)
messages  = []
PromptStillRunning = False
UPDATED_ = True # if user is updated

@app.route('/')
def home():
    return render_template("home.html")

def buildPrompt():
    global messages
    output = ""
    for i in  range(len(messages)):
        output += "Q: " + messages[i]["Userinput"]
        if (messages[i]["response"] != "waiting ..."):
            output += "A: " + messages[i]["response"]
    return output

def ThreadPrompt(word):
    global PromptStillRunning, UPDATED_, messages
    PromptStillRunning = True
    result = model(buildPrompt())
    # time.sleep(5)
    if (len(messages) >0):
        messages[-1] =  {"response":result,"Userinput":messages[-1]["Userinput"]}
        print(messages)
    PromptStillRunning = False
    UPDATED_ = False

@app.route('/check_result', methods=['GET'])
def check_result():
    global PromptStillRunning, UPDATED_
    if not PromptStillRunning and not UPDATED_:
        return jsonify({"result":"Ready"})
    else:
        return jsonify({"result":"Not ready"})
    
@app.route('/reload', methods=['GET'])
def reload():
    global PromptStillRunning, UPDATED_, messages
    messages = []
    PromptStillRunning = False
    UPDATED_ = False
    return jsonify({"status":"ok"})

@app.route('/prompt',methods=['POST'])
def prompt():
    promptInput = request.get_json()
    word        = promptInput["promptWord"]
    topp        = promptInput["top_p"]
    temp        = promptInput["temperature"]
    print(f'[*] Content: \n{"="*60}\nInput:\n{word}\n')

    try:
        result      = model(word,topp,temp)
        print(f'Ouput:\n{result}\n{"="*60}\n')
        ouputJoson  = {
            "status":"ok",
            "data":{
                    "promptWord":word,
                    "top_p":topp,
                    "temperature":temp,
                    "ouput":result,
                }
        }
    except Exception as e:
        result = e
        print(e)
        ouputJoson  = {
            "status":e
            }
    
    return jsonify(ouputJoson)


@app.route('/test',methods=['POST'])
def test():
    promptInput = request.get_json()
    print(promptInput)
    ouputJoson = {
        "status":"ok",
        "data":{
                "promptWord":"None",
                "top_p":0.2,
                "temperature":1,
                "ouput":"None",
            }
        }
    return jsonify(ouputJoson)


@app.route('/chat',methods=['POST','GET'])
def chat():
    global PromptStillRunning,messages,UPDATED_
    UPDATED_ = True
    if request.method == "POST":
        userInput = request.form.get("userInput")
        PromptStillRunning = True
        messages.append( {"response":"waiting ...","Userinput":userInput})
        threading.Thread(target=ThreadPrompt,args=(userInput,),daemon=True).start()
        print(messages)
        return render_template("chat.html",messages=messages)


    if (request.method == "GET"):
        return render_template("chat.html",messages=messages)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8088,debug=False)