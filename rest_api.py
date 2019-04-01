from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from werkzeug.utils import secure_filename
from tutorial_makeup import simulate_makeup
import os

UPLOAD_FOLDER = 'C:\\Users\\comsc\\AppData\\Local\\Programs\\Python\\Python36\\Project_senior\\tmp_images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
api = Api(app)
# Enable CORS
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

SM = simulate_makeup()
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
		img_output_path = SM.get_makeup(img_path,type_id,style_id)
		img_output_path = img_output_path.decode('utf-8')

		
	return jsonify(
		TYPE_ID=type_id,
		IMAGE_PATH=img_output_path,
		STYLE_ID=style_id
	),201

@app.route("/get_result",methods=["GET"])
def	get_result():

	test = "TEST"
	return jsonify(
		STRING = test
	),201
