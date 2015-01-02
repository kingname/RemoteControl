from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    f = open('mail_note.log','rb')
    content = f.readlines()
    s = ''
    for each in content:
        if 'gmail_helper.py' in each:
            s += each
            s += '</p>'
    f.close()
    return s

if __name__ == '__main__':
    app.run(host='0.0.0.0')
