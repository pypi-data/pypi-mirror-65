#!/usr/bin/env python
from email.mime.text import MIMEText
from pathlib import Path
from datetime import datetime
from time import sleep
import smtplib, ssl, imaplib, email
import subprocess, os
from getpass import getpass, getuser

## TODO move to util

def mkdirs(path_list=list):
    for path in path_list:
        mkdirs(path)
    return

    os.mkdir(base_folder + new_folder_name)

    return

def mkdirs(path=str):
    path_comp = path.split('/')
    current = ""
    for comp in path_comp:
        current += "{}/".format(comp)
        if not os.path.isdir(current):
            os.mkdir(current)
    return
###############

class gmail:

    __port = 465
    __smtp_server = "smtp.gmail.com"
    __cachePath = "{}/.config/hermes".format(str(Path.home()))
    __cacheFile = "pass.txt"

    def __init__(this, receiver, cred=[], cache=True):
        
        this.__setup(cred, receiver, cache)
        return

    ## Init handler to set up credential and receiver information
    def __setup(this, cred, receiver, cache):

        assert receiver != "", "Receiver mail field is empty"
        cach_creds = this.__searchCacheOrUpdate(cred, cache)
        this.__username, this.__password = cach_creds[0], cach_creds[1]
        this.__receiver = receiver
        return

    ## Search cache for existing credentials. If found, check if newer are given
    def __searchCacheOrUpdate(this, cred, cache):
        creds = []
        ## If credentials are found in cache get them
        if os.path.isfile("{}/{}".format(this.__cachePath, this.__cacheFile)):
            with open("{}/{}".format(this.__cachePath, this.__cacheFile), 'r') as pf:
                creds = pf.read().splitlines()
                assert len(creds) == 2, "Cached credentials have wrong format!"
                assert creds[0] != "" and creds[1] != "", "Username or password field is empty"
            ## Given credentials are considered fresher than cached
            if len(cred) == 2 and creds != cred:
                creds = cred
                ## Write to cache, if instructed
                if cache:
                    this.__writeCache(creds)
        ## Otherwise use the given ones, if given
        else:
            # assert len(cred) == 2, "Format of input tuple for username/password is incorrect"
            # assert cred[0] != "" and cred[1] != "", "Username or password field is empty"
            creds.append(input("Sender email username: "))
            creds.append(str(getpass("Password: ")))
            ## Write to cache, if instructed
            if cache:
                this.__writeCache(creds)
        return creds

    ## Update mail credentials to cache
    def __writeCache(this, cred):
        if not os.path.isdir(this.__cachePath):
            mkdirs(this.__cachePath)
        with open("{}/{}".format(this.__cachePath, this.__cacheFile), 'w') as pf:
            pf.write("\n".join(cred))
        return

    ## Return username allocated to this object
    def user(this):
    	return this.__username

    ## Core function to broadcast a message to receiver
    def broadcast(this, reporting_module, msg, request_reply = False):

        if this.__password == "":
            assert False, "SMTP Server password for {} not specified!".format(this.__username)

        message = this.__generate_message(reporting_module, msg)
        this.__send_message(message)

        if request_reply:
            this.__mailbox_check_wait(message)
            cmd = this.__receive_instruction()
            this.__execute_instructions(cmd)
            return cmd

        return

    ## MIME message constructor
    def __generate_message(this, rm, m):
        message = MIMEText("Error Reported:\n\n---------------------------------------\n{}\n---------------------------------------\n\nError reported by mail agent".format(m))
        message['Subject'] = "{}".format(rm)
        message['From'] = this.__username
        message['To'] = this.__receiver
        message['Sent'] = str(datetime.now())
        return message

    ## Login to smtp server using credentials and send message
    def __send_message(this, message):

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(this.__smtp_server, this.__port, context=context) as server:
            server.login(this.__username, this.__password)
            server.sendmail(this.__username, this.__receiver, message.as_string())
        return

    ## Fetch mail, extract the body of the message and parse the instruction given
    def __receive_instruction(this):

        r, d = this.__fetch_mail(encoding = "(UID BODY[TEXT])")
        msg = this.__extract_email(d).as_string().split('\n')
        command = []

        for line in msg:
            if "$cmd" in line:
                command_str = ":".join(line.split(':')[1:])
                command = [x.split() for x in command_str.split(';') if x]
                break

        assert len(command) != 0, "Command field not extracted successfully!"
        return command

    ## Simple routine to execute in bash the instruction given
    def __execute_instructions(this, cmd):

        for c in cmd:
            proc = subprocess.Popen(c, stdout=subprocess.PIPE)
            out, err = proc.communicate()
            ## Convert to logger
            print(out.decode("utf-8"))
        return

    ## Busy waiting for a reply from a specific recipient
    def __mailbox_check_wait(this, message):

        r, d = this.__fetch_mail()
        msg = this.__extract_email(d)

        ## TODO add time too
        while not (message['Subject'] in msg['Subject'] and message['To'] in msg['From']):     
            sleep(10)
            r, d = this.__fetch_mail()
            msg = this.__extract_email(d)
        return

    ## Login to mailbox and fetch the latest email
    def __fetch_mail(this, encoding = "(RFC822)"):

        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(this.__username, this.__password)
        mail.list()

        # Out: list of "folders" aka labels in gmail.
        mail.select("inbox", readonly=True) # connect to inbox.
        result, data = mail.search(None, "ALL")
        id_list = data[0].split() # ids is a space separated string
        latest_email_id = id_list[-1] # get the latest
        result, data = mail.fetch(latest_email_id, encoding) # fetch the email body (RFC822) for the given ID

        return result, data

    ## Extract the core message from raw mail data
    def __extract_email(this, data):

        for response_part in data:
            if isinstance(response_part, tuple):
                return email.message_from_bytes(response_part[1])

        assert False, "Main email cannot be extracted: Wrong format!"
