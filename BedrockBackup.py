#import packages
import os
import time
import shutil
import requests
from mcstatus import MinecraftBedrockServer

#Get env variables
webhook_url = os.environ['WEBHOOK']
interval = os.environ['INTERVAL']
MCserver = os.environ['MCserver']
MCport = os.environ['MCport']
interval = int(interval)

# Source path
src = '/MClevel/worlds'

while True:
    #Set time to str for file name
    timestr = time.strftime("%Y%m%d-%H%M%S")

    # Destination path
    dest = '/BackupDir/'+timestr

    #Check server to see how many are online
    server = MinecraftBedrockServer.lookup(""+MCserver+":"+MCport+"")
    status = server.status()
    online = status.players_online
    onlineint = int(online)

    print(online)

    #Check last run and write current run
    last_count = open('/app/last_count.txt', 'r').read()
    last_count = int(last_count)

    baw = open("/app/last_count.txt", "w")
    baw.write(online)
    baw.close()

    #If someone diconnects, copy the world folder
    if last_count > 0 and onlineint == 0:
        print("All users offline. Creating Backup")

        #Copy the contents from Source to Dest
        shutil.copytree(src, dest)

        #write 0 count to file
        baw = open("/app/last_count.txt", "w")
        baw.write(online)
        baw.close()
        
        #check if file exists
        isFile = os.path.exists(dest)

        #Send webhook
        if webhook_url:
            if isFile:
                #Send to Discord on success
                Message = {
                    "content": "All Players logged off. Backup successful.."
                }
                requests.post(webhook_url, data=Message)
            else:
                #Send to Discord on success
                Message = {
                    "content": "Backup Failed! Check server logs!"
                }
                requests.post(webhook_url, data=Message)

    else:
        print("No Backup required")

    #sleep for loop
    time.sleep(interval)