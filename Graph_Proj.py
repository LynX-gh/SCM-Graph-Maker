import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

def loadenv():
    load_dotenv('Cookies.env')
    cookie = {'steamLogin' : os.getenv('steamLogin'), 
              'sessionid' : os.getenv('sessionid'), 
              'steamparental' : os.getenv('steamparental'),
              'steamRememberLogin' : os.getenv('steamRememberLogin'), 
              'steamMachineAuthsteamID64' : os.getenv('steamMachineAuthsteamID64')
              }
    return cookie

def plot(skins, cookie):
    #Intitialize the axes
    plt.style.use('seaborn')
    plt.clf()
    fig = plt.figure()
    ax = plt.axes()

    #Create a plot for each skin
    for skin, market_hash in skins.items():
        param = ['US', '1', market_hash]
        url = 'https://steamcommunity.com/market/pricehistory/?country={}&currency={}&appid=730&market_hash_name={}'.format(param[0], param[1], param[2])

        response = requests.get(url, cookies = cookie)
        data = response.json()

        price_df = pd.DataFrame(data['prices'])
        price_df.columns = ['Date', 'Price', 'Items']

        price_df['Date'] = price_df['Date'].str[:-7]
        price_df['Date'] = pd.to_datetime(price_df['Date'], format = '%b %d %Y')
        price_df['Price'] = price_df['Price']/74.18

        price_df_clean = price_df.groupby('Date', as_index = False).mean()
        price_df_clean.to_csv('Data\\{}.csv'.format(skin))
        price_df_clean.plot(y = 'Price', x = 'Date', ax = ax, label = skin, alpha = 0.8)

    #Set labels and grid
    ax.set_xlabel('Days After Release')
    ax.set_ylabel('SCM Price USD')
    plt.grid()

    #Save the graph and show on screen
    plt.savefig('plot3.svg', dpi=300)
    plt.show()

if __name__ == "__main__":
    skins = {'Bravo Case' : 'Operation%20Bravo%20Case', 
             'Phoenix Case' : 'Operation%20Phoenix%20Weapon%20Case',
             'Breakout Case' : 'Operation%20Breakout%20Weapon%20Case',
             'Vanguard Case' : 'Operation%20Vanguard%20Weapon%20Case',
             'Falchion Case' : 'Falchion%20Case',
             'Wildfire Case' : 'Operation%20Wildfire%20Case',
             'Hydra Case' : 'Operation%20Hydra%20Case',
             'Shattered Web' : 'Shattered%20Web%20Case',
             'Broken Fang' : 'Operation%20Broken%20Fang%20Case'
             }
    cookies = loadenv()
    plot(skins, cookies)
