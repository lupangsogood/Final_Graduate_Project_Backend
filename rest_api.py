from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'C:\\Users\\ANUSIT\\Anaconda3\\envs\\opencv-env\\Project_senior\\Project_senior\\images_output'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
api = Api(app)
# Enable CORS
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/apply_makeup", methods=["POST"])
def makeup():
	
	if request.method == "POST":    		
		type_makeup = request.form["type"]
		style_makeup = request.form["style"]  
		file = request.files['image']
		f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
		# ประมวลผล
		# ...
		# ตัวอย่างเช่น รับค่ามา แล้ว คูณ 2
		img_path = f

		file.save(f)
		type_id = type_makeup
		style_id = style_makeup
		# ###
	return jsonify(
		TYPE_ID=type_id,
		IMAGE_PATH=img_path,
		STYLE_ID=style_id
	),201