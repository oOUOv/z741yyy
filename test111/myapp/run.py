from flask import Flask, request, redirect

app = Flask(__name__)



@app.route('/',methods=['GET','POST'])
def index():
    return "hello world"



if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8081)
    # app.run()