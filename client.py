import requests
def test():
    prompt = {
        "promptWord":"test",
        "top_p":0.2,
        "temperature":1,
        }
    response  = requests.post("http://192.168.0.7:8088/test",json=prompt)
    print(response.json())



def prompt(word):
    import requests
    prompt = {
        "promptWord":word,
        "top_p":0.2,
        "temperature":1,
        }
    response  = requests.post("http://192.168.0.7:8088/prompt",json=prompt)
    reJson = response.json()
    print(reJson)
    if (reJson["status"] =="ok"):
        return reJson["data"]["ouput"]


if __name__ == "__main__":
    print(prompt("你好"))