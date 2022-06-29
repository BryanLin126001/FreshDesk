PATH=.:/usr/bin:/usr/lib/jvm/java-8-openjdk-amd64/bin:$PATH
JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
CLASSPATH=/home/bryan/jfreshdesk/lib/freshdesk.jar:/home/bryan/jfreshdesk/lib/gson-2.8.5.jar:/home/bryan/jfreshdesk/lib/log4j-api-2.12.0.jar:/home/bryan/jfreshdesk/lib/log4j-core-2.12.0.jar:/home/bryan/jfreshdesk/lib/sqlite-jdbc-3.27.2.1.jar:/home/bryan/jfreshdesk/properties

export PATH
export JAVA_HOME
export CLASSPATH

python3 ticket_gen.py -n 10 -o /home/bryan/freshdesk/activities.json
java freshdesk.Freshdesk -p /home/bryan/freshdesk/activities.json
python3 Report.py
