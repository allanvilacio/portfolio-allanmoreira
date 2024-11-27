from flask import Flask, render_template, request, jsonify
from flask_wtf.csrf import CSRFProtect
from decouple import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



server_smtp = config('SERVER_SMPT')
port = config('PORT_EMAIL')

sender_email = config('SENDER_EMAIL')
password =  config('EMAIL_PASSWORD')


receive_email = config('RECEIVE_EMAIL')

def make_msg(name, msg):
    body_msg = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Resposta ao Contato</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    color: #333;
                    margin: 0;
                    padding: 20px;
                }}

                .container {{
                    max-width: 600px;
                }}

                p {{
                    line-height: 1.5;
                }}

                i {{
                    padding-left: 20px;
                    display: block;
                    width: 90%;
                    color: #4d4d4d;
                }}
                a {{
                    text-decoration: none;
                    color: #333;
                }}
            </style>
        </head>

        <body>
            <div class="container">
                <h2>Obrigado pelo Seu Contato!</h2>
                <p>Olá [Nome do Contato],</p>
                <p>Obrigado por entrar em contato através do meu portfólio. Fico muito feliz em saber do seu interesse e estou
                    animado para conversar mais sobre.</p>
                <i>Lorem ipsum dolor sit amet consectetur adipisicing elit. Saepe quas temporibus minima aperiam vel amet quia,
                    iste ipsa enim dolorum perferendis esse? Vel alias cumque, fuga at aperiam dicta maxime!</i>
                <p>Eu retornarei a sua mensagem o mais breve possível. Enquanto isso, sinta-se à vontade para explorar mais
                    sobre o meu trabalho e projetos no meu site.</p>
                <p>Se a sua mensagem for urgente, por favor, entre em contato diretamente pelo telefone ou whatsapp
                    <a href="https://api.whatsapp.com/send?phone=5582996320261&text=Ol%C3%A1%20Venho%20atrav%C3%A9s%20de%20seu%20portf%C3%B3lio." target="_blank">
                        <strong>(082) 99632-0261</strong>.</p>
                    </a>
                <br>
                <p>Atenciosamente,<br>Allan Moreira</p>
            </div>
        </body>

        </html>
        """
    return body_msg


app = Flask(__name__)
app.secret_key = config('FLASK_SECRET_KEY')
csrf = CSRFProtect(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():

    body = request.json
    subject = f'Contato portifólio {body.get("name")}'
    receive_email_cc = f"{receive_email}, {body.get('email')}"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receive_email_cc
    message['Subject'] = subject
    message.attach(MIMEText(make_msg(body.get("name"),body.get("msg")),"html"))
    
    try:
        print('start server')
        print(server_smtp, port)
        print(sender_email, password)
        print( receive_email_cc.split(','))
        print( message.as_string())
        server =smtplib.SMTP(server_smtp, port)
        server.starttls()
        print('1')
        server.login(sender_email, password)
        print('2')
        server.sendmail(sender_email, receive_email_cc.split(','), message.as_string())
        print('3')
        msg = True

    except Exception as ex:
        print(ex)
        msg = False

    finally:
        server.quit()

    return jsonify({'msg':msg})

if __name__=='__main__':
    app.run(debug = config('DEBUG', cast=bool),host='0.0.0.0', port=5000)