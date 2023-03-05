import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init SQLAlchemy
db = SQLAlchemy(app)

   

# Log data model
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Log {self.id}>'



@app.route('/')
def index():
    return 'Welcome to the Work Log!'

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # 处理表单提交的数据
        title = request.form['title']
        content = request.form['content']
        # 将日志保存到数据库中
        log = Log(title=title, content=content)
        db.session.add(log)
        db.session.commit()
        return redirect('/')
    else:
        # 显示表单
        return '''
            <form method="post">
                <label for="title">Title</label>
                <input type="text" name="title" id="title" />
                <label for="content">Content</label>
                <textarea name="content" id="content"></textarea>
                <input type="submit" value="Create" />
            </form>
        '''

@app.route('/logs')
def logs():
    logs = Log.query.all()
    return render_template('logs.html', logs=logs)


@app.route('/logs/<int:id>')
def log(id):
    log = Log.query.get_or_404(id)
    return render_template('log.html', log=log)


if __name__ == '__main__':
    if not os.path.exists('logs.db'):
        open('logs.db', 'w').close()
        with app.app_context():
            model = Log
            db.create_all()
 
    app.run(debug=True)


