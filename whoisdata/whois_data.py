# running the data without a cron job to show the actual output
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from collections import defaultdict
import whois
import csv
import schedule
import time 

domains = []
with open('domain.txt','r')as f:
        for i in f:
              domains.append(i.strip('\n'))

sender_mailid = "sachiksachin99@gmail.com"
password = "jcwyrqmrnhrnqrlf"
reciver_mailid = "sachiksachin99@gmail.com"

user_time = "09:00"
# create some data
data = defaultdict(list)

def job():
        # for writing domain details into
        for domain in domains:
                w = whois.whois(domain)
                data['domain_name'] += [w.domain_name]
                data['emails'] += [w.emails]
                data['creation_data'] += [w.creation_date]
                data['expiration_date'] += [w.expiration_date]

        # print(data)
        # domain_name
        # emails
        # creation_date
        # expiration_date

        # create a pandas dataframe from the data
        df = pd.DataFrame(data)

        # write the dataframe to a CSV file
        df.to_csv('output.csv', index=False)

        # sending mail
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        #
        # # start TLS for security
        s.starttls()
        #
        # # Authentication
        s.login(sender_mailid, password)

        message = ''

        with open('output.csv', 'r') as f:
                csv_data = list(csv.reader(f))
                for i in csv_data[1:]:
                        message += f'\n{"*"*25}\n{i[0]} domain details\n'
                for j in i:
                        message += str(j)
                        message += '\n'
                message += '\n'
        #
        # print(message)
        # for key, value in data.items():
        #         try:
        #                 message += f'{key}: {" | ".join(value)}'
        #                 message += '\n'
        #         except TypeError:
        #                 message += f'{key}:  {value}'
        #                 message += '\n'
        #         else:
        #                 pass

        print(message)

        # create message object instance
        msg = MIMEMultipart()

        # set the subject of the email
        msg['Subject'] = 'Domain Details'

        msg.attach(MIMEText(message))
        # sending the mail
        s.sendmail(sender_mailid, reciver_mailid, msg.as_string())

        # terminating the session
        s.quit()


# go to google account settings
# search allow less secure and enable it
# two-step verification should be enabled
# search app passwords, generate new password by entering custom name
#  cpy the password generated and use it in script for sender mail id authentication.
schedule.every().day.at(user_time).do(job)
#job()
while True:
    schedule.run_pending()
    time.sleep(1)