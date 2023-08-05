from .auth import Sendsms
import requests
import json
import urllib.request
def bulksms(telephone,smsname,message,username,password):

    print(username)
    data={
        'username':username,
        'password':password,
        'type':0,
        'dlr':1,
        'destination':telephone,
        'source':smsname, 
        'message':message
    }
    sms = requests.post(' http://rslr.connectbind.com:8080/bulksms/bulksms',data=data).text
    res=sms[:4]
   
    print(res)
    if res ==str(1701):
        print(sms)
        print('your message has been sent')
    elif res==str(1703):
        print("Invalid credentials") 
    elif res==str(1702 ):
        print("Invalid URL") 
    elif res==str(1706):

        print("Invalid destination check your phone") 
    elif res==str(1707):
        
        print("Invalid Sender - SMS name ca not go beyond 11 character") 



        
   
    else:
        print("error occured with code :"+res+"") 

   
 
    
    return res