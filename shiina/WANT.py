from shiina import Shiina

app = Shiina.create_app()

@app.viewfunction('/')
@app.method("POST")
def function(request):
    ...

api_template = APITemplate('/$name/<int:ID>/')
@app.viewfunction(api_template(name="comment"))
@app.method("GET")
def function(request):
    ...

api_prefix = APIPrefix('/user/')
