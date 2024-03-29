import argparse
import logging
import os
import signal
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template, send_file, redirect, request, send_from_directory, abort
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.serving import run_simple
from werkzeug.utils import secure_filename

from config.configuration_manager import ConfigurationManager
from core.csv_parser import parse_generate
from utils.log import write_server_log
from utils.output import error, success
from utils.path import is_valid_subpath, is_valid_upload_path, get_parent_directory, process_files

version_info = (2, 1)
version = '.'.join(str(c) for c in version_info)

base_directory = ''

# Flask Werkzeug Logger redirect to server.log file
handler = RotatingFileHandler('logs/server.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)

logging.root.handlers = [handler]


def read_write_directory(directory):
    if os.path.exists(directory):
        if os.access(directory, os.W_OK and os.R_OK):
            return directory
        else:
            error('The output is not readable and/or writable')
    else:
        error('The specified directory does not exist')


def parse_arguments():
    parser = argparse.ArgumentParser(prog='edofparser')
    cwd = os.getcwd()
    parser.add_argument('-d', '--directory', metavar='DIRECTORY', type=read_write_directory, default=cwd,
                        help='Root directory\n'
                             '[Default=.]')
    parser.add_argument('-p', '--port', type=int, default='8000',
                        help=f'Port to serve [Default=8000]')
    parser.add_argument('--password', type=str, default='', help='Use a password to access the page. (No username)')
    parser.add_argument('--ssl', action='store_true', help='Use an encrypted connection')
    parser.add_argument('--version', action='version', version='%(prog)s v')
    parser.add_argument('--env', type=str, default='DEV', help='DEV or PROD')

    args = parser.parse_args()

    # Normalize the path
    args.directory = os.path.abspath(args.directory)

    return args


def main():
    args = parse_arguments()

    # loads applicative configuration
    config = ConfigurationManager(args.env)

    HOST = config.active_configuration['HOST']
    CERTIFICATE_PATH = config.active_configuration['CERTIFICATE_PATH']
    PRIVATE_KEY_PATH = config.active_configuration['PRIVATE_KEY_PATH']

    app = Flask(__name__)
    auth = HTTPBasicAuth()

    global base_directory
    base_directory = args.directory

    # Deal with Favicon requests
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'images/favicon.ico', mimetype='image/vnd.microsoft.icon')

    ############################################
    # File Browsing and Download Functionality #
    ############################################
    @app.route('/', defaults={'path': None})
    @app.route('/<path:path>')
    @auth.login_required
    def home(path):
        # If there is a path parameter and it is valid
        if path and is_valid_subpath(path, base_directory):
            # Take off the trailing '/'
            path = os.path.normpath(path)
            requested_path = os.path.join(base_directory, path)

            # If directory
            if os.path.isdir(requested_path):
                back = get_parent_directory(requested_path, base_directory)
                is_subdirectory = True

            # If file
            elif os.path.isfile(requested_path):

                # Check if the view flag is set
                if request.args.get('view') is None:
                    send_as_attachment = True
                else:
                    send_as_attachment = False

                # Check if file extension
                (filename, extension) = os.path.splitext(requested_path)
                if extension == '':
                    mimetype = 'text/plain'
                else:
                    mimetype = None

                try:
                    return send_file(requested_path, mimetype=mimetype, as_attachment=send_as_attachment)
                except PermissionError:
                    abort(403, 'Read Permission Denied: ' + requested_path)

        else:
            # Root home configuration
            is_subdirectory = False
            requested_path = base_directory
            back = ''

        if os.path.exists(requested_path):
            # Read the files
            try:
                directory_files = process_files(os.scandir(requested_path), base_directory)
            except PermissionError:
                abort(403, 'Read Permission Denied: ' + requested_path)

            return render_template('home.html', files=directory_files, back=back,
                                   directory=requested_path, is_subdirectory=is_subdirectory, version=version)
        else:
            return redirect('/')

    #############################
    # File Upload Functionality #
    #############################
    @app.route('/upload', methods=['POST'])
    @auth.login_required
    def upload():
        if request.method == 'POST':

            # No file part - needs to check before accessing the files['file']
            if 'file' not in request.files:
                return redirect(request.referrer)

            path = request.form['path']
            # Prevent file upload to paths outside of base directory
            if not is_valid_upload_path(path, base_directory):
                return redirect(request.referrer)

            for file in request.files.getlist('file'):

                # No filename attached
                if file.filename == '':
                    return redirect(request.referrer)

                # Assuming all is good, process and save out the file
                # TODO:
                # - Add support for overwriting
                if file:
                    filename = secure_filename(file.filename)
                    full_path = os.path.join(path, filename)
                    try:
                        file.save(full_path)
                    except PermissionError:
                        abort(403, 'Write Permission Denied: ' + full_path)
                    finally:
                        write_server_log("----File parsing started----")
                        parsedCorrectly = parse_generate(full_path)
                        write_server_log("----File parsing finished----")
                        if parsedCorrectly == False:
                            write_server_log("Error while parsing File not correctly formated")
                            abort(415, 'File not correctly formated')

            return redirect(request.referrer)

    # Password functionality is without username
    users = {
        '': generate_password_hash(args.password)
    }

    @auth.verify_password
    def verify_password(username, password):
        if args.password:
            if username in users:
                return check_password_hash(users.get(username), password)
            return False
        else:
            return True

    # Inform user before server goes up
    success('Serving {}...'.format(args.directory, args.port))

    def handler(signal, frame):
        print()
        error('Exiting!')

    signal.signal(signal.SIGINT, handler)

    ssl_context = None
    if args.ssl:
        ssl_context = (CERTIFICATE_PATH, PRIVATE_KEY_PATH)

    run_simple(HOST, int(args.port), app, ssl_context=ssl_context)


if __name__ == '__main__':
    main()
