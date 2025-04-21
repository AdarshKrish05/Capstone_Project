from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os
import subprocess
from werkzeug.utils import secure_filename
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    try:
        print("\n===== NEW REQUEST =====")
        
        # Validate file
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('index'))
            
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
            
        if not allowed_file(file.filename):
            flash('Only .txt files allowed', 'error')
            return redirect(url_for('index'))
        
        # Validate key
        try:
            key = int(request.form.get('key', 3))
            if key < 1 or key > 25:
                flash('Key must be between 1-25', 'error')
                return redirect(url_for('index'))
        except ValueError:
            flash('Invalid key value', 'error')
            return redirect(url_for('index'))
        
        # Validate mode
        mode = request.form.get('mode')
        if mode not in ('encrypt', 'decrypt'):
            flash('Invalid mode', 'error')
            return redirect(url_for('index'))
        
        # Save file with Windows-safe path
        filename = secure_filename(file.filename)
        input_path = str(Path(app.config['UPLOAD_FOLDER']) / f"input_{filename}")
        output_path = str(Path(app.config['UPLOAD_FOLDER']) / f"output_{filename}")
        file.save(input_path)
        
        # Verify file saved
        if not os.path.exists(input_path):
            flash('File upload failed', 'error')
            return redirect(url_for('index'))
        
        # Compile if needed (Windows)
        if not os.path.exists("cipher.exe"):
            print("Compiling cipher program...")
            compile_result = subprocess.run(
                ["gcc", "cipher.c", "-o", "cipher.exe"],
                capture_output=True,
                text=True,
                shell=True
            )
            if compile_result.returncode != 0:
                print("Compilation failed:", compile_result.stderr)
                flash('Failed to compile cipher program', 'error')
                return redirect(url_for('index'))
        
        # Run cipher (Windows)
        print(f"Running cipher with: {input_path} {output_path} {key} {mode}")
        try:
            result = subprocess.run(
                ["cipher.exe", input_path, output_path, str(key), mode],
                capture_output=True,
                text=True,
                shell=True,
                timeout=10
            )
            
            print("Cipher output:", result.stdout)
            print("Cipher errors:", result.stderr)
            
            if result.returncode != 0:
                error_msg = result.stderr or "Unknown error in cipher program"
                print("Cipher failed:", error_msg)
                flash(f'Processing failed: {error_msg}', 'error')
                return redirect(url_for('index'))
                
            # Read result
            with open(output_path, 'r') as f:
                result_text = f.read()
                
            return render_template(
                "index.html",
                result_text=result_text,
                download_link=url_for('download', filename=f"output_{filename}")
            )
            
        except subprocess.TimeoutExpired:
            print("Cipher timed out")
            flash('Processing timed out', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        print("Unexpected error:", str(e))
        flash('An unexpected error occurred', 'error')
        return redirect(url_for('index'))

@app.route("/download/<filename>")
def download(filename):
    try:
        path = str(Path(app.config['UPLOAD_FOLDER']) / secure_filename(filename))
        return send_file(path, as_attachment=True)
    except Exception as e:
        print("Download failed:", str(e))
        flash('File download failed', 'error')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)