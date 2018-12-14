import json
from shiina import create_app

app = create_app()

@app.viewfunction('/')
@app.method('GET','POST')
def origin(request):
    if request.method == 'GET':
        return json.dumps({"GET": 1,})
    if request.method == 'POST':
        return json.dumps({"POST": 2,})

if __name__ == "__main__":
    app.run()
