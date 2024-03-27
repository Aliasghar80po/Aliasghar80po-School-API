from threading import Thread


class SendEmailThread(Thread):
    def __init__(self, email_object):
        Thread.__init__(self)
        self.email_object = email_object

    def run(self):
        self.email_object.send()


def send_email_thread(email_object):
    SendEmailThread(email_object).start()