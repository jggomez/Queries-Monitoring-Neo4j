import re
import sys
import os
import pickle
import yagmail
import requests
import json
import yaml
from os import path


SUBJECT = "Neo4j Queries Monitoring - New Issue"
SLACK_ICON_URL = 'https://dist.neo4j.com/wp-content/uploads/neo4j_logo_globe1.png'
SLACK_USER_NAME = "Neo4j Monitoring"
URI_PICKLE_FILE = "proccesed_queries.pk"
WRITE_BINARY = "wb"
READ_BINARY = "rb"
PATTERN = r"[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) (2[0-3]|[01][0-9]):[0-5][0-9]:[0-5][0-9]"


def validate_config_variables(args):
    try:
        global path_pickle_file
        path_pickle_file = "{}/{}".format(args[2], URI_PICKLE_FILE)

        with open(args[1]) as file:
            config_list = yaml.load(file, Loader=yaml.FullLoader)

            global path_query_log_file
            path_query_log_file = config_list["pathquerylogfile"]

            if(not path_query_log_file):
                print('The config variable pathquerylogfile doesnt exist')
                return False

            global email_enable
            email_enable = config_list["emailenable"]

            if(email_enable == "Y"):
                global email_to
                email_to = config_list["emailto"]

                if(not email_to):
                    print('The config variable emailto doesnt exist')
                    return False

                global email_from
                email_from = config_list["emailfrom"]

                if(not email_from):
                    print('The config variable emailfrom doesnt exist')
                    return False

                global password_email_from
                password_email_from = config_list["passwordemailfrom"]

                if(not password_email_from):
                    print('The config variable passwordemailfrom doesnt exist')
                    return False

            global slack_enable
            slack_enable = config_list["slackenable"]

            if(slack_enable == "Y"):
                global slack_web_hook
                slack_web_hook = config_list["slackwebhook"]

                if(not slack_web_hook):
                    print('The config variable slackwebhook doesnt exist')
                    return False
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    return True


def get_date_queries_sent():
    return get_content_file(path_pickle_file)


def save_date_queries_sent(dates):
    if(dates):
        for date in dates:
            new_item = {
                date: date
            }
            if(os.path.exists(path_pickle_file)):
                dict_dates = get_content_file(path_pickle_file)
                dict_dates.update(new_item)
                write_content_file(dict_dates, path_pickle_file)
            else:
                write_content_file(new_item, path_pickle_file)


def get_content_file(file):
    if(path.exists(file)):
        with open(file, READ_BINARY) as handle:
            return pickle.load(handle)


def write_content_file(content, file):
    with open(file, WRITE_BINARY) as handle:
        pickle.dump(content, handle)


def read_query_log_file(name_file):
    text_tmp = []
    text_list = []
    dates_processed = []
    data_sent = get_date_queries_sent()
    for line in reversed(list(open(name_file))):
        text_tmp.append('{} \n'.format(line.rstrip()))
        value = re.match(PATTERN, line.rstrip())
        if(value):
            if(data_sent and value.group(0) in data_sent.keys()):
                break
            else:
                dates_processed.append(value.group(0))
                text_tmp.append('******************************** \n')
                text_list.extend(text_tmp)
                text_tmp.clear()

    text_list.reverse()
    return "".join(text_list), dates_processed


def send_email(text):
    if(text):
        print("Sending email...")
        yagmail.register(email_from, password_email_from)
        with yagmail.SMTP(email_from, password_email_from) as yag:
            yag.send(
                to=email_to,
                subject=SUBJECT,
                contents=text
            )


def post_message_to_slack(text, blocks=None):
    if(text):
        print("Posting in slack...")
        response = requests.post(slack_web_hook, data=json.dumps({
            'text': text,
            'username': SLACK_USER_NAME,
            'icon_url': SLACK_ICON_URL,
            'blocks': json.dumps(blocks) if blocks else None
        }), headers={'Content-Type': 'application/json'})
        print('Response Slack: ' + str(response.text))


def start_proccess():

    if(len(sys.argv) < 3):
        print('The arguments are invalid')
        return

    print("Init process...")
    validate_config_variables(sys.argv)

    text_to_send, dates_processed = read_query_log_file(
        path_query_log_file)

    success_email = True
    success_slack = True

    try:
        if(email_enable == "Y"):
            send_email(text_to_send)
    except Exception as ex:
        print("Error sending email", ex)
        success_slack = False

    try:
        if(slack_enable == "Y"):
            post_message_to_slack(text_to_send)
    except Exception as ex:
        print("Error posting message in slack", ex)
        success_slack = False

    if(success_slack or success_email):
        save_date_queries_sent(dates_processed)

    print("Finished process...")


start_proccess()
