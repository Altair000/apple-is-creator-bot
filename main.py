import base64
import json
from curl_cffi import requests
from bs4 import BeautifulSoup

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'

def home():
    # EXTRACCIÓN DE TOKENS DE APPLE ######################
    url = 'https://appleid.apple.com/widget/account/?roleType=Agent&lv=0.3.17&widgetKey=af1139274f266b22b68c2a3e7ad932cb3c0bbe854e13a79af78dcc73136882c3&v=3&appContext=account'
    home = requests.get(url, headers={'User-Agent': UA})
    soup = BeautifulSoup(home.text, 'html.parser')
    tokens_place = soup.find('script', {'id': 'boot_args'})
    json_data = json.loads(tokens_place.string)
    scnt = json_data.get('direct', {}).get('scnt')
    widgetKey = json_data.get('direct', {}).get('widgetKey')
    sessionId = json_data.get('direct', {}).get('sessionId')
    ########################################################
    return scnt, widgetKey, sessionId
# CÓDIGO DE SOLICITUDES ################################
def get_captcha(scnt, widgetKey, sessionId):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://appleid.apple.com',
        'Referer': 'https://appleid.apple.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': UA,
        'X-Apple-I-FD-Client-Info': '{"U":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0","L":"es","Z":"GMT-05:00","V":"1.1","F":"Nta44j1e3NlY5BNlY5BSmHACVZXnNA9Z39VdCp_.5y.ptIV69LarUqUdHz16uBxLNlYJPuVg91k3sdmcK5rT_yQgzApyYEKaBNlY5BPY25BNnOVgw24uy.1Y."}',
        'X-Apple-I-TimeZone': 'America/Havana',
        'X-Apple-ID-Session-Id': sessionId,
        'X-Apple-Request-Context': 'create',
        'X-Apple-Widget-Key': widgetKey,
        'scnt': scnt,
        'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'type': 'IMAGE',
    }

    captcha = requests.post('https://appleid.apple.com/captcha', headers=headers, json=json_data)
    if captcha.status_code == 200 or 201:
        captcha_json = captcha.json()
        captcha_img_encode = captcha_json['payload']['content']
        captcha_img_decode = base64.b64decode(captcha_img_encode)
        # Guardar la imagen decodificada en un archivo
        with open("image.jpg", "wb") as f:
            f.write(captcha_img_decode)
        captcha_token = captcha_json['token']
        captcha_id = captcha_json['id']
        return captcha_token, captcha_id
    else:
        print(f"Error: {captcha.status_code}")

def validate_info(scnt, widgetKey, sessionId, email, password, first_name, last_name, birth, captcha, captcha_token, captcha_id):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://appleid.apple.com',
        'Referer': 'https://appleid.apple.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        'X-APPLE-HC': '1:10:20250104211246:91a59d1b17282f894c5fafff1d9274a3::409',
        'X-Apple-I-FD-Client-Info': '{"U":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0","L":"es","Z":"GMT-05:00","V":"1.1","F":"Fta44j1e3NlY5BNlY5BSmHACVZXnNA9Z39Y4vFmWCU.Pwdk2_AIQjvEodUW2x5TfBNldicA1Vg0D9Re4GhrWU_HzA2x5TfBNlY5BNp55BNlan0Os5Apw.0K0"}',
        'X-Apple-I-TimeZone': 'America/Havana',
        'X-Apple-ID-Session-Id': sessionId,
        'X-Apple-Request-Context': 'create',
        'X-Apple-Widget-Key': widgetKey,
        'scnt': scnt,
        'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'phoneNumberVerification': {
            'phoneNumber': {
                'id': 1,
                'number': '2084359135',
                'countryCode': 'US',
                'countryDialCode': '1',
                'nonFTEU': True,
            },
            'mode': 'sms',
        },
        'account': {
            'name': email,
            'password': password,
            'person': {
                'name': {
                    'firstName': first_name,
                    'lastName': last_name,
                },
                'birthday': birth,
                'primaryAddress': {
                    'country': 'USA',
                },
            },
            'preferences': {
                'preferredLanguage': 'es_MX',
                'marketingPreferences': {
                    'appleNews': False,
                    'appleUpdates': False,
                    'iTunesUpdates': False,
                },
            },
            'verificationInfo': {
                'id': '',
                'answer': '',
            },
        },
        'captcha': {
            'id': captcha_id,
            'token': captcha_token,
            'answer': captcha,
        },
        'privacyPolicyChecked': False,
    }

    validate = requests.post('https://appleid.apple.com/account/validate', headers=headers, json=json_data)
    validate_json = validate.json()
    if validate.status_code == 200:
        name = validate_json['account']['name']
        first_name = validate_json['account']['person']['name']['firstName']
        last_name = validate_json['account']['person']['name']['lastName']
        verification(name, first_name, last_name)
    elif validate.status_code == 400:
        try:
            message = validate_json['service_errors'][0]['message']
            print(message)
        except KeyError:
            print(validate_json)
    else:
        print(f"Error: {validate.status_code}")

def verification(scnt, widgetKey, sessionId, email, first_name, last_name):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://appleid.apple.com',
        'Referer': 'https://appleid.apple.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        'X-Apple-I-FD-Client-Info': '{"U":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0","L":"es","Z":"GMT-05:00","V":"1.1","F":"Fta44j1e3NlY5BNlY5BSmHACVZXnNA9Z39dTdTjP4Cw0fmb.DJhCizgzH_y3EoOuglY5PuVg91k3sdmcK5rT4yN2wrMuBxLNlY5BNleBBNlYCa1nkBMfs.75H"}',
        'X-Apple-I-TimeZone': 'America/Havana',
        'X-Apple-ID-Session-Id': sessionId,
        'X-Apple-Request-Context': 'create',
        'X-Apple-Widget-Key': widgetKey,
        'scnt': scnt,
        'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'account': {
            'name': email,
            'person': {
                'name': {
                    'firstName': first_name,
                    'lastName': last_name,
                },
            },
        },
        'countryCode': 'USA',
    }

    verification = requests.post('https://appleid.apple.com/account/verification', headers=headers, json=json_data)
    verification_json = verification.json()
    try:
        Id = verification_json['verificationId']
        return Id
    except KeyError:
        print(verification_json)

def send_verify_code(scnt, widgetKey, email, sessionId, Id):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://appleid.apple.com',
        'Referer': 'https://appleid.apple.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        'X-Apple-I-FD-Client-Info': '{"U":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0","L":"es","Z":"GMT-05:00","V":"1.1","F":"Fta44j1e3NlY5BNlY5BSmHACVZXnNA9Z39ijO9NTdfs2M_D.RdPQSzOy_Aw7UcnpOY5CKp0NJ4V8lI_FeCiwnwdbuJzGben5BNlY5CGWY5BOgkLT0XxU...rh"}',
        'X-Apple-I-TimeZone': 'America/Havana',
        'X-Apple-ID-Session-Id': sessionId,
        'X-Apple-Request-Context': 'create',
        'X-Apple-Widget-Key': widgetKey,
        'scnt': scnt,
        'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'name': email,
        'verificationInfo': {
            'id': Id,
            'answer': '975387',
        },
    }

    send_verify_code = requests.put('https://appleid.apple.com/account/verification', headers=headers, json=json_data)
    return send_verify_code.status_code, send_verify_code.json()
