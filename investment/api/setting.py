#  -*- coding:utf-8 -*-
# 火币配置信息
huobi_setting = {
    #APIKEY
    'ACCESS_KEY' : "4fe092e2-60ac39e8-06675103-e8209",
    'SECRET_KEY' : "e0d3a7a6-589d7d3d-b04f7461-125ea",
    # API 请求地址
    'MARKET_URL' : "https://api.huobi.pro",
    'TRADE_URL' : "https://api.huobi.pro",
    #REST API GET请求 header信息
    'GET_HEADERS' : {
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    },
    #REST API POST请求 header信息
    'POST_HEADERS' : {
        "Accept": "application/json",
        'Content-Type': 'application/json'
    },

    'ORDER_PLACE_URL' : '/v1/order/orders/place',

}

# 币安配置信息
bian_setting = {
    # API key
    'api_key':"YEHLgYLaa24asbNg2h2XLi9nCZJSi2yHANm1erW1WWt4COIvAl0z0GiDH3xGFUXC",
    'api_secret':"zU7FjB1LTrsrxUFaMZu0Vwxewy9FQhlYOkkUhxeiXbmGSVbVe82991KbE8bQAeLU",
    # API 请求地址
    'API_URL': 'https://api.binance.com/api'

}

# fcoin配置信息
fcoin_setting = {
    # TODO 待完成
'base_url':'https://api.fcoin.com/v2/',
'key' : '55b6353945d14944bece3b5bc8d42580',
'secret' : 'e5f615e4d88d47a082a1b0f263fb8309',
'ft' : {'name': 'xrpusdt', 'coin': 'ft', 'price_precision': 6, 'amount_precision': 0, 'min_amount': 5}
}

# okcoin配置信息
okcoin_setting = {
    'apikey':'0a5ba5fe-2ce4-4f2a-b308-1f6f17d3e6ec',
    'secretkey':'82B69BD2B7DBBABF726D046C37C7969F',
    'okexRESTURL':'https://www.okex.com'
}
okex_headers = {
            "Content-type" : "application/x-www-form-urlencoded",
     }

