import streamlit as st
import numpy as np
import pandas as pd
import requests
import json


colours = {
	'normal': '#A8A77A',
	'fire': '#EE8130',
	'water': '#6390F0',
	'electric': '#F7D02C',
	'grass': '#7AC74C',
	'ice': '#96D9D6',
	'fighting': '#C22E28',
	'poison': '#A33EA1',
	'ground': '#E2BF65',
	'flying': '#A98FF3',
	'psychic': '#F95587',
	'bug': '#A6B91A',
	'rock': '#B6A136',
	'ghost': '#735797',
	'dragon': '#6F35FC',
	'dark': '#705746',
	'steel': '#B7B7CE',
	'fairy': '#D685AD',
}

#Get a random pokedex number
# random_number = str(np.random.randint(0, 720))
# random_number_2 = str(np.random.randint(0, 720))

## For random pokemons
# print(all_pokemon)
#Fetch the name of that pokemon 
# def get_random_pokemon(number:int) -> str:
#     try: 
#         url = 'https://pokeapi.co/api/v2/pokemon/'+number
#         response = requests.get(url)
#         data = response.json()
#     except Exception as e:
#         st.write(f'Error: {e}')
#         data = None
#     return data.get('name')

# poke_name = get_random_pokemon(random_number)
# poke_name_2 = get_random_pokemon(random_number_2)
######################################################################################################



file = open('pokemon-list-en.txt', 'r')
all_pokemon = list(file.readlines())
all_pokemon = [pokemon.strip() for pokemon in all_pokemon]

def get_pokemon_data(pokemon_name) -> dict:
    try: 
        url = 'https://pokeapi.co/api/v2/pokemon/'+pokemon_name
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        st.write(f'Error: {e}')
        data = None
    return data
