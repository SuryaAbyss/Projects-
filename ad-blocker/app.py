import datetime
import time

end_time = datetime.datetime(2025,1,15)
site_block = ["www.wscubetech.com","www.pw.live"]
host_path = "C:/Windows/System32/drivers/etc/hosts"
redirect = "127.0.0.1"

while True:
    if datetime.datetime.now()<end_time:
        print("Start Blocking")
        with open(host_path,"r+") as host_file :
            content = host_file.read()
            for website in site_block:
                if website not in content :
                    host_file.write(redirect +" "+website+"\n")
                else:
                    pass
    else:
        with open(host_path,"r+") as host_file: #file opening for stop blocking after time ends
            content = host_file.readlines()
            host_file.seek(0) # Move the pointer to the beginning of the file
            for lines in content:
               if not any(website in lines for website in site_block): #using for loop for checking file is present or not
                  host_file.write(lines)


            host_file.truncate()
        time.sleep(5)

