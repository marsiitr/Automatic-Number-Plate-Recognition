import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_contacts(filename):
    
    names = []
    emails = []
    vehicle_nos=[]
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
            vehicle_nos.append(a_contact.split()[2])
    return names, emails , vehicle_nos

def read_template(filename):
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def email_vehicle_user(vehicle_no ):
    names, emails , vehicle_nos = get_contacts('database.txt')
    gmailaddress = "Your email address"
    gmailpassword = "Your email password"
    message_template = read_template("message.txt")
    msg = MIMEMultipart()
    s = smtplib.SMTP('smtp.gmail.com' , 587)
    s.starttls()
    s.login(gmailaddress, gmailpassword)
    if vehicle_no in vehicle_nos:
        i= vehicle_nos.index(vehicle_no)
        name = names[i]
        email = emails[i]
        message = message_template.substitute(PERSON_NAME=name.title() , VEHICLE_NO=vehicle_no)
        msg['From']=gmailaddress
        msg['To']=email
        msg['Subject']="TAXN GENERATED"
        msg.attach(MIMEText(message, 'plain'))
        s.send_message(msg)
        del msg
    s.quit()