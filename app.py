import os
import boto3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# # AWS credentials (make sure to set these in your environment)
# AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
# AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
# S3_BUCKET = 'videotore232003'

from dotenv import load_dotenv
load_dotenv()  # This will load environment variables from .env

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
S3_BUCKET = 'videotore232003'


# S3 client setup
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    # Upload file to S3
    s3.upload_fileobj(
        file,
        S3_BUCKET,
        file.filename,
        ExtraArgs={
        "ACL": "public-read",  # This makes the uploaded file publicly readable
        "ContentType": file.content_type  # This sets the correct content type
    }
    )

    # Generate video URL for rendering
    video_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{file.filename}"

    return render_template('view.html', video_url=video_url)

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
