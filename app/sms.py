import africastalking
class SMS:
    def __init__(self):
        self.username = "migori-moh"
        self.api_key = "18f90bf9a7b40466101892256753222f8e230828aa0cb595108b4bed2731d232"
        africastalking.initialize(self.username, self.api_key)
        self.sms = africastalking.SMS
    def send(self,msg,recipients):
            # Set the numbers you want to send to in international format
        self.recipients = recipients

            # Set your message
        self.message = msg

            # Set your shortCode or senderId
        sender = "SHORTCODE_OR_SENDERID"
        try:
				# Thats it, hit send and we'll take care of the rest.
            response = self.sms.send(self.message, self.recipients)
            print (response)
        except Exception as e:
            print ('Encountered an error while sending: %s' % str(e))

if __name__ == '__main__':
    SMS().send()
