"""
MIT License
Copyright (c) 2023 Gaspar Uribe
https://gasparuribe.cl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import requests
import json
from time import gmtime, strftime
login_pass="YWRtaW4=" #Esa es la contraseña por defecto "admin", tiene que enviarse codificada en Base64
HOST = "192.168.0.1"
URL = "http://"+HOST
URL_SET=URL+"/goform/goform_set_cmd_process"
URL_GET=URL+"/goform/goform_get_cmd_process"
REFERER=URL+"/index.html"
HEADERS={'Referer': REFERER}

def login(): #Asegura que tengamos acceso admin a la web de configuraciones
    try:
        data = { 'isTest' : 'false','cmd':'loginfo'}
        response = requests.post(URL_GET, data=data, headers=HEADERS)
        response_dict = json.loads(response.content.decode('utf-8'))
        if response_dict['loginfo'] =='ok':
            return True
        else:
            data = {'isTest':'false', 'goformId':'LOGIN', 'password':login_pass}
            response = requests.post(URL_SET, data=data, headers=HEADERS)
            response_dict = json.loads(response.content.decode('utf-8'))
            if response_dict['result'] == '0':
                return True
            else:
                return False
    except Exception as e:
        return False
def mobile_handle(bool): #(True|False) Enciende o apaga la coneccion a internet movil
    try:
        if login():
            if bool:
                data = { 'isTest':'false', 'notCallback':'true', 'goformId':'CONNECT_NETWORK'}
            else:
                data = { 'isTest':'false', 'notCallback':'true', 'goformId':'DISCONNECT_NETWORK'}
            response = requests.post(URL_SET, data=data, headers=HEADERS)
            response_dict = json.loads(response.content.decode('utf-8'))
            if response_dict['result'] =='success':
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        return False
def wifi_handle(bool): #(True|False) Enciende o apaga la coneccion a Wifi
    try:
        if login():
            if bool:
                data = { 'goformId':'SET_WIFI_INFO', 'isTest':'false', 'm_ssid_enable':'1', 'wifiEnabled':'1' }
            else:
                data = { 'goformId':'SET_WIFI_INFO', 'isTest':'false', 'm_ssid_enable':'0', 'wifiEnabled':'0' }
            response = requests.post(URL_SET, data=data, headers=HEADERS)
            response_dict = json.loads(response.content.decode('utf-8'))
            if response_dict['result'] =='success':
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        return False
def get_sms(): #Muestra todos los mensajes en el disposivo
    try:
        if login():
            data = {'isTest':'false', 'cmd':'sms_data_total', 'page':'0', 'data_per_page':'500', 'mem_store':'1', 'tags':'10', 'order_by':'order+by+id+desc'}
            response = requests.get(URL_GET, params=data, headers=HEADERS)
            response_dict = json.loads(response.content.decode('utf-8'), strict=False)
            for sms in response_dict["messages"]:
                sms['content_to_txt'] = bytes.fromhex(sms['content']).decode('utf-8').replace("\x00", "")
            return response_dict["messages"]
        else:
            return False
    except Exception as e:
        print(e)
        return False
def get_sms_capacity(): #informacion cantidad mensajes
    try:
        if login():
            data = { 'isTest' : 'false','cmd':'sms_capacity_info'}
            response = requests.post(URL_GET, data=data, headers=HEADERS)
            response_dict = json.loads(response.content.decode('utf-8'))
            return response_dict
        else:
            return False
    except Exception as e:
        return False
def send_sms(number,text): #envia un sms a el numero indicado
    try:
        if login():
            time=strftime("%y;%m;%d;%H;%M;%S;+5", gmtime())
            text=text.encode("utf-16-be")
            msg="".join("{:02x}".format(c) for c in text)
            data = {'notCallback' : 'true', 'goformId' : 'SEND_SMS', 'isTest' : 'false','Number' : number, 'sms_time': time, 'MessageBody': msg, 'encode_type' : 'UNICODE', 'ID' : '-1'}
            response = requests.post(URL_SET, data=data, headers=HEADERS)
            response_dict = json.loads(response.content.decode('utf-8'))
            if response_dict['result'] =='success':
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        return False
def delete_sms(ids): #('29;33;55;')elimina uno o varios sms, el id debe estar acompañado de un caracter de puntocoma ;
    #aun no pruebo esta funcion, TESTING NEEDED
    try:
        if login():
            data = { 'isTest' : 'false','goformId':'DELETE_SMS','msg_id':ids,'notCallback':'true'}
            response = requests.post(URL_SET, data=data, headers=HEADERS)
            response_dict = json.loads(response.content.decode('utf-8'))
            if response_dict['result'] =='success':
                print("Delete Success")
            else:
                print("Delete Fail: "+response_dict)
        else:
            return False
    except Exception as e:
        return False

if __name__ == "__main__": #Para probar el codigo desde terminal/comandos
    #mobile_handle(False)
    #wifi_handle(False)
    print(get_sms_capacity())
    print()
    the_sms=get_sms()
    for sms in the_sms:
        print("From: "+sms['number'] + " Date:"+sms['date'] + " ID:"+sms['id'] )
        print(sms['content_to_txt'])
    #send_sms('+56995330765','Hola estoy probando tu codigo gracias')
    #delete_sms('88;')
    print("End BYE")
