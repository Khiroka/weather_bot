# coding: utf-8
from slack import WebClient
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
from datetime import datetime

import os
import requests
import urllib.request as req
import sys
import json
import pprint
import re
import datetime

client = WebClient(token=os.getenv('SLACK_CLIENT_TOKEN'))



@listen_to('^天気')
def reply_weather(message, arg):

    client.chat_postMessage(
    channel=message.body['channel'],
  
    blocks=[
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "天気を知りたい都道府県を教えて欲しいなッ！！！"
                },
                "accessory": {
                    "type": "static_select",
                    "action_id": "select-menu",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "ここから選んでね！！",
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "東京",
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "埼玉",
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "千葉",
                            },
                            "value": "value-2"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "山梨",
                            },
                            "value": "value-3"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "グンマ",
                            },
                            "value": "value-4"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "茨城",
                            },
                            "value": "value-5"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "栃木",
                            },
                            "value": "value-6"
                        }
                    ]
                }
            },
            {
                "type": "divider"
            }
    ]
)

    # if re.search('^天気', arg) is None:
    #     return

    if "千葉" in "select-menu":
        city_name = "Chiba"
        city = "千葉"
    elif "埼玉" in "select-menu":
        city_name = "Saitama"
        city = "埼玉"
    elif "茨城" in "select-menu":
        city_name = "Ibaraki"
        city = "茨城"
    elif "群馬" in "select-menu":
        city_name = "Gunma"
        city = "群馬"
    elif "山梨" in "select-menu":
        city_name = "Yamanashi"
        city = "山梨"
    elif "神奈川" in "select-menu":
        city_name = "Kanagawa"
        city = "神奈川"
    elif "栃木" in "select-menu":
        city_name = "Tochigi"
        city = "栃木"
    else:
        city_name ="Tokyo"
        city = "東京"



    # city_nameで指定した地域のお天気結果取得
    res_api = get_api_response(city_name)
    pprint.pprint(res_api)


    #mainから取得
    res_main = res_api.get("main")
    #res_pressure = res_main.get("pressure")
    res_temp = res_main.get("temp")

    #weatherから取得
    res_weather = res_api.get("weather")
    res_weatherlist = res_weather[0]
    res_mark = res_weatherlist.get("main")
    
    #お天気マーク
    #emoji = main_weather.get(res_mark)
    #emoji ={"Rain":":umbrella:",  "clear sky":":sunny:", "Thunderstorm":":pika:", "Drizzle":":shower:", "Snow":":snowflake:", 
    #"Mist":":new_moon_with_face:", "Smoke":":yosi:", "Haze":":hotsprings:", "Dust":":mask:", "Fog":":dash:", "Sand":":camel:", "Ash":":volcano:", 
    #"Squall":":ocean:", "Tornado":":cycrone:", "Clouds":":cloud:"}

    #その他res_apiから取得
    # res_timezone = res_api.get("dt")

    date_time = datetime.date.today()

    #英語をそれぞれ日本語にしてくれる辞書
    main_weather ={"Rain":"雨が降ってますね・・・:umbrella:",  "clear sky":"晴れてますよ！！良いぞ:sunny::sunny:", "Thunderstorm":"雷と雨が襲来します:pika::pika:", "Drizzle":"霧雨、防水にお気をつけ下さい:shower:", "Snow":"・・・？！雪が降っている？！:snowflake:", 
 "Mist":"かすんでます:new_moon_with_face:", "Smoke":"けむいですご注意ください:yosi:", "Haze":"もやもや気味です:hotsprings:", "Dust":"ほこりっぽいです:mask:", "Fog":"きりだぁああああ前方注意:dash:", "Sand":"砂ぼこりが舞ってます！！僕も舞います:camel::踊る男性:", "Ash":"火山灰が降ってます！！お逃げの準備を:volcano:", 
 "Squall":"嵐のコンサートですよ:ocean:", "Tornado":"竜巻が来日してます:cycrone:", "Clouds":"曇ってますが:cloud:僕の心は晴れてます:sunglasses:"}

    # main_weather[res_mark]

    if main_weather.get(res_mark):
        res_mark = main_weather.get(res_mark)
    else:
        res_mark = f"設定辞書に{res_mark}が含まれてないみたいだよ"
    
    if "天気" in message:
        message.reply(f"\nこんにちは！晴男です！！！\n{date_time} 現在の{city}は{res_mark}！！！\n気温は{res_temp}度です！！！") 


def get_api_response(city):
  request_url = f"http://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&APPID={API_KEY}&lang=ja"
  response = requests.get(request_url)
  data = response.json()

  return data

# 辞書型の中身の取り出し方
# dict["key_name"] or dict.get("key_name")

# try  key_nameをcloudsとして上のやり方で取ってみよう
# try main

# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？

# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                               文字列中に':'はいらない

# .*でどんなメッセージでも受け付ける状態
# respond_toで指定してもいいし、中でif message=xxx と分岐してもいい

# def listen_func(message):
#     message.send('誰かがリッスンと投稿したようだ')      # ただの投稿
#     message.reply('君だね？')
