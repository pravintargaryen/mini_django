import smtplib

def send_mail(email:str, password:str, subject:str, message:str, from_address: str, to_address:list):
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        connection.sendmail(from_addr=from_address, to_addr=to_address, subject=subject, msg=message)


