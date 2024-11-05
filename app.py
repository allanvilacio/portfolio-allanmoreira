from flask import Flask, render_template, request, jsonify
from flask_wtf.csrf import CSRFProtect
from time import sleep
from decouple import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



server_smtp = 'smtp.gmail.com'
port = 587 
sender_email ='allanmoreiracontato@gmail.com'
password =  config('EMAIL_PASSWORD')


receive_email = "allan.vilacio@gmail.com, allan@acaiconcept.com"
subject = '3 email teste portifolio'
body_msg = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>teste de email</title>
    </head>
    <body>
        <h1>teste de email h1</h1>
        <p>teste paragrafo</p>
    </body>
    </html>
"""



app = Flask(__name__)
app.secret_key = config('FLASK_SECRET_KEY')
csrf = CSRFProtect(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():

    #body = request.json

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receive_email
    message['Subject'] = subject
    message.attach(MIMEText(body_msg,"html"))

    try:
        server =smtplib.SMTP(server_smtp, port)
        server.starttls()

        server.login(sender_email, password)

        server.sendmail(sender_email, receive_email.split(','), message.as_string())
        print('Email enviado com sucesso')
    except Exception as e:
        print(f'Houve um erro {e}')
    finally:
        server.quit()
    
    #sleep(5)

    return jsonify({'msg':False})

if __name__=='__main__':
    app.run(debug = config('DEBUG', cast=bool))