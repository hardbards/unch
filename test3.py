import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
from io import StringIO
import cards as cs

st.title('Yoba Unchained')

#card_url = 'https://api.x.immutable.com/v1/orders?direction=asc&include_fees=true&order_by=buy_quantity&page_size=1&sell_token_address=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c&sell_token_type=ERC721&status=active&sell_token_name="%s"&sell_metadata={"quality":["Meteorite"]}&buy_token_type=ETH'
#card_url_gds = 'https://api.x.immutable.com/v1/orders?direction=asc&include_fees=true&order_by=buy_quantity&page_size=1&sell_token_address=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c&sell_token_type=ERC721&status=active&sell_token_name="%s"&sell_metadata={"quality":["Meteorite"]}&buy_token_address=0xccc8cb5229b0ac8069c51fd58367fd1e622afd97'
cards_url_eth_proto = 'https://api.x.immutable.com/v1/orders?direction=asc&include_fees=true&order_by=buy_quantity&page_size=1&sell_token_address=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c&sell_token_type=ERC721&status=active&sell_metadata={"proto":["%s"],"quality":["Meteorite"]}&buy_token_type=ETH'
cards_url_gds_proto = 'https://api.x.immutable.com/v1/orders?direction=asc&include_fees=true&order_by=buy_quantity&page_size=1&sell_token_address=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c&sell_token_type=ERC721&status=active&sell_metadata={"proto":["%s"],"quality":["Meteorite"]}&buy_token_address=0xccc8cb5229b0ac8069c51fd58367fd1e622afd97'
gecko_url = 'https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=ethereum,gods-unchained'
#card_info_url = 'https://api.x.immutable.com/v1/assets/0xacb3c6a43d15b907e8433077b6d38ae40936fe2c/%s?include_fees=true'


top_cards = []
json_cards = []
price_eth = np.NaN
price_gds= np.NaN
card_id = ''
records = []

def load():
    print('Hello')
    #records = []
    response = requests.get(gecko_url)
    usd = response.json()
    eth_usd = usd['ethereum']['usd']
    gds_usd = usd['gods-unchained']['usd']
    print(eth_usd)
    for card_name in top_cards:
        print(card_name)
        record = {}
        proto_id = False
        current_card_info = []
        #card_keys = cs.cards_new.keys()
        #print(card_keys)
        if card_name not in top_cards:
            print('Not in')
            pass
        else:
            proto_id = cs.cards_new[card_name][0]
            print(proto_id)
        if proto_id:
            response = requests.get(cards_url_eth_proto % proto_id)
            data = response.json()
            try:
                data = data['result']
            except:
                data = []
            if not data:
                pass
            else:
                record['name'] = card_name
                record['god'] = cs.cards_new[card_name][1]
                record['set'] = cs.cards_new[card_name][2]
                record['rarity'] = cs.cards_new[card_name][3]
                record['mana'] = cs.cards_new[card_name][4]
                record['effect'] = cs.cards_new[card_name][5]

                decimal_eth = int(data[0]["buy"]["data"]["decimals"])
                quantity_eth = int(data[0]["buy"]["data"]["quantity"])
                price_eth = (quantity_eth / pow(10, decimal_eth))
                record['eth_price'] = price_eth

                response2 = requests.get(cards_url_gds_proto % proto_id)
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
    #print(records)

def load_data():
    load()
    cards = pd.DataFrame(records)
    return cards

def convert_df(df):
    return df.to_csv().encode('utf-8')

uploaded_file = st.file_uploader("Choose a file")
if st.button('Load'):
    if uploaded_file is not None:
        top_cards = StringIO(uploaded_file.getvalue().decode("utf-8")).read().splitlines()
        print(top_cards)
    else:
        st.write("Default file will be loaded")
        with open('cards_top.txt') as my_file:
            top_cards = my_file.read().splitlines()
    data_load_state = st.text('Loading data...')
    data = load_data()
    data_load_state.text("Done!")
    st.write(data)
    csv = convert_df(data)
    st.download_button(
    "Download CSV",
    csv,
    "result.csv",
    "text/csv",
    key='result-data'
)
