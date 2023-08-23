from flask import Flask, jsonify, render_template, request

import dotenv
dotenv.load_dotenv()

from LLm import LOAD_LLM_MODEL


# model = LOAD_LLM_MODEL()
app   = Flask(__name__)
messages  = []

@app.route('/')
def home():
    return render_template("home.html")



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
    if request.method == "POST":
        userInput = request.form.get("userInput")
        result = userInput
        messages.append((result,userInput))
        print(messages)
        return render_template("chat.html",messages=messages)
        
    if (request.method == "GET"):
        return render_template("chat.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8088)