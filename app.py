from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
import os
import random
from flask import send_from_directory
import subprocess

app = Flask(__name__,static_url_path='/static', static_folder='static')
app.config['UPLOAD_FOLDER'] = 'users_files/'
app.secret_key = 'your_secret_key'  # Set a secret key for flashing messages

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/upload')
def upload_page():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    user_id = request.form['userId']
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    uploaded_file.save(os.path.join(user_folder, uploaded_file.filename))
    flash('File uploaded successfully!', 'success')
    return redirect(url_for('upload_page'))

@app.route('/retrieve')
def retrieve_page():
    return render_template('retrieve.html')

@app.route('/retrieve-files', methods=['GET'])
def retrieve_files():
    user_id = request.args.get('userId')
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
    if os.path.exists(user_folder):
        files = os.listdir(user_folder)
        file_contents = {}
        for file_name in files:
            with open(os.path.join(user_folder, file_name), 'r') as file:
                file_contents[file_name] = file.read()
        return render_template('files.html', files=files, user_id=user_id, file_contents=file_contents)
    else:
        return 'No files found for the given user ID.'

@app.route('/edit-file', methods=['POST'])
def edit_file():
    user_id = request.form['userId']
    filename = request.form['filename']
    file_content = request.form['fileContent']
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
    file_path = os.path.join(user_folder, filename)
    with open(file_path, 'w') as file:
        file.write(file_content)
    return redirect(url_for('retrieve_files', userId=user_id))

@app.route('/files/<user_id>/<filename>')
def get_file(user_id, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], user_id), filename)

def get_user_path(user_id):
    """Get the path of the first script file for the given user ID."""
    users_files_path = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
    if os.path.exists(users_files_path) and os.path.isdir(users_files_path):
        users_files = [f for f in os.listdir(users_files_path) if os.path.isfile(os.path.join(users_files_path, f))]
        if users_files:
            return os.path.join(users_files_path, users_files[0])  # Get the path of the first file
    return None

def get_random_script(user_files_directory):
    
    user_ids = [folder for folder in os.listdir(user_files_directory) if os.path.isdir(os.path.join(user_files_directory, folder))]
    
    if not user_ids:
        print("No user IDs found in the directory.")
        return None

    random_user_id = random.choice(user_ids)
    user_folder_path = os.path.join(user_files_directory, random_user_id)

    python_files = [file for file in os.listdir(user_folder_path) if file.endswith('.py')]
    
    if not python_files:
        print(f"No Python files found in the folder '{random_user_id}'.")
        return None

    random_script_filename = random.choice(python_files)
    script_path = os.path.join(user_folder_path, random_script_filename)

    return script_path

def execute_script(script_path):
    try:
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        output = result.stdout.strip()  

        output_int = int(output)

        return output_int
    except Exception as e:
        print(f"Error running script at '{script_path}': {e}")
        return None


user_files_directory= r"C:\Users\praty\Desktop\WebDev\Second\users_files";


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        user_id = request.form.get('userId')
        if user_id:
            user_script_path = get_user_path(user_id)
            if user_script_path:  
                    try:
                        x1 = execute_script(user_script_path) 
                    except Exception as e:
                        return f'Error executing selected script: {e}'
                    random_script_path = get_random_script(user_files_directory)
                    y1 = execute_script(random_script_path)
                    if x1 == y1:
                        result_msg = 'Draw'
                    elif((x1==0 and y1==2 ) or (x1==1 and y1==0) or (x1==2 or y1==1)):
                        result_msg = 'You win'
                    elif((x1==0 and y1==1 ) or (x1==1 and y1==2) or (x1==2 or y1==0)):
                        result_msg = 'Opponent wins'
                    return f'Test result: {result_msg, x1, y1}'
                    
            else:
                return 'Error: No files found for the provided User ID.'
        else:
            return 'Error: User ID not provided.'
    else:
        return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)