$Version = Read-Host -Prompt 'Which version you deploying?'
Write-Host "Deploying version to tekkenthuuug/drr-bot:$Version"

docker build -t tekkenthuuug/drr-bot:$Version .
docker push tekkenthuuug/drr-bot:$Version

Write-Host "SSHing..."
ssh root@207.154.212.51 "docker pull tekkenthuuug/drr-bot:$Version && docker tag tekkenthuuug/drr-bot:$Version dokku/drr-bot:$Version && dokku tags:deploy drr-bot $Version"