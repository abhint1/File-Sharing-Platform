from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import secrets

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# Dictionary to store shareable links and corresponding file paths
shareable_links = {}

@app.route('/')
def home():
    return render_template('index.html', shareable_link_download=None, shareable_link_view=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"

    if file:
        # Generate a unique filename
        filename = secrets.token_hex(16) + file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the file to the 'uploads' folder
        file.save(file_path)
        
        # Generate a shareable link for download
        link_download = secrets.token_urlsafe(16)
        shareable_links[link_download] = file_path

        # Generate a shareable link for viewing in a new tab
        link_view = secrets.token_urlsafe(16)
        shareable_links[link_view] = file_path

        return render_template('index.html', shareable_link_download=request.host_url + 'download/' + link_download, shareable_link_view=request.host_url + 'download/' + link_view)


@app.route('/download/<link>')
def download_file(link):
    file_path = shareable_links.get(link)

    if file_path:
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found."

if __name__ == '__main__':
    app.run(debug=True)



































































































# from flask import Flask, render_template, request, send_file
# import os
# import secrets

# app = Flask(__name__)
# import os

# app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# # Define a route for the homepage
# @app.route('/')
# def home():
#     return render_template('index.html')

# # Handle file upload
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return "No file part"

#     file = request.files['file']
    
#     if file.filename == '':
#         return "No selected file"

#     if file:
#         # Generate a unique filename
#         filename = secrets.token_hex(16) + file.filename

#         # Save the file to the 'uploads' folder
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#         # Create a shareable link
#         link = f"/download/{filename}"
#         return f"File uploaded! Share this link: {link}"

# # Serve shared files
# @app.route('/download/<filename>')
# def download_file(filename):
#     return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
