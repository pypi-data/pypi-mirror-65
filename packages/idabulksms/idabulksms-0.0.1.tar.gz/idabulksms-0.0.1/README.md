# idasms 

Idasms is a python packages which allow you to send  bulk sms . 

before installing this packages you need to get intouch with Ida technology (www.idatech.rw) or send an email at info@idatech.rw to provide  credentials of bulk sms to their bulks sms API.
after that  you ready to go

## HOW TO USE IT  AFTER INSTALLATION 
 open your python file and paste below code 
 ----------------------------------------------------------------------------------
import idabulksms

cre =idabulksms.Sendsms()

usernam=cre.username("enter username")

passwor=cre.password("enter your password")

idabulksms.bulksms('add phone with country code omit +','ssmsname','enter message',usernam,passwor)

print(idabulksms.bulksms)



