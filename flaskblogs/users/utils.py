import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblogs import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, fext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + fext
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    resized_image = Image.open(form_picture)
    resized_image.thumbnail(output_size)
    resized_image.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender="pythonflaskmaildemo@gmail.com",
                  recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, then simply ignore this email and no change will be made
'''
    mail.send(msg)
