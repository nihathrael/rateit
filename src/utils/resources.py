'''
Created on 02.06.2011

@author: moritz
'''
import os

def get_resource_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))