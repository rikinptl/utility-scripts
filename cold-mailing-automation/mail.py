import smtplib
import os
import openpyxl
from pathlib import Path

class ColdMail:
    def __init__(self, recruiter_name, company_name, email_address):
        if recruiter_name is None:
            recruiter_name = company_name + " hiring manager(s)"
        
        message = """
Greetings {}, 

Allow me to introduce myself: I'm Rikin Patel.

In the interest of respecting your time, I'll be brief. Here are three key points about me:

1. I've been immersed in the world of data engineering and object-oriented programming and have been crafting systematic Python scripts since the age of 15. I'm an avid reader and always eager to delve into new technologies.
   
2. With a two year of experience under my belt, I've honed my skills as a data engineer, delving into tasks ranging from managing cloud infrastructure to developing microservices as well as compatible complex data pipelines.

3. I'm keen on pursuing an internship opportunity with {}. Would it be possible for me to forward my resume for your consideration?

Looking forward to the possibility of working together.

Best regards,
Rikin Patel
        """.format(recruiter_name, company_name)

        subject = "My interest in a SWE internship at {}".format(company_name)

        self.FROM = os.environ["GMAIL_EMAIL"]
        self.TO = [email_address]

        self.full_mail = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\

        %s
        """ % (self.FROM, ", ".join(self.TO), subject, message)

        self.send_mail()

    def send_mail(self):
        server.sendmail(self.FROM, self.TO, self.full_mail)

if __name__ == "__main__":
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.ehlo()
    server.starttls()
    server.login(os.environ["GMAIL_EMAIL"], os.environ["GMAIL_PASSWORD"])

    xlsx_file = Path('.', 'Recruiter-emails.xlsx')
    wb_obj = openpyxl.load_workbook(xlsx_file)
    sheet = wb_obj.active

    data = []
    for row in sheet.iter_rows(values_only=True):
        name = None
        if row[0] is not None and row[1] is not None:
            if row[2] is not None:
                index_of_bracket = row[2].find('[')
                if index_of_bracket == -1:  # '[' not found
                    name = row[2]
                else:
                    name = row[2][:index_of_bracket]

            data.append({"company": row[0], "email": row[1], "name": name})

    for recruiter in data:
        ColdMail(recruiter["name"], recruiter["company"], recruiter["email"])

    server.quit()
