# Neo4j Queries Monitoring

This program monitors the query.log file created by neo4j and sends the queries by email or slack.

# Steps
 - [ ] Neo4j can be configured to log queries executed in the database. Please add the threshold parameter.
       
       https://neo4j.com/docs/operations-manual/current/monitoring/logging/query-logging/

 - [ ] Install python3 and pip3 at the server. You could use the following guides.

        https://realpython.com/installing-python/
        https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/

 - [ ] Download the python program on your server and install dependencies with the following command 
        
        sudo -H pip3 install yagmail
        sudo -H pip3 install keyring
        sudo -H pip3 install requests
        sudo -H pip3 install pyyaml
        sudo -H pip3 install -U PyYAML
        sudo -H pip3 install keyrings.alt
    
- [ ] Modify the yaml file. Contains important parameters for the correct job. 
 
        configfile: config.yaml --> [THE CONFIGURATION FILE NAME]
        pathquerylogfile: /var/log/neo4j/query.log --> [THE PATH OF THE query.log FILE. THIS FILE IS CREATED BY NEO4J]
        emailenable: N --> [If you want to send an email, change N to Y]
        emailto: support_company@gmail.com
        emailfrom: support_company@gmail.com --> [Only gmail]
        passwordemailfrom: XXYYYZZZ
        slackenable: Y --> [If you want to send a message to slack, change N to Y]
        slackwebhook: https://hooks.slack.com/services/XXXXXXXXXXXXXXXXXXXX
        
 - [ ] Install cron package for linux with the following commands
        
        apt-get update && apt-get upgrade
        sudo apt-get install cron
        systemctl status cron
        
 - [ ] Edit the cron jobs file with the following command
         
         crontab -e
         
 - [ ] Schedule the script via cron, in this example the program will run every 10 minutes. The program has two arguments. The first argument is the path of the configuration file and the second parameter is the path of the "DataBase" file created by the program

        */10 * * * * /usr/bin/python3 /home/juan/Queries-Monitorig/monitoring_queries.py /home/juan/Queries-Monitorig/config.yaml /home/juan/Queries-Monitorig/ >> /home/juan/Queries-Monitorig/logmonitoring.log 2>&1
       
- [ ] If you have problem sending an email, please you could enable the option "Less secure app access"
        
        https://myaccount.google.com/lesssecureapps
        https://accounts.google.com/DisplayUnlockCaptcha
