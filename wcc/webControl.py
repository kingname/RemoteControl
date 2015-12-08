#--coding:utf8--
from flask.ext.bootstrap import Bootstrap
from flask import Flask, render_template, redirect
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from util.DataBaseManager import DataBaseManager

app = Flask(__name__)
bootstrap = Bootstrap(app)

app. config['SECRET_KEY'] = 'youcouldneverknowhis-name'
app.config.from_object(__name__)

class contentForm(Form):
    commandInConfig = StringField(u'')
    commandInWrite = TextAreaField(u'', default="")
    sendCommand = SubmitField(u'发送命令')
    clearCommand = SubmitField(u'清空命令')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = contentForm()
    dataBaseManager = DataBaseManager()
    if form.validate_on_submit():
        innerCommand = form.commandInConfig.data
        writeCommand = form.commandInWrite.data

        if not (innerCommand or writeCommand):
            errorinfo = u'内置命令和自定义代码至少要写一个！'
            return render_template('index.html', form=form, errorinfo=errorinfo)
        else:
            info = {'innerCommand': innerCommand, 'writeCommand': writeCommand, 'run': False}
            dataBaseManager.insert(info)
        return redirect('/')
    return render_template('index.html', form=form, errorinfo='')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, threaded=True)
    app.run(processes=10)
