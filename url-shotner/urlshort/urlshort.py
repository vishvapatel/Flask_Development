from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
import os.path
from werkzeug.utils import secure_filename
bp = Blueprint('urlshort', __name__)
#print(__name__)
#Rename the file to urlshort.py tomake flask understand this is the default file to run.


@bp.route('/')
def home():
    return render_template('home.html', codes=session.keys())


@bp.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}
        if os.path.exists('../urls.json'):
            with open('../urls.json') as url_file:
                urls = json.load(url_file)
        if request.form['code'] in urls.keys():
            flash('The code name is already taken')
            return redirect(url_for('urlshort.home'))
        if 'Url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['Url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('C:/Users/-Vs8/Desktop/url-shotner/urlshort/static/user_files/' + full_name)
            urls[request.form['code']] = {'file': full_name}

        with open('../urls.json', 'w') as urls_file:
            json.dump(urls, urls_file)
            session[request.form['code']] = True
        return render_template('your_url.html', code=request.form['code'])
    else:
        #return redirect('/') This is one method but not a good prctise as routes can be changed thus what we need is the home()
        return redirect(url_for('urlshort.home'))

@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('../urls.json'):
        with open('../urls.json') as url_file:
            urls = json.load(url_file)
        if code in urls.keys():
            if 'url' in urls[code].keys():
                return redirect(urls[code]['url'])
            else:
                return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))