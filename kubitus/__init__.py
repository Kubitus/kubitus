# encoding: utf-8

from flask import Flask, render_template, flash, request, redirect
from werkzeug.urls import url_encode
from urllib2 import urlopen
from email.mime.text import MIMEText
from smtplib import SMTP


app = Flask(__name__)
app.secret_key = 'what a secret key!'


def _validate_recaptcha(challenge, response, remote_addr):
    """Perform the actual validation."""
    private_key = '6LerttYSAAAAANfAFTDXSssP76iAcxY4L_Hd1E_X'

    data = url_encode({
        'privatekey': private_key,
        'remoteip': remote_addr,
        'challenge': challenge,
        'response': response})

    response = urlopen('http://api-verify.recaptcha.net/verify', data)

    if response.code != 200:
        return False

    lines = [line.strip() for line in response.readlines()]

    if lines and lines[0] == 'true':
        return True

    return False


@app.route('/')
def index():
    return render_template('index.html.jinja2')


@app.route('/<string:page>/')
def page(page):
    return render_template('%s.html.jinja2' % page, page=page)


@app.route('/contact/', methods=['POST'])
def contact():
    social = request.form.get('social', '')
    name = request.form.get('name', '')
    firstname = request.form.get('firstname', '')
    function = request.form.get('function', '')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    comment = request.form.get('comment', '')
    challenge = request.form.get('recaptcha_challenge_field', '')
    response = request.form.get('recaptcha_response_field', '')
    remote_ip = request.remote_addr

    if not challenge or not response:
        flash(u'Le champ de validation est requis', 'error')
        return redirect('/contact/')

    if not all((social, name, firstname, function, phone)):
        flash(u'Les champs marqués d’un astérisque sont requis', 'error')
        return redirect('/contact/')

    if not _validate_recaptcha(challenge, response, remote_ip):
        flash(u'La validation a échoué', 'error')
        return redirect('/contact/')

    text = u"""
Une nouvelle demande a été faite pour Kubitus.

Raison sociale : %s
Nom : %s
Prénom : %s
Fonction : %s
Email : %s
Téléphone : %s
Commentaire :
%s
""" % (social, name, firstname, function, email, phone, comment)

    message = MIMEText(text.encode('utf-8'))
    message.set_charset('utf-8')
    message['Subject'] = u'Nouvelle demande pour Kubitus'
    message['From'] = 'contact@kubitus.fr'
    message['To'] = 'contact@kubitus.fr'

    server = SMTP('smtp.keleos.fr')
    server.sendmail(
        'contact@kubitus.fr', ['contact@kubitus.fr'],
        message.as_string())
    server.quit()

    flash(u'Votre demande a bien été enregistrée, un conseiller prendra '
          u'contact avec vous dans les plus brefs délais', 'info')
    return redirect('/')
