## Prerequisites

- Python 3.7 or higher
- pip

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Data Preparation

1. Place your model files in the `models` directory. Ensure the files are named in the format `random_forest_model_<Country>.pkl` (e.g., `random_forest_model_United States.pkl`).

2. Place your data files in the `data` directory:
    - `GlobalLandTemperaturesByCountry.csv`
    - `ch4.csv`
    - `co2.csv`
    - `n2o.csv`

## Running the Server

1. Make sure you are in the project directory and your virtual environment is activated.

2. Start the Flask server:
    ```bash
    python app.py
    ```

3. The server will start on `http://127.0.0.1:5000`. You can now make requests to the available endpoints.

## API Endpoints

### Predict Future Climate

- **URL:** `/predict`
- **Method:** `POST`
- **Content-Type:** `application/json`
- **Request Body:**
    ```json
    {
        "country": "United States",
        "year": 2030,
        "features": [400, 2, 0.5]
    }
    ```
- **Response:**
    ```json
    {
        "prediction": 1.5,
        "historical_temperature": 15.0,
        "actual_temperature": 16.5
    }
    ```

### Get Historical Data

- **URL:** `/historical_data`
- **Method:** `GET`
- **Parameters:**
    - `year`: e.g., `2020`
    - `country`: e.g., `United States`
- **Response:**
    ```json
    {
        "AverageTemperature": 15.0,
        "AverageTemperatureUncertainty": 0.2
    }
    ```

### Get Emissions Data

- **URL:** `/emissions_data`
- **Method:** `GET`
- **Parameters:**
    - `year`: e.g., `2020`
    - `country`: e.g., `United States`
- **Response:**
    ```json
    {
        "methane": 150.0,
        "co2": 4000.0,
        "nitrous_oxide": 20.0
    }
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please create a pull request or open an issue to discuss what you would like to change.

## Acknowledgements

This project uses data from Kaggle and other sources for temperature and emissions data.
