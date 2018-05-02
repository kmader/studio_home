from flask import Flask, jsonify, request,  render_template, abort, make_response, render_template_string, send_from_directory

from .database.db import get_all_models, get_model
from .models import get_predictions_for_model
import os
import pickle
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, FileField, FloatField, HiddenField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired
from werkzeug import secure_filename
import subprocess
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
root_folder = os.environ.get("DEPLOY_DIR") + "/model_storage/"

@app.route('/')
def index():
    return jsonify({'status' : 'OK'})

@app.route('/models/list')
def models_list():
	
	models = get_all_models()
	num_models = len(models)

	list_of_models = [{
		'name' : model['name'], 
		'version' : model['version'], 
		'last_deployed' : model['last_deployed'], 
		'api_activated' : model['activated'], 
		'backend_adapter' : model['adapter']} for model in models]

	return jsonify({'num_models' : num_models, 'models' : list_of_models})

@app.route('/models/<string:name>/v<int:version>/')
def model_detail(name, version=1):

	model = get_model(name, version)
	del model['path']

	if not model['activated']:
		return jsonify({'success':False, 'message' : 'The specified model is deactivated.'})

	return jsonify(model)

@app.route('/models/<string:name>/v<string:version>/predict', methods=['POST'])
def model_predict(name, version="1"):	

	model_path = root_folder + name + "/v" + version 

	print ( request.files)
	with open(root_folder + name + "/v" + version + "/mapping.pkl", "rb") as f:
		data_mapping = pickle.load(f)
		keys = []
		values = []
		for column in data_mapping['inputs']['InputPort0']['details']:
			keys.append(column["name"])
			if column["type"] == 'Image' or column['type'] == 'Numpy':
				file = request.files[column["name"]]
				filename = secure_filename(file.filename)
				file.save(os.path.join(model_path, filename))
				values.append(filename)
				
			else:
				values.append(request.form[column["name"]])
		
		with open (model_path + "/test.csv", "w") as f:
			f.write (",".join(keys) + "\n")
			f.write(",".join(values))

		program = ["python", os.path.abspath("backend/wrapper.py"), model_path + "/test.csv"]
        
		task = subprocess.Popen(program, cwd=model_path)
		status_code = task.wait()

		if status_code < 0:
			return jsonify({"status" : "ERROR", "message": "error duing inferencer"})
		
		out_type = data_mapping['outputs']['OutputPort0']['details'][0]['type']
		try:
			with open(model_path + '/test_result.csv') as csvfile:
				reader = csv.DictReader(csvfile)
				row1 = next(reader)
				if out_type == 'Categorical':
					return jsonify({'type': out_type, 'base_path': name + "/v" + version, "status": "OK",
									'predictions':row1['predictions'], 'probabilities':row1['probabilities']})
				else:

					return jsonify({"status": "OK", 'type': out_type, 'base_path': name + "/v" + version, 
								'predictions':row1['predictions']})
		except:
			return jsonify({"status" : "ERROR", "message": "Unknown error occured"})
	
	return jsonify({"status" : "ERROR", "message": "Unknown error occured"})


@app.route('/models/<string:name>/v<string:version>/app.html')
def model_app(name, version="1"):
    	
	with open(root_folder + name + "/v" + version + "/mapping.pkl", "rb") as f:
		data_mapping = pickle.load(f)
		
		class MyForm(FlaskForm):
			dls_model_name = HiddenField()
			dls_model_version = HiddenField()
			pass
		api_url = 'curl -X POST HOST_SERVER '
		for column in data_mapping['inputs']['InputPort0']['details']:
			if column["type"] == 'Numeric':
				setattr(MyForm, column["name"], FloatField(label=column["name"], validators=[InputRequired()]))
				api_url += "-F \"%s\"=\"%s\" " % (column["name"],'replace_this_value')
			elif column["type"] == 'Image' or column['type'] == 'Numpy':
				setattr(MyForm, column["name"], FileField(label=column["name"], validators=[FileRequired()]))
				api_url += '-H "Content-Type:multipart/form-data" '
				api_url += '-F \"data={\\\"key\\\": \\\"'+column["name"]+ '\\\"};type=application/json\" -F \"'+column["name"]+'=@/path/to/image.png\" '
			elif column["type"] == 'Array':
				setattr(MyForm, column["name"], TextAreaField(label=column["name"], validators=[InputRequired()]))
				api_url += "--data-urlencode \"%s\"=\"%s\" " % (column["name"],'replace_this_value')
			else:
				cat=[]
				col = ""
				for category in column["categories"]:
					cat.append((category, category))
					col = category
				setattr(MyForm, column["name"], SelectField(column["name"], choices=cat) )
				api_url += "-F \"%s\"=\"%s\" " % (column["name"], col)

		form = MyForm(dls_model_name=name, dls_model_version=version)
		return render_template("app.html", form=form, name=name, version=version, api_url=api_url)
	abort(404)

@app.route('/models/file/<path:path>')
def model_app_send_file(path):
	if path.endswith(".png") or path.endswith(".npy"):
		print (root_folder, path)
		return send_from_directory(root_folder, path)
	abort(404)
