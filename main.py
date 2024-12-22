from pystray import Icon,MenuItem,Menu
from tkinter import messagebox
from os import path,name,mkdir
from threading import Thread
from requests import Session
from json import loads
from time import sleep
from PIL import Image

if name=='nt':
    messagebox.showinfo('Ukraine Alarm/Alert','Це неофіційна програма тривог, але є офіційно доступна для Windows: https://winapp.ukrainealarm.com/publish/setup.exe')

BASE_URL='https://api.ukrainealarm.com/api/v3/'
API_KEY='de48614d:654f3ad5a03ae3ee8dab1d9a025738f3'

RUNNING=True
def on_quit():
    global RUNNING
    ICON.stop()
    RUNNING=False

ICONS={'normal':Image.open('favicon.ico'),'connection_error':Image.open('favicon_warning.ico')}
ICON = Icon('Ukraine Alarm/Alert',ICONS['normal'],'Тривога!',Menu(MenuItem('Показати статус',...),MenuItem('Вийти',on_quit)),visible=True)

Thread(target=ICON.notify,args=('Отримання інформації...','Тривога!',)).start()
REQUESTS_SESSION,SELECTED_REGION,ACTIVE_ALERTS,ACTIVE_AIR_ALERT,ACTIVE_ARTILLERY_ALERT,PROBLEMS=Session(),'30',0,False,False,False
Thread(target=ICON.run).start()
    
while RUNNING:
    try:
        RESPONSE=REQUESTS_SESSION.get(BASE_URL+'alerts/'+SELECTED_REGION,headers={'Authorization':API_KEY})
        INFO=loads(RESPONSE.content)
        if len(INFO)==0:Thread(target=ICON.notify,args=('Цей регіон не було знайдено!','Тривога!',)).start()
        else:
            if ACTIVE_ALERTS>len(INFO['activeAlerts']):
                ACTIVE_ALERTS=len(INFO['activeAlerts'])
                ICON.notify(f'🟢Увага! Відбій тривоги в {INFO['regionName']} o {INFO['lastUpdate']}')
            else:
                for alert in INFO['activeAlerts']:
                    if alert['type']=='AIR':ACTIVE_AIR_ALERT=True
                    elif alert['type']=='ARTILLERY':ACTIVE_ARTILLERY_ALERT=True
                    Thread(target=ICON.notify,args=(f'{'🟠' if alert['type']=='ARTILLERY' else '🔴'}'+f'Увага! Початок {'артилерійської' if alert['type']=='ARTILLERY' else 'повітряної'} тривоги в {INFO['regionName']} о {INFO['lastUpdate']}','Тривога!',)).start()
                ACTIVE_ALERTS=len(INFO['activeAlerts'])
        if PROBLEMS:
            PROBLEMS=False
            ICON.icon=ICONS['normal']
            sleep(1.0)
    except Exception as e:
        if not PROBLEMS:
            ICON.icon=ICONS['connection_error']
            PROBLEMS=True