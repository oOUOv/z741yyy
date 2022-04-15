from flask import Flask, request, redirect
from flask import render_template
import pymysql

app = Flask(__name__)

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     port=3308,
                     user='root',
                     password='root',
                     database='userinfo')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

#查询数据
@app.route("/select")
def selectAll():
    sql="SELECT * FROM user ORDER BY id"
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        userList = cursor.fetchall()
    except:
        # 如果发生错误则回滚
        db.rollback()
    return render_template("index.html",user_list=userList)

@app.route('/',methods=['GET','POST'])
def index():
    id=request.args.get("id")
    if id:
        sql="SELECT * FROM user where id="+id+" ORDER BY id"
        cursor.execute(sql)
        user=cursor.fetchall()
        print(user)
        return render_template("index.html",user_list=user)
    return selectAll()
#添加数据
@app.route('/insert',methods=['GET','POST'])
def Insert():
    #进行添加操作
    name=request.form['name']
    score=request.form['score']
    sql="INSERT INTO user(name,score) VALUES ('"+str(name)+"',"+score+")"
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    # 添加完成重定向至主页
    return redirect('/')

@app.route("/insert_page")
def insert_page():
    # 跳转至添加信息页面
    return render_template("insert.html")

#删除数据
@app.route("/delete",methods=['GET'])
def delete():
    # 操作数据库得到目标数据，before_number表示删除之前的数量，after_name表示删除之后的数量
    id = request.args.get("id")
    sql="DELETE FROM user WHERE id="+id
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    return redirect('/')

#修改操作
@app.route("/alter",methods=['GET','POST'])
def alter():
    # 访问/alter  通过GET请求返回修改页面 通过POST请求使用修改操作
    if request.method == 'GET':
        id = request.args.get("id")
        name = request.args.get("name")
        score = request.args.get("score")
        user = []
        user.append(id)
        user.append(name)
        user.append(score)
        return render_template("alter.html", user=user)
    else:
        # 接收参数，修改数据
        id = request.form["id"]
        name = request.form['name']
        score = request.form['score']
        sql = "UPDATE user SET name='" + name + "',score=" + score + " WHERE id="+id
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        return redirect('/')



if __name__ == '__main__':
    # app.run(debug=True,host="0.0.0.0",port=8080)
    app.run()