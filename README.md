# BlendedCrudeDistillationProfile
Using data science methods to build a model to predict the distillation profile of blended crude oils. 

This project consists of web crawling, data cleaning, model selection, training, and hyperparameter tuning, and finally deployment using Flask. A little bit of HTML was used to create a simple user interface. 

## Files: 
* `WebCrawler.py`: The Python module responsible for performing web scrapping. 
* `DataCleaner.py`: The Python module used to clean the web data and transform them to be ready for modelling.
* `CrudeBlendModel.py`: Main logic for blending rules and machine learning models. 
* `main.py`: The file that automates every step and creates a simple user interface. 
* `templates`: The directory which contains some HTML files for the UI. 
* `solution_summary.ipynb`: A summary of the solution I used to solve this project.
* `solution_summary.pdf`: A pdf version of `solution_summary.ipynb`
* `TestDataCleaner.py`: Unit test for the module `DataCleaner.py`. Includes a couple simple test cases.

To run this program on your local computer, clone this directory, and run `main.py` using Python. It will take a few minutes for the server to get started. The web application will run on your localhost.
