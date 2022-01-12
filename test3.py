import streamlit as st
import pandas as pd
import numpy as np
import requests
import json

st.title('Yoba Unchained')

card_url = 'https://api.x.immutable.com/v1/orders?direction=asc&include_fees=true&order_by=buy_quantity&page_size=1&sell_token_address=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c&sell_token_type=ERC721&status=active&sell_token_name="%s"&sell_metadata={"quality":["Meteorite"]}&buy_token_type=ETH'
card_url_gds = 'https://api.x.immutable.com/v1/orders?direction=asc&include_fees=true&order_by=buy_quantity&page_size=1&sell_token_address=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c&sell_token_type=ERC721&status=active&sell_token_name="%s"&sell_metadata={"quality":["Meteorite"]}&buy_token_address=0xccc8cb5229b0ac8069c51fd58367fd1e622afd97'
gecko_url = 'https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=ethereum,gods-unchained'
card_info_url = 'https://api.x.immutable.com/v1/assets/0xacb3c6a43d15b907e8433077b6d38ae40936fe2c/%s?include_fees=true'

top_cards = []
json_cards = []
price_eth = np.NaN
price_gds= np.NaN
card_id = ''
sample = {'proto': 1, 'name': 'name', 'god': 'god', 'set': 'set', 'rarity': 'rarity', 'mana': 'mana', 'effect': 'effect', 'eth_price': 'eth_price', 'eth_price_in_usd': 'eth_price_in_usd',
'gds_price': 'gds_price', 'gds_price_in_usd': 'gds_price_in_usd', 'diff': 'diff' }
records = []

with open('cards_top.txt') as my_file:
    top_cards = my_file.readlines()

def load():
    #records = []
    response = requests.get(gecko_url)
    usd = response.json()
    eth_usd = usd['ethereum']['usd']
    gds_usd = usd['gods-unchained']['usd']
    print(eth_usd)
    for card in top_cards:
        record = {}
        response = requests.get(card_url % card)
        response2 = requests.get(card_url_gds % card)
        data = response.json()
        data = data['result']
        if not data:
            pass
        else:
            card_name = data[0]["sell"]["data"]["properties"]["name"]
            card_id = data[0]["sell"]["data"]["id"]
            response_info = requests.get(card_info_url % card_id)
            card_info = response_info.json()
            record['name'] = card_info['metadata']['name']
            record['god'] = card_info['metadata']['god']
            record['set'] = card_info['metadata']['set']
            record['rarity'] = card_info['metadata']['rarity']
            record['mana'] = card_info['metadata']['mana']
            record['effect'] = card_info['metadata']['effect']
            #records.append(record)
            #print(record)
            decimal_eth = int(data[0]["buy"]["data"]["decimals"])
            quantity_eth = int(data[0]["buy"]["data"]["quantity"])
            price_eth = (quantity_eth / pow(10, decimal_eth))
            record['eth_price'] = price_eth

            data2 = response2.json()
            data2 = data2['result']
            if not data2:
                pass
            else:
                decimal_gds = int(data2[0]["buy"]["data"]["decimals"])
                quantity_gds = int(data2[0]["buy"]["data"]["quantity"])
                price_gds = (quantity_gds / pow(10, decimal_gds))
                #print(decimal_gds, " ", quantity_gds)
                record['gds_price'] = price_gds


                price_eth_in_usd = price_eth*eth_usd
                price_gds_in_usd = price_gds*gds_usd
                record['eth_price_in_usd'] = price_eth_in_usd
                record['gds_price_in_usd'] = price_gds_in_usd
                diff = price_gds_in_usd - price_eth_in_usd
                record['diff'] = diff
                perc1 = price_eth_in_usd * 0.01
                record['diff %'] = int(diff / perc1)

            records.append(record)
            
            #print(record)

        #json_cards.append(data)

    print(records)


def load_data(nrows):

    #cf = {'Name of card': data['name'], 'Set': data['set'], 'Rarity': data['rarity'], 'God': data['god'], 'Mana': data['mana'], 'Involved Effects': data['effect']}
    #json.d
    #cards = pd.read_json('cards.json')
    #cards = pd.json_normalize(cards['records'])
    #print(cards['name'])
    #cards = cards.loc(cards['name'].isin(top_cards))
    #card_frame = pd.DataFrame([[data['name'], data['set'], data['rarity'], data['god'], data['mana'], data['effect']]])
    #print(card_frame)
    #card_data = card_data.append(cf, ignore_index=True)
    
    #data = pd.read_json(card_url)
    #pd.json_normalize(data[0]['result'])
    #data = pd.json_normalize(data)
    #print(card_frame)
    load()
    #data.rename(lowercase, axis='columns', inplace=True)
    #data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    #result = pd.json_normalize(data["result"])
    cards = pd.DataFrame(records)
    return cards

data_load_state = st.text('Loading data...')
data = load_data(1)
data_load_state.text("Done!")


st.write(data)

#st.subheader('Number of pickups by hour')
#hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
#st.bar_chart(hist_values)

# Some number in the range 0-23
#hour_to_filter = st.slider('hour', 0, 23, 17)
#filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

#st.subheader('Map of all pickups at %s:00' % hour_to_filter)
#st.map(filtered_data)