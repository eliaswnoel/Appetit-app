from django.shortcuts import render, redirect

import os
import requests
from django.shortcuts import render, redirect
import environ
import json

#  api .env
env = environ.Env()
environ.Env.read_env()
api_key = os.environ['TASTY_API_KEY']
api_host = os.environ['TASTY_HOST']


def getPopularRecipes(num):
  url = f'https://tasty.p.rapidapi.com/recipes/list'
  querystring = {"from":"0","size":{num},"tags":"under_30_minutes"}
  headers = {
    'x-rapidapi-key': api_key,
    'x-rapidapi-host': "tasty.p.rapidapi.com"
  } 
  
  response = requests.request("GET", url, headers=headers, params=querystring)
  data = response.json()
  return(data)









