from flask import Blueprint, render_template, request, redirect, send_file
import pyqrcode 
from pyqrcode import QRCode 
import subprocess

import os
import shutil


from .extensions import db
from .models import Link



path = '/static/'

short = Blueprint('short', __name__)


@short.route('/<short_url>')
def redirect_url_to_url(short_url):

	link = Link.query.filter_by(short_url=short_url).first_or_404()

	link.visits = link.visits + 1

	db.session.commit()

	return render_template('redirect.html', redirect_url = link.original_url)


#@short.route('/<short_url>')
#def redirect_url_to_url(short_url):
#    link = Link.query.filter_by(short_url=short_url).first_or_404()

    #link.visits = link.visits + 1
    #db.session.commit()

    #return redirect(link.original_url) 

@short.route('/')
def index():
	return render_template('index.html')


@short.route('/<qr_file>')
def download(qr_file):
	#return send_from_directory('/', qr_file, as_attachment=True)
	return send_file(qr_file, as_attachment=True)


@short.route('/add_link', methods=['POST'])
def add_link():
    original_url = request.form['original_url']

    if original_url.startswith(('http')) == False:
        original_url = 'http://' + original_url

    link = Link(original_url=original_url)
    db.session.add(link)
    db.session.commit()




    dir = os.getcwd()
	
	#create a folder is it doesn't exist
	#if not os.path.exists(dir):
	#os.makedirs(dir)
	


    qr_url = pyqrcode.create(link.short_url) 

    qr_file = link.short_url + 'qr' + '.svg'
	#qr_url.svg(os.path.join(app.root_path, qr_file), scale = 8) 
	
    absolute_path = os.path.abspath('../'+'urlshortner/url_shortner/static/'+ qr_file)

 
    qr_url.svg(absolute_path, scale = 8) 

    
	#qrImage = myQr.png(os.path.join(dir, name.get()+".png"), scale= 6)

    #subprocess.call(['chmod', '-R', '+w', '/downloads'])

    #qr_newfile = shutil.copy(qr_file, '/downloads')


    return render_template('link_added.html', 
        new_link=link.short_url, original_url=link.original_url, qr_file=qr_file)

@short.route('/privacy')
def privacy():

    return render_template('privacy.html')

@short.route('/stats')
def stats():
    links = Link.query.all()

    return render_template('stats.html', links=links)

@short.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@short.errorhandler(400)
def bad_request():
    """Bad request."""
    return make_response(render_template("400.html"), 400)


@short.errorhandler(500)
def server_error():
    """Internal server error."""
    return make_response(render_template("500.html"), 500)
