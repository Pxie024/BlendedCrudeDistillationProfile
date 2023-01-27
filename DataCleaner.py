import pandas as pd
import os
import numpy as np
import re

class CleanData():
    """
    This class is used to clean data scraped from https://www.crudemonitor.ca/

    Required inputs:
    ----
    base_path: str, the path that contains all data directories. 
    Default is the current working directory

    profile_name: str. The profile which we intent to clean. By default "distillation"
    """

    def __init__(self, base_path='.') -> None:
        self.base_path = base_path

    
    def clean_distillation(self) -> pd.DataFrame:

        data_folder = 'distillation_data'
        dir_path = os.path.join(self.base_path, data_folder)
        
        percentages = ['IBP', 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99]
        distill_data = {'percentage': percentages}
        
        for file in os.listdir(dir_path):
            if file.endswith('.csv'):
                file_path = os.path.join(dir_path, file)
                file_name = os.path.splitext(file)[0].replace(" ", "")
                df = pd.read_csv(file_path)
                df = df.replace('---', np.nan)
                df['recent_C'] = df['recent_C'].astype('float64')
                df['5_year_C'] = df['5_year_C'].astype('float64')
                df['Temparature'] = df['5_year_C']
                df['Temparature'].fillna(df.recent_C, inplace=True)
                distill_data[file_name] = df.Temparature.values
        
        distill_df = pd.DataFrame(data=distill_data)
        distill_df = distill_df.drop(0).reset_index(drop=True) # remove the row IBP 
        distill_df.set_index('percentage', inplace=True)
        
        self.oil_types = distill_df.columns.values # all oil types with available distillation data 

        return distill_df


    def clean_basic(self) -> pd.DataFrame:
        """
        OUTPUT:
        ------
        a pandas.DataFrame containing basic information for all crude oils who have 
        valid distillation profile. 
        """

        data_folder = 'basic_data'
        dir_path = os.path.join(self.base_path, data_folder)

        properties = ['Density(kg/m³)', 'Gravity(°API)', 'Sulphur(wt%)',
       'MicroCarbonResidue(wt%)', 'Nickel(mg/kg)', 'Vanadium(mg/kg)']
        basic_data = {"property": properties}

        for file in os.listdir(dir_path):
            if file.endswith('.csv'):
                file_path = os.path.join(dir_path, file)
                file_name = os.path.splitext(file)[0].replace(" ", "")
                if (file_name in self.oil_types) and (file_name != 'PremiumAlbianSynthetic(PAS)'):
                    df = pd.read_csv(file_path)
                    df = df.replace(['---', 'ND'], np.nan)
                    df = df[df["property"].isin(properties)].reset_index()
                    df["values"] = df['five_year']
                    df["values"].fillna(df.most_recent, inplace=True)
                    if len(df.values) == len(properties):
                        basic_data[file_name] = df["values"].values

        basic_df = pd.DataFrame(data=basic_data)
        return basic_df 



    def clean_lightends(self) -> pd.DataFrame:
        """
        OUTPUT:
        ------
        a pandas.DataFrame containing light ends components for all crude oils who have 
        valid distillation profile. 
        """
        
        data_folder = 'lightends_data'
        dir_path = os.path.join(self.base_path, data_folder)

        components = ['C3-(vol%)', 'iC4iso-Butane(vol%)', 'nC4n-Butane(vol%)',
       'iC5iso-Pentane(vol%)', 'nC5n-Pentane(vol%)', 'C6Hexanes(vol%)',
       'C7Heptanes(vol%)', 'C8Octanes(vol%)', 'C9Nonanes(vol%)',
       'C10Decanes(vol%)']
        lightends_data = {"property": components}

        for file in os.listdir(dir_path):
            if file.endswith('.csv'):
                file_path = os.path.join(dir_path, file)
                file_name = os.path.splitext(file)[0].replace(" ", "")
                if file_name in self.oil_types:
                    df = pd.read_csv(file_path)
                    df = df.replace(['---', 'ND'], np.nan)
                    df["values"] = df.five_year
                    df["values"].fillna(df.most_recent, inplace=True)
                    lightends_data[file_name] = df["values"]

        lightends_df = pd.DataFrame(data=lightends_data)
        return lightends_df 



    def clean_btex(self) -> pd.DataFrame:
        """
        OUTPUT:
        ------
        a pandas.DataFrame containing btex components for all crude oils who have 
        valid distillation profile. 
        """
        
        data_folder = 'btex_data'
        dir_path = os.path.join(self.base_path, data_folder)

        components = ['Benzene(vol%)', 'Toluene(vol%)', 'Ethylbenzene(vol%)',
       'Xylenes(vol%)']
        btex_data = {"property": components}

        for file in os.listdir(dir_path):
            if file.endswith('.csv'):
                file_path = os.path.join(dir_path, file)
                file_name = os.path.splitext(file)[0].replace(" ", "")
                if file_name in self.oil_types:
                    df = pd.read_csv(file_path)
                    df = df.replace(['---', 'ND'], np.nan)
                    df["values"] = df.five_year
                    df["values"].fillna(df.most_recent, inplace=True)
                    btex_data[file_name] = df["values"]

        btex_df = pd.DataFrame(data=btex_data)
        return btex_df 


    def get_x_y_data(self) -> pd.DataFrame:
        """
        Combining basic, light ends, and btex datas and return a large 
        dataframe containing all independent variables (X). The columns will 
        be all the features while the rows will be all different oil names with 
        valid distillation data. 
        """

        target_df = self.clean_distillation().T.astype(float)
        
        basic_df = self.clean_basic()
        lightends_df = self.clean_lightends()
        btex_df = self.clean_btex()

        feature_df = pd.concat([basic_df, lightends_df, btex_df]).set_index('property').T.astype(float)
        return feature_df, target_df



if __name__ == '__main__':
    data = CleanData()
    data.get_x_y_data()