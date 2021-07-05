# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import re

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import AllSlotsReset, Restarted, SlotSet, SessionStarted
from rasa_sdk.executor import CollectingDispatcher
# from utils.db import db
import datetime


class ActionDaiKuan(Action):
    def name(self):
        return "action_需要贷款吗"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        if not tracker.active_loop:
            dispatcher.utter_message(response="utter_需要贷款吗")
        return []


class ActionZhuCe(Action):
    def name(self):
        return "action_需要注册吗"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        if not tracker.active_loop:
            dispatcher.utter_message(response="utter_需要注册吗")
        return []

class ActionGreet(Action):
    def name(self):
        return "action_转人工"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_转人工")
        has_fang = tracker.get_slot('has_fang')
        has_che = tracker.get_slot('has_che')
        has_zhi = tracker.get_slot('has_zhi')
        has_wei = tracker.get_slot('has_wei')
        has_xin = tracker.get_slot('has_xin')
        phone_number = tracker.get_slot('phone_number')
        zhuce_type = tracker.get_slot('zhuce_type')
        zhuce_hangye = tracker.get_slot('zhuce_hangye')
        has_zhucedi = tracker.get_slot('has_zhucedi')
        has_yes = tracker.get_slot('has_yes')
        results = []
        return results


class ValidationZhuCe(FormValidationAction):
    def name(self) -> Text:
        return "validate_注册_form"

    def validate_zhuce_type(self, value, dispatcher, tracker, domain):
        if value:
            return {"zhuce_type": value}
        else:
            return {"zhuce_type": None}

    def validate_zhuce_hangye(self, value, dispatcher, tracker, domain):
        return {"zhuce_hangye": value}

    def validate_has_zhucedi(self, value, dispatcher, tracker, domain):
        return {"has_zhucedi": value}

    def validate_phone_number(self, value, dispatcher, tracker, domain):
        phone_number = re.findall(r'[0-9]{11}', value)
        if phone_number:
            return {"phone_number": phone_number[0]}
        else:
            dispatcher.utter_message(response="utter_电话无效")
            return {"phone_number": None}

    def validate_has_yes(self, value, dispatcher, tracker, domain):
        if value:
            return {"has_yes": value}
        else:
            return {"phone_number": None, "has_yes": None}


class ValidationDaiKuan(FormValidationAction):
    def name(self) -> Text:
        return "validate_贷款_form"

    def validate_amount_of_money(self, value, dispatcher, tracker, domain):
        return {"amount_of_money": str(value)}

    def validate_has_fang(self, value, dispatcher, tracker, domain):
        d = {"has_fang": value}
        if value:
            d["has_che"] = False
            d["has_zhi"] = False
            d["has_wei"] = False
            d["has_xin"] = False
        return d

    def validate_has_che(self, value, dispatcher, tracker, domain):
        d = {"has_che": value}
        if value:
            d["has_zhi"] = False
            d["has_wei"] = False
            d["has_xin"] = False
        return d

    def validate_has_zhi(self, value, dispatcher, tracker, domain):
        d = {"has_zhi": value}
        if value:
            d["has_wei"] = False
            d["has_xin"] = False
        return d

    def validate_has_wei(self, value, dispatcher, tracker, domain):
        d = {"has_wei": value}
        if value:
            d["has_xin"] = False
        return d

    def validate_has_xin(self, value, dispatcher, tracker, domain):
        d = {"has_xin": value}
        return d

    def validate_phone_number(self, value, dispatcher, tracker, domain):
        phone_number = re.findall(r'[0-9]{11}', value)
        if phone_number:
            return {"phone_number": phone_number[0]}
        else:
            dispatcher.utter_message(response="utter_电话无效")
            return {"phone_number": None}

    def validate_has_yes(self, value, dispatcher, tracker, domain):
        if value:
            return {"has_yes": value}
        else:
            return {"phone_number": None, "has_yes": None}


class ActionUserInfo(Action):
    def name(self):
        return "action_user_info"

    def run(self, dispatcher, tracker, domain):
        if tracker.get_intent_of_latest_message() == '转人工':
            return [AllSlotsReset()]
        has_fang = tracker.get_slot('has_fang')
        has_che = tracker.get_slot('has_che')
        has_zhi = tracker.get_slot('has_zhi')
        has_wei = tracker.get_slot('has_wei')
        has_xin = tracker.get_slot('has_xin')
        phone_number = tracker.get_slot('phone_number')
        zhuce_type = tracker.get_slot('zhuce_type')
        zhuce_hangye = tracker.get_slot('zhuce_hangye')
        has_zhucedi = tracker.get_slot('has_zhucedi')
        amount_of_money = tracker.get_slot("amount_of_money")
        user_info = '您的信息是：'
        data = {}
        if amount_of_money:
            user_info += "贷款金额："+str(amount_of_money)+", "
        flag = False
        if has_fang:
            user_info += '有房，'
            data['has_fang'] = 1
            flag = True
        elif has_fang == False:
            data['has_fang'] = 0
            user_info += '无房，'
        if has_che:
            data['has_che'] = 1
            user_info += '有车，'
            flag = True
        elif has_che == False and not flag:
            data['has_che'] = 0
            user_info += '无车，'
        if has_xin:
            data['has_xin'] = 1
            user_info += '有信用卡，'
            flag = True
        elif has_xin == False and not flag:
            data['has_xin'] = 0
            user_info += '无信用卡，'
        if has_wei:
            data['has_wei'] = 1
            user_info += '有微粒贷，'
            flag = True
        elif has_wei == False and not flag:
            data['has_wei'] = 0
            user_info += '无微粒贷，'
        if has_zhi:
            data['has_zhi'] = 1
            user_info += '有支付宝，'
            flag = True
        elif has_zhi == False and not flag:
            data['has_zhi'] = 0
            user_info += '无支付宝，'
        if zhuce_type:
            user_info += '执照类型：' + zhuce_type + ', '
        if zhuce_hangye:
            user_info += '注册行业： ' + zhuce_hangye + ', '
        if has_zhucedi:
            user_info += '是否有商用产权的注册地址: 是, '
        elif has_zhucedi == False:
            user_info += '是否有商用产权的注册地址: 否, '
        if phone_number:
            data['phone_number'] = phone_number
            user_info += '电话是：'+phone_number
        data['create_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # db.insert('user_info', data)
        dispatcher.utter_message(text=user_info)
        if phone_number:
            dispatcher.utter_message(text='我们将尽快联系您，请保持电话通畅！')
        # elif has_fang is not None:
        #     dispatcher.utter_message(response="utter_不能办理贷款")
        return [AllSlotsReset()]
