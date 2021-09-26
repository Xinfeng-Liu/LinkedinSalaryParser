#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 00:25:28 2021

@author: Xinfeng Liu(xinfengl@umich.edu)
"""

import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class SalaryParser:
    '''
    Note:
        1. self.path needs to change to your own path
        2. email & passward in LinkedinParser was set to empty by default, 
           please add your own email & password
    '''
    def __init__(self):
        self.company_name = []
        self.title = []
        self.sum_list = []
        self.salary = []
        # define webdriver path
        self.path = '/Users/xinfengliu/Desktop/chromedriver'
    
    def LinkedinParser(self):
        driver = webdriver.Chrome(self.path)
        driver.get("https://www.linkedin.com/login")
        
        #login to linkedin
        email = ''
        password = ''
        time.sleep(2)
        driver.find_element_by_id('username').send_keys(email)
        driver.find_element_by_id('password').send_keys(password)
        driver.find_element_by_id('password').send_keys(Keys.RETURN)
        time.sleep(2)
        
        #open linkedin salary page
        driver.get("https://www.linkedin.com/salary/")
        time.sleep(2)
        
        #input company name & title into search box
        for i in self.sum_list:
            search = driver.find_element(By.XPATH, '//div[@role="combobox"]/input')
            search.send_keys(i)
        
            #click on "search"
            search_button = driver.find_element(By.XPATH, '//div[@class="search-box"]/div[@class="user-search-input-container"]/div[@class="search-button-container"]/button')
            search_button.send_keys(Keys.RETURN)
            time.sleep(2)
        
            #return the salary info
            try:
                result = driver.find_element(By.XPATH,'//span[@class="searchTopCard__baseCompensation"]').text
                self.salary.append(result)
            except NoSuchElementException:
                print(f'{i} was not found on Linkedin salary website')
                self.salary.append(" ")
            
            #clear the precious search result
            previous_search = driver.find_element(By.XPATH, '//div[@role="combobox"]/input')
            previous_search.clear()
        driver.close()
        return 
    
    def file_manipulation(self):
        #read the file
        df = pd.read_csv('PythonTesting_20210924.csv')
        
        #create company+title list
        for i in df['company']:
            self.company_name.append(i)
            
        for i in df['title']:
            self.title.append(i)
            
        for item1,item2 in zip(self.company_name,self.title):
            self.sum_list.append(item1 + " " + item2)
        
        #start parsing the website
        self.LinkedinParser()
        
        #add salary info to dataframe
        df['salary'] = self.salary
        
        # export as csv file
        df.to_csv('linkedin_salary_info.csv',index= False)
        return
    
    
parser = SalaryParser()
parser.file_manipulation()

        