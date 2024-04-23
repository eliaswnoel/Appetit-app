from django.shortcuts import render, redirect
import urllib
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



def accessAPI(end_url, string, method): 
  # end_url access the api at a given end point
  # find end points on https://rapidapi.com/apidojo/api/tasty
  url = f'{api_host}{end_url}'
  # remove whitespace froms url

  # add the parameters as a string
  querystring = string
  # headers stay the same
  headers = {
    'x-rapidapi-key': api_key,
    'x-rapidapi-host': "tasty.p.rapidapi.com"
  } 

  # response retrieves the data from the api
  response = requests.request(method, url, headers=headers, params=querystring)
  # convert the response to json
  data = response.json()
  return (data)
