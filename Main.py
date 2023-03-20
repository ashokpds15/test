from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from requests_futures import sessions

import time

import json



driver = webdriver.Chrome(ChromeDriverManager().install())

# Login details

username = 'MP520136'

password = 'Chaitra@2021'





def login():

  usernameField = driver.find_element_by_xpath(

    '/html/body/app-root/app-login/div/div/div[2]/form/div[1]/in')

  usernameField.send_keys(username)

  passwordField = driver.find_element_by_xpath('//*[@id="password-field"]')

  passwordField.send_keys(password)

  loginButton = driver.find_element_by_xpath(

    '/html/body/app-root/app-login/div/div/div[2]/form/div[3]/button')

  loginButton.click()

  time.sleep(15)





def get_tokens():

  try:

    driver.get('https://tms14.nepsetms.com.np/')

    login()

  except:

    pass

  hostSessionId = ''

  xsrf_token = ''

  cookie = ''

  for request in driver.requests:

    if request.url == 'https://tms14.nepsetms.com.np/tmsapi/user/frlist':

      hostSessionId = request.headers['Host-Session-Id']

      xsrf_token = request.headers['X-XSRF-TOKEN']

      cookie = request.headers['Cookie']

  return [hostSessionId, xsrf_token, cookie]





# Change variables here

price = 522.7

quantity = 10

securityId = 2911

exchangeSecurityId = 8018

tokens = get_tokens()



orderBook = {

  "orderBookExtensions": [{

    "orderTypes": {

      "id": 1,

      "orderTypeCode": "LMT"

    },

    "disclosedQuantity": 0,

    "orderValidity": {

      "id": 1,

      "orderValidityCode": "DAY"

    }

  }],

  "orders": [{

    "price": price,

    "quantity": quantity,

    "securityId": securityId,

    "exchangeSecurityId": exchangeSecurityId,

    "orderActionId": 1,

    "accountNumber": "",

    "traderId": "",

    "remarks": ""

  }]

}

payload = json.dumps({"orderBook": orderBook})

headers = {

  'Host': 'tms14.nepsetms.com.np',

  'User-Agent':

  'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36 Edg/111.0.1661.44',

  'Content-Type': 'application/json',

  'Request-Owner': '356920',

  'Host-Session-Id': tokens[0],

  'X-XSRF-TOKEN': tokens[1],

  'Cookie': tokens[2]

}



while True:

  try:

    session = sessions.FuturesSession(max_workers=10)

    [

      session.post('https://tms14.nepsetms.com.np/tmsapi/orderApi/orderbook',

                   data=payload,

                   headers=headers) for _ in range(1000)

    ]

  except:

    print("error")

