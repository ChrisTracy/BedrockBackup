# BedrockBackup
A docker container to backup your bedrock server

    docker run --name bedrock-backup --restart unless-stopped -d -e MCserver="example.org" -e MCport=19132 -e INTERVAL="60" -e WEBHOOK="https://discord.com/api/webhooks/..."  -v /path/to/minecraft/level:/MClevel -v /Backup/Location:/BackupDir christracy/bedrock-backup
