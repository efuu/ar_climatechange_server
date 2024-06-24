## Prerequisites

- Python version >= 3.7, <3.11; download at https://www.python.org/
- pip

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/efuu/ar_climatechange_server.git
    cd ar_climatechange_server
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

   if using conda:
   ```bash
   conda create --name climatechange-server python
   ```

4. Activate the virtual environment:

    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
        or if using conda:
        ```bash
        conda activate climate-prediction
        ```
    - On macOS:
        ```bash
        source venv/bin/activate
        ```

5. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Server

1. Make sure you are in the project directory and your virtual environment is activated.

2. Start the Flask server:
    ```bash
    python app.py
    ```

3. The server will start on `http://127.0.0.1:5000` by default.

4. Run the unity file and it should be able to connect with the local server. 

## Acknowledgements

This project uses data from [https://ourworldindata.org/co2-and-greenhouse-gas-emissions](https://ourworldindata.org/co2-and-greenhouse-gas-emissions)
