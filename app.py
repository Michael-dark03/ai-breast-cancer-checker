from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load the model
with open('self_check_breast_cancer_model.pkl', 'rb') as f:
    model = pickle.load(f)

# List of input fields (excluding 'diagnosis')
FIELDS = [
    'age', 'bmi', 'family_history', 'menopause_status', 'lump_present', 'lump_size', 'lump_fixed', 'lump_pain',
    'nipple_discharge', 'skin_changes', 'nipple_retraction', 'breast_pain', 'swelling', 'hormonal_therapy',
    'oral_contraceptives', 'alcohol_consumption', 'smoking', 'physical_activity', 'previous_biopsy',
    'mammogram_history', 'last_mammogram'
]

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', fields=FIELDS)

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    features = []
    for field in FIELDS:
        value = request.form.get(field)
        if value is not None and value != '':
            try:
                value = float(value)
            except ValueError:
                pass
        features.append(value)
    features = np.array(features).reshape(1, -1)
    prediction = model.predict(features)
    return jsonify({'prediction': int(prediction[0])})

@app.route('/breast_cancer_ai')
def breast_cancer_ai():
    return render_template('breast_cancer_ai.html')

if __name__ == '__main__':
    app.run(debug=True)
