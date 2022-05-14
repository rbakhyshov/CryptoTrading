import requests, google_trends as gt
import ftx


def get_info():
    response = requests.get(url="https://yobit.net/api/3/info")

    with open("info.txt", "w") as file:
        file.write(response.text)

    return response.text


def get_ticker(coin1="btc", coin2="usd"):
    # response = requests.get(url="https://yobit.net/api/3/ticker/eth_btc-xrp_btccc?ignore_invalid=1")
    response = requests.get(url=f"https://yobit.net/api/3/ticker/{coin1}_{coin2}?ignore_invalid=1")

    with open("ticker.txt", "w") as file:
        file.write(response.text)

    return response.text


def get_depth(coin1="btc", coin2="usd", limit=150):
    response = requests.get(url=f"https://yobit.net/api/3/depth/{coin1}_{coin2}?limit={limit}&ignore_invalid=1")

    with open("depth.txt", "w") as file:
        file.write(response.text)

    bids = response.json()[f"{coin1}_usd"]["bids"]

    total_bids_amount = 0
    for item in bids:
        price = item[0]
        coin_amount = item[1]

        total_bids_amount += price * coin_amount

    return f"Total bids: {total_bids_amount} $"


def get_trades(coin1="btc", coin2="usd", limit=150):
    response = requests.get(url=f"https://yobit.net/api/3/trades/{coin1}_{coin2}?limit={limit}&ignore_invalid=1")

    with open("trades.txt", "w") as file:
        file.write(response.text)

    total_trade_ask = 0
    total_trade_bid = 0

    for item in response.json()[f"{coin1}_{coin2}"]:
        if item["type"] == "ask":
            total_trade_ask += item["price"] * item["amount"]
        else:
            total_trade_bid += item["price"] * item["amount"]

    info = f"[-] TOTAL {coin1} SELL: {round(total_trade_ask, 2)} $\n[+] TOTAL {coin1} BUY: {round(total_trade_bid, 2)} $"

    return info


def main():
    #print(get_info())

    client = ftx.FtxClient()
    result = client.get_trades('DOGEBULL/USD')
    result = client.get_orderbook('DOGEBULL/USD', 1)

    print(result)

    #tr = pytrends.TrendReq(hl='ru-RU', tz=360)
    #kw_list = ["Blockchain"]
    #pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')



    print(get_ticker())
    # print(get_ticker(coin1="eth"))
    # print(get_depth())
    #print(get_depth(coin1="doge"))
    # print(get_depth(coin1="doge", limit=2000))
    # print(get_trades())
    #print(get_trades(coin1="btc"))
    #print(get_trades(coin1="doge", coin2= "usd"))




if __name__ == '__main__':
    main()