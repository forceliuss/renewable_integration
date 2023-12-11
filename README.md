# Renewable Integration
## Integration of renewable energy analysis dashboard

This is an experimental project!! The main objective of this project is to create a dashboard to analyze the data from several sources and develop a common place for these insights. This project gets most of the datasets from Kaggle. (links below)

## Datasets

* Renewable Energy (1960 - 2023)
<a href='https://www.kaggle.com/datasets/imtkaggleteam/renewable-energy-1960-2023' target='_blank'>Kaggle dataset</a>

* World GDP by Country (1960 - 2022)
<a href='https://www.kaggle.com/datasets/sazidthe1/world-gdp-data' target='_blank'>Kaggle dataset</a>

* Coming soon

## Code focus objectives

 - Import and clear the data from the datasets
 - Combine all the different sources into a main dataframe
 - Analyze the dataframe and create metrics
 - Create a local dashboard (StreamLit)
 - Sort the global datasets by countries
 - Use the Prophet model, to predict some values for integration metrics (FUTURE)

## Libraries

* Pandas -`pip install pandas`
* Numpy -`pip install numpy`
* StreamLit -`pip install streamlit`
* Matplotlib -`pip install matplotlib`
* Prophet (FUTURE) -`pip install prophet`

## How to run

1.Clone this project
2.Run your python kernel
3.Install all the libraries above
4.Run `main.py` through the streamlit command `streamlit run main.py`

## Disclaiming

WHEN WORKING ON THE LOCAL JUPYTER NOTEBOOKS(`main.ipynb`, `draft.ipynb`) TO DEBUG, REMEMBER TO CHANGE A (.) ON THE CSV FILE PATH ON THE `cleaning.ipynb`. :)