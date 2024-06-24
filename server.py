from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load models
path_to_model = 'models'
model = 'random_forest_model'
countries = ['United States', 'China', 'Japan', 'Germany']

models = {}

for country in countries:
    models[country] = joblib.load(f'{path_to_model}/{model}_{country}.pkl')

# Load temperature data
temperature_data = pd.read_csv('data\GlobalLandTemperaturesByCountry.csv')

# Load emissions data
methane_data = pd.read_csv('data\ch4.csv')
co2_data = pd.read_csv('data\co2.csv')
nitrous_oxide_data = pd.read_csv('data\\n2o.csv')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    country = data['country']
    year = data['year']
    features = np.array(data['features']).reshape(1, -1)
    
    if country in models:
        model = models[country]

        # Convert features to df to match the training format
        feature_names = ['co2', 'ch4', 'n2o'] 
        features_df = pd.DataFrame(features, columns=feature_names)

        prediction = model.predict(features_df)[0]
        
        # Fetch historical temperature
        historical_temperature = temperature_data[(temperature_data['dt'].str.startswith(str(year))) & 
                                                  (temperature_data['country'] == country)]['AverageTemperature'].mean()
        
        if pd.isna(historical_temperature):
            return jsonify({'error': 'No historical temperature data found'}), 404
        
        actual_temperature = historical_temperature + prediction
        
        return jsonify({
            'prediction': prediction,
            'historical_temperature': historical_temperature,
            'actual_temperature': actual_temperature
        })
    else:
        return jsonify({'error': 'Model for specified country not found'}), 400


@app.route('/historical_data', methods=['GET'])
def historical_data():
    year = request.args.get('year')
    country = request.args.get('country')
    
    filtered_data = temperature_data[(temperature_data['dt'].str.startswith(year)) & 
                                     (temperature_data['country'] == country)]
    
    if filtered_data.empty:
        return jsonify({'error': 'No data found for the specified year and country'}), 404
    else:
        result = filtered_data[['AverageTemperature', 'AverageTemperatureUncertainty']].mean().to_dict()
        return jsonify(result)

@app.route('/emissions_data', methods=['GET'])
def emissions_data():
    year = int(request.args.get('year'))
    country = request.args.get('country')

    methane_filtered = methane_data[(methane_data['Year'] == year) & (methane_data['Entity'] == country)]
    co2_filtered = co2_data[(co2_data['Year'] == year) & (co2_data['Entity'] == country)]
    nitrous_oxide_filtered = nitrous_oxide_data[(nitrous_oxide_data['Year'] == year) & (nitrous_oxide_data['Entity'] == country)]

    result = {
        'methane': methane_filtered['Annual methane emissions in CO₂ equivalents'].mean() if not methane_filtered.empty else None,
        'co2': co2_filtered['Annual CO₂ emissions'].mean() if not co2_filtered.empty else None,
        'nitrous_oxide': nitrous_oxide_filtered['Annual nitrous oxide emissions in CO₂ equivalents'].mean() if not nitrous_oxide_filtered.empty else None
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
