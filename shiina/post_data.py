import json
from shiina import create_app

app = create_app()

@app.viewfunction('/')
@app.method("POST")
def origin(request):
    username = request.json.get("username")
    return json.dumps({"msg": "Hello! " + username}), "200 OK"

@app.viewfunction('/profile')
@app.method("GET")
def profile(request):
    id = request.args.get("id")
    return json.dumps({"msg": "Your id is: " + id}), "201 Also OK"

if __name__ == "__main__":
    app.run()
