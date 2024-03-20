import smtplib


def sendEmail(*args, **kwargs):
    #  creates SMTP session
    s = smtplib.SMTP("smtp.gmail.com", 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login("backendtesting85@gmail.com", "uqdw cnvd brpe thae")
    # message to be sent
    message = f"Subject:{kwargs['subject']}\n\n{kwargs['message']}"
    # sending the mail
    s.sendmail("noreply@backend.com", kwargs["to"], message)
    # terminating the session
    s.quit()
