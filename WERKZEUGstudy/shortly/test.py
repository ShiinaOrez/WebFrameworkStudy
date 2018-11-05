from shiina import Shiina, create_app
import json

app = create_app(with_static = False)

@app.viewfunction('/')
@app.method('GET')
def origin(request):
    print (app.url2endpoint.keys())
    return json.dumps({"msg": 'successful!'})

@app.viewfunction('/short')
@app.method('POST', 'GET')
def short(request):
    return json.dumps({"info": str(request.environ)})

if __name__ == "__main__":
    app.run()
