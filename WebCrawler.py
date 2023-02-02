#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 21:27:19 2023

@author: paulxie
"""


import io
import pandas as pd
import os

import urllib.request
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import time
import re


# specify URL 
URL = "https://www.crudemonitor.ca/"



# Launch Chrome browser in headless mode
options = webdriver.ChromeOptions()
options.add_argument("headless")
browser = webdriver.Chrome(options=options)


if not os.path.exists("./distillation_data"):
    os.makedirs("./distillation_data")

if not os.path.exists("./basic_data"):
    os.makedirs("./basic_data")
    
if not os.path.exists("./lightends_data"):
    os.makedirs("./lightends_data")

if not os.path.exists("./btex_data"):
    os.makedirs("./btex_data")



class getProfiles():
    """
    Used to get information about Profiles for all crude oils 
    listed on https://www.crudemonitor.ca/
    """
    
    def __init__(self):
        self.browser = browser
        self.options = options
        self.URL = URL
        # load the webpage 
        self.browser.execute_script("window.open('%s', '_self');" % self.URL)

        # execute script to scroll down the page
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Get the number of macro-types
        sections = self.browser.execute_script("return document.getElementsByClassName('card home-card');")
        self.num_sections = len(sections)

    
    def get_all_profiles(self) -> None:
        for i in range(0, self.num_sections):
            oil_links = self.browser.execute_script("return document.getElementsByClassName('card home-card')[%d].\
                                              getElementsByTagName('li');" % i)
            oil_names = [link.text for link in oil_links]
            for j in range(len(oil_links)):
                oil_name = oil_names[j]
                print('getting information for ', oil_name)
                link = self.browser.execute_script("return document.getElementsByClassName('card home-card')[%d].\
                                              getElementsByTagName('li')[%d].getElementsByTagName('a')[0];" %(i,j))
                self.browser.execute_script("arguments[0].click();", link)  #clicking the links of each oil 
                
                # distillation profile 
                self.distillation_profile(oil_name)
                # basic profile 
                self.basic_profile(oil_name)
                # lightends profile 
                self.lightends_profile(oil_name)
                # btex profile
                self.btex_profile(oil_name)

                # reload the webpage 
                self.browser.execute_script("window.open('%s', '_self');" % URL)
                time.sleep(3)
        
        #convert .txt files into csv files 
        self.to_csv(profile_name='distillation')
        self.to_csv(profile_name='basic')
        self.to_csv(profile_name='lightends')
        self.to_csv(profile_name='btex')
    
    
    def distillation_profile(self, oil_name) -> None :
        """
        Returns
        -------
        None 
        This function will perform web scraping for distillation profiles for all 
        crude oils listed on https://www.crudemonitor.ca/. The results will be saved as 
        .txt files in the ./distillation_data/ directory. 
        """
        # get the distillation profile table using xpath
        distill_profile = self.browser.find_elements(By.XPATH, "//table[@id='HTSD']/tbody[1]")
        
        if len(distill_profile) >= 1:
            # write the data into a .txt file 
            file_path = './distillation_data/{}.txt'.format(oil_name)
            with open(file_path, 'w') as f:
                content = distill_profile[0].text
                f.write(content)
        
        
    def basic_profile(self, oil_name) -> None:
        # get the distillation profile table using xpath
        bas_profile = self.browser.find_elements(By.XPATH, "//table[@id='basic-analysis']/tbody[1]")
        
        if len(bas_profile) >= 1:
            # write the data into a .txt file 
            file_path = './basic_data/{}.txt'.format(oil_name)
            with open(file_path, 'w') as f:
                content = bas_profile[0].text
                content_items = content.split('\n')
                for line in content_items :
                    if ")" in line:
                        loc = re.search("\)", line).span()[0]
                        header = line[:loc+1]
                        data = line[loc+1:]
                        header = header.replace(' ','')
                        new_line = header + data + '\n'
                        f.write(new_line)
                    elif len(line.strip()):
                        f.write(line)
    
    
    
    def lightends_profile(self, oil_name) -> None:
        # get the distillation profile table using xpath
        le_profile = self.browser.find_elements(By.XPATH, "//table[@id='light-ends']/tbody[1]")
        
        if len(le_profile) >= 1:
            # write the data into a .txt file 
            file_path = './lightends_data/{}.txt'.format(oil_name)
            with open(file_path, 'w') as f:
                content = le_profile[0].text
                content_items = content.split('\n')
                for line in content_items :
                    if ")" in line:
                        loc = re.search("\)", line).span()[0]
                        header = line[:loc+1]
                        data = line[loc+1:]
                        header = header.replace(' ','')
                        new_line = header + data + '\n'
                        f.write(new_line)
                    elif len(line.strip()):
                        f.write(line)



    def btex_profile(self, oil_name) -> None:
        # get the distillation profile table using xpath
        bt_profile = self.browser.find_elements(By.XPATH, "//table[@id='BTEX']/tbody[1]")
        
        if len(bt_profile) >= 1:
            # write the data into a .txt file 
            file_path = './btex_data/{}.txt'.format(oil_name)
            with open(file_path, 'w') as f:
                content = bt_profile[0].text
                content_items = content.split('\n')
                for line in content_items :
                    if ")" in line:
                        loc = re.search("\)", line).span()[0]
                        header = line[:loc+1]
                        data = line[loc+1:]
                        header = header.replace(' ','')
                        new_line = header + data + '\n'
                        f.write(new_line)
                    elif len(line.strip()):
                        f.write(line)
    
    
    def to_csv(self, profile_name='distillation'):
        """
        convert all .txt files inside the given data directory into .csv files. 
        The original .txt files will be deleted.

        INPUT:
        ------
        profile_name: optional. By default "distillation" can take values in 
        ['distillation', 'basic', 'lightends', 'btex'].
        """
        assert profile_name in ['distillation', 'basic', 'lightends', 'btex']
        
        dir_path = './{}_data'.format(profile_name)

        # specifying header for each profile 
        if profile_name == 'distillation':
            header = ['percentage', 'recent_C', '5_year_C', 'recent_F', '5_year_F']
        if profile_name == 'basic':
            header = ['property', 'most_recent', 'six_month', 'one_year', 'five_year']
        if profile_name == 'lightends':
            header = ['property', 'most_recent', 'six_month', 'one_year', 'five_year']
        if profile_name == 'btex':
            header = ['property', 'most_recent', 'six_month', 'one_year', 'five_year']
        
        for file in os.listdir(dir_path):
            if file.endswith('.txt'):
                file_path = os.path.join(dir_path, file)
                file_name = os.path.splitext(file)[0]
                df = pd.read_csv(file_path, sep='\s+', header=None)
                csv_path = os.path.join(dir_path, '%s.csv'% file_name)
                df.to_csv(csv_path, header = header, index=False)
                os.remove(file_path)

    
    # def normailize_txt(self, file_path) -> None:
    #     """
    #     This function is used to normalize .txt files
    #     e.g. get rid of irregular spaces such as "BC Light (BCL)" -> "BCLight(BCL)"
    #     Those spaces will make rows to take different length, thus impossible to be 
    #     converted into .csv files.
    #     """

    #     with open(file_path, 'r+') as f:
    #         content = f.read()
    #         content_items = content.split('\n')
    #         for line in content_items :
    #             if ")" in line:
    #                 loc = re.search("\)", line).span()[0]
    #                 header = line[:loc+1]
    #                 data = line[loc+1:]
    #                 header = header.replace(' ','')
    #                 new_line = header + data + '\n'
    #                 f.write(new_line)
    #             elif len(line.strip()):
    #                 f.write(line)
    
    
    def close_browser(self):
        self.browser.close()


    
if __name__ == '__main__':
    oil_profiles = getProfiles()
    oil_profiles.get_all_profiles()

    





