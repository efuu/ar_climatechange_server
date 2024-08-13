```markdown
# Climate Change Prediction AR Application

## Table of Contents
- [Overview](#overview)
- [Scenes](#scenes)
  - [Historical Temperature](#historical-temperature)
  - [Temperature Prediction](#temperature-prediction)
- [Earth Model Red Factor](#earth-model-red-factor)
- [Data Processing](#data-processing)
  - [Historical Temperature Data](#historical-temperature-data)
  - [Future Prediction Data](#future-prediction-data)
- [How to Use](#how-to-use)
- [Dependencies](#dependencies)
- [Future Work](#future-work)

## Overview

The Climate Change Prediction AR Application is an educational tool that allows users to visualize the changes in global temperatures, both historically and predicted for the future. The application leverages Unity and AR Foundation to provide an interactive experience where users can observe how temperature variations impact different countries around the world.

The application is divided into two main scenes:
1. **Historical Temperature**: Shows the actual historical temperature data from 1901 to 2020.
2. **Temperature Prediction**: Predicts temperature increases from 2020 to 2099 based on various climate scenarios.

## Scenes

### Historical Temperature

In this scene, the application reads historical temperature data from a file and displays the corresponding temperature for each year. The year can be adjusted using a slider, and the temperature is shown both numerically and visually on an Earth model. The Earth model adjusts its "red factor" to represent increasing temperatures by making countries appear more red.

### Temperature Prediction

This scene uses future climate scenario data to predict temperature increases from 2020 to 2099. Users can select different climate scenarios (e.g., SSP1-1.9, SSP1-2.6, SSP2-4.5, SSP3-7.0, SSP5-8.5) from a dropdown menu and adjust the year using a slider. Similar to the historical scene, the predicted temperature increase is displayed numerically and visually by adjusting the "red factor" on the Earth model.

## Earth Model Red Factor

The Earth model visualizes temperature increases by adjusting the redness of each country. The redness is controlled by the `UpdateRedFactorForAllCountries` method in the `WorldMapManager` script. This method adjusts the `_redFactor` value in the shader for each country's material.

### Code Snippet: Update Red Factor
```csharp
public void UpdateRedFactorForAllCountries(float value)
{
    foreach (Country country in countries)
    {
        if (country != null && country.meshRenderer != null)
        {
            // Instead of creating a new material each time, modify the existing one
            Material material = country.meshRenderer.material;
            material.SetFloat("_redFactor", value);
        }
    }
}
```

### Shader Code
```csharp
float4 moreRedColor = lerp(float4(hsvTorgb391, 0.0), float4(1.0, 0.0, 0.0, 1.0), _redFactor);
lerpResult392 = lerp(temp_output_372_0, moreRedColor, _VertexColorTint);
//changed stripe value * 2
float4 CountriesEmission152 = ( ( StripesMaskCountries335 * temp_output_109_0 * _StripesValue * 10 ) + ( BordersMask144 * temp_output_109_0 * NoiseAnimSmall300 * 3) + lerpResult392 );
//CountriesEmission152 = lerp(CountriesEmission152, float4(1.0, 0.0, 0.0, 1.0), _redFactor);
//float4 temptest = lerp(CountriesEmission152, float3(1.0,0.0,0.0), 0.5);

//CountriesEmission152 = lerp(CountriesEmission152, intermediateColor, _redFactor);

CountriesEmission152 = lerp(CountriesEmission152, moreRedColor, _redFactor);
```

## Data Processing

### Historical Temperature Data

The historical temperature data is read from a file located in the `Assets/StreamingAssets/temperatures` directory. The data is stored in a dictionary where the key is the year and the value is the temperature.

### Code Snippet: Historical Temperature Data Processing
```csharp
Dictionary<int, float> ReadTemperatureFile(string filePath)
{
    string persistentFilePath = Path.Combine(Application.persistentDataPath, filePath);

    string directoryPath = Path.GetDirectoryName(persistentFilePath);
    if (!Directory.Exists(directoryPath))
    {
        Directory.CreateDirectory(directoryPath);
    }

    if (!File.Exists(persistentFilePath))
    {
        Debug.Log("Copying file from StreamingAssets to PersistentDataPath...");
        string streamingFilePath = Path.Combine(Application.streamingAssetsPath, filePath);

        if (Application.platform == RuntimePlatform.Android)
        {
            WWW reader = new WWW(streamingFilePath);
            while (!reader.isDone) { }
            File.WriteAllBytes(persistentFilePath, reader.bytes);
        }
        else
        {
            File.Copy(streamingFilePath, persistentFilePath);
        }
    }

    if (!File.Exists(persistentFilePath))
    {
        Debug.LogError("File not found: " + persistentFilePath);
        return null;
    }

    string[] lines = File.ReadAllLines(persistentFilePath);
    Dictionary<int, float> yearlyTemperatures = new Dictionary<int, float>();

    for (int i = 4; i < lines.Length; i++)
    {
        string line = lines[i].Trim();
        if (!string.IsNullOrWhiteSpace(line))
        {
            string[] parts = line.Split(new char[] { ' ' }, System.StringSplitOptions.RemoveEmptyEntries);
            if (int.TryParse(parts[0], out int year))
            {
                if (float.TryParse(parts[parts.Length - 1], out float annValue))
                {
                    yearlyTemperatures[year] = annValue;
                }
                else
                {
                    Debug.LogError("Failed to parse float value on line: " + (i + 1));
                }
            }
            else
            {
                Debug.LogError("Failed to parse year on line: " + (i + 1));
            }
        }
    }

    return yearlyTemperatures;
}
```

### Future Prediction Data

The future temperature predictions are read from CSV files stored in the `Resources/forecasts/` directory. The predictions vary by scenario, and the data is stored in a dictionary where the key is the scenario name and the value is another dictionary mapping years to temperature changes.

### Code Snippet: Future Prediction Data Processing
```csharp
void LoadCSVData(string filePath, string scenario)
{
    TextAsset csvFile = Resources.Load<TextAsset>(filePath);
    if (csvFile == null)
    {
        Debug.LogError($"CSV file not found at path: {filePath}");
        return;
    }

    var lines = csvFile.text.Split(new[] { '\n' }, System.StringSplitOptions.RemoveEmptyEntries);
    Dictionary<int, float> yearData = new Dictionary<int, float>();
    foreach (var line in lines.Skip(1))
    {
        var values = line.Split(',');
        if (values.Length < 3)
        {
            Debug.LogError($"Invalid line format: {line}");
            continue;
        }

        if (!float.TryParse(values[0].Trim(), System.Globalization.NumberStyles.Float, System.Globalization.CultureInfo.InvariantCulture, out float yearFloat))
        {
            Debug.LogError($"Invalid year format: {values[0]}");
            continue;
        }

        int year = Mathf.RoundToInt(yearFloat);

        if (!float.TryParse(values[2].Trim(), System.Globalization.NumberStyles.Float, System.Globalization.CultureInfo.InvariantCulture, out float meanTemperature))
        {
            Debug.LogError($"Invalid temperature format: {values[2]}");
            continue;
        }

        yearData[year] = meanTemperature;
    }
    scenarioData[scenario] = yearData;
}
```

## How to Use

1. **Historical Temperature Scene**:
    - Use the year slider to select a year between 1901 and 2020.
    - Observe the temperature value for the selected year and watch the Earth model adjust in redness.

2. **Temperature Prediction Scene**:
    - Select a climate scenario from the dropdown menu.
    - Use the year slider to select a year between 2020 and 2099.
    - Observe the predicted temperature increase and the corresponding change in the Earth's redness.

## Dependencies

- **Unity 2021.3+**
- **AR Foundation 5.1**
- **Michsky's Modern UI Pack (MUIP)**
- **TextMeshPro**
- **SceneManager**

## Future Work

- **Additional Scenarios**: Incorporate more climate scenarios and extend the prediction range.
- **Improved Visualization**: Enhance the shader effects for better visual representation of temperature changes.
- **User Feedback Integration**: Gather user feedback to refine and improve the application’s educational effectiveness.
```
