import requests
import pandas as pd


def get_id (urls) :
    split_url = urls.split(',')

    id = [id.split("/")[-1] for id in split_url]

    return id

def scrap_data (id_tiktok) : 
    all_komen = []

    ids = id_tiktok

    for id in ids :

        for cursor in range(0 , 100) :

            url = "https://www.tiktok.com/api/comment/list/"

            querystring = {"aweme_id":id,"count":"50","cursor":cursor  * 50,"WebIdLastTime":"1639506389","aid":"1988","app_language":"ja-JP","app_name":"tiktok_web","browser_language":"en-US","browser_name":"Mozilla","browser_online":"true","browser_platform":"Win32","browser_version":"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0","channel":"tiktok_web","cookie_enabled":"true","current_region":"JP","data_collection_enabled":"true","device_id":"7041626242181744130","device_platform":"web_pc","enter_from":"tiktok_web","focus_state":"false","fromWeb":"1","from_page":"video","history_len":"3","is_fullscreen":"false","is_non_personalized":"false","is_page_visible":"true","odinId":"7264238560303416325","os":"windows","priority_region":"ID","referer":"https://www.bing.com/","region":"ID","root_referer":"https://www.bing.com/","screen_height":"720","screen_width":"1280","tz_name":"Asia/Jakarta","user_is_login":"true","webcast_language":"en","msToken":"ZdSMovTf545nrCnxOpKLhswH6CVJC7QdryvqAay0Pzev8e_hb_z9fb8YlCwttKa3-OXadIMCB7W1Z4L4x84zzhugxzR6lPw06TGgTRpZK0iynwSZxL5aj7y7ATSNTQ11Z-pab0h_dtIKfw==","X-Bogus":"DFSzswVLnjsANVA/tX4vyMSscjVx","_signature":"_02B4Z6wo00001luC7awAAIDC0dbjZCJe3q5bgukAAPAUdd"}

            payload = ""
            headers = {
                "cookie": "odin_tt=8f91cad8a23599ac058b25d8f0db9d99a38ee56bdd5c508ea949cc9a50b8a5a7e7303b90b14b77805ba7406ebbb091b15ac4fa3eb45eb3b472bb295fb4257760bcaac0a9f939a4f53503da521b297d61; msToken=omdGdprVrikrsLNV_9KuSeHutZ_LPcqpbo0u52OSgUkJzi5QLdO9lB73QE2RwYIQD_SrMExn492y3-u1ZOhOtaX027LPKtbrqowqO3JRi7OW1DTVpzD0ffKSMMsBLCGoBn0fOT3S1grUoA%3D%3D",
                "User-Agent": "insomnia/10.0.0"
            }


            response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

            j = response.json()

            try :

                if len(j["comments"]) <=0 :
                    break;
            except :
                break ;

            try :
                for i in range(0 , len(j['comments'])):
                    all_komen.append(j['comments'][i]['text'])
            except :
                print("UDAH GA ADA")

    data = pd.DataFrame({"comments" :all_komen })
    return data

def metric_sentiment(data):

    data_positive = data[data.Sentiment == 0]
    data_negative = data[data.Sentiment == 1]

    index_positive = data_positive.shape[0]
    index_negative = data_negative.shape[0]

    return [index_positive , index_negative]


