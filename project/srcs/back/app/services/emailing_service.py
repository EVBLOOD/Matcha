from flask_mail import Message
from app.core.config import Config

class EmailingService :
    def send_email_welcoming(email: str, username : str, token: str) :
        msg = Message(
            subject="Welcome to Matcha",
            recipients=[email],
        )
        link = Config.BACKEND_LINK + "/user/verify_account?token_id=" + token 

        msg.body = f"""
        Hello { username },

        Welcome to Matcha! To activate your account, visit the link below:
        { link }

        If you didn't register, please ignore this email. Contact us if you need any help!
        """
        
        msg.html = f"""
          <body>
            <p>Hello { username },</p>
            <p>Welcome to Matcha! To activate your account, please click the link below:</p>
            <p><a href="{ link }">Activate your account</a></p>
            <p>If you didn’t sign up with us, please ignore this email. Feel free to contact support if you need help!</p>
          </body>
        """
        Config.mail.send(msg)
    
    
    def send_email_change_confirming(email: str, username : str, token: str) :
        msg = Message(
            subject="Email from Matcha",
            recipients=[email],
        )
        link = Config.FRONT + "/user/verify_change_email?token=" + token + "&email=" + email

        msg.body = f"""
        Hello { username },

        To change your email account, please click the link below :
        { link }

        If you didn’t request this, please ignore this email. Feel free to contact support if you need help!
        """
        
        msg.html = f"""
          <body>
            <p>Hello { username },</p>
            <p>To change your email account, please click the link below:</p>
            <p><a href="{ link }">Change email</a></p>
            <p>If you didn’t request this, please ignore this email. Feel free to contact support if you need help!</p>
          </body>
        """
        Config.mail.send(msg)

    def send_email_forgoten_pass(email: str, username : str, token: str) :
        msg = Message(
            subject="Email from Matcha",
            recipients=[email],
        )
        link = Config.FRONT + "/user/verify-reset-token?token=" + token

        msg.body = f"""
        Hello { username },

        To reset your email account, please click the link below :
        { link }

        If you didn’t request this, please ignore this email. Feel free to contact support if you need help!
        """
        
        msg.html = f"""
          <body>
            <p>Hello { username },</p>
            <p>To reset your email account, please click the link below:</p>
            <p><a href="{ link }">Change email</a></p>
            <p>If you didn’t request this, please ignore this email. Feel free to contact support if you need help!</p>
          </body>
        """
        Config.mail.send(msg)