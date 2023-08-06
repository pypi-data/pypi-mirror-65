import time


def request(req):
    print("request")
    time.sleep(2)
    req.agents = ["negamax", "random"]
    return req


def response(req, resp):
    print("response")
    time.sleep(2)
    return resp
