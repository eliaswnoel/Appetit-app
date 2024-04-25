from django.shortcuts import render, redirect
import urllib
import os
import requests
from django.shortcuts import render, redirect
import environ
import json
from django.contrib.auth.models import User

from .models import Recipe

#  api .env
env = environ.Env()
environ.Env.read_env()
api_key = os.environ['TASTY_API_KEY']
api_host = os.environ['TASTY_HOST']

recipe_list = '/recipes/list'
tags_list = '/tags/list'
get_recipe = '/recipes/get-more-info'

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

def fetch_recipe_from_api(recipe_id):
  # Make a request to the third-party API to fetch the recipe data
  url = f'{api_host}{recipe_list}'
  querystring = {'id': recipe_id}
  headers = {
    'x-rapidapi-key': api_key,
    'x-rapidapi-host': "tasty.p.rapidapi.com"
  } 
  response = requests.request('GET', url, headers=headers, params=querystring)
  
  # Check if the request was successful
  if response.status_code == 200:
    # Parse the JSON response and return a Recipe object
    data = response.json()
    recipe_data = data['results']
    recipe = Recipe(
      external_id=recipe_data["id"],
      name=recipe_data["name"],
      description=recipe_data["description"],
      user = User.objects.get(username="llillianlayne")
    )
    print(recipe)
    return recipe
  else:
    # If the request was not successful, raise an exception
    raise Exception(f"Failed to fetch recipe with ID {recipe_id} from third-party API")