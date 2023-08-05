class Sendsms:
    def username(self,username):
        print(username)

        return username
    def password(self,password):
        print(password)
        
        return password

def main():
    # object zanjye
    sendsms=Sendsms() 
    sendsms.password()
    sendsms.username()
  
if __name__ == "__main__":
    main()

