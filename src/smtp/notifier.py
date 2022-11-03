import aiosmtpd.controller


class NotifierSMTPHandler:

    def __init__(self):
        pass

    async def handle_DATA(self, server, session, envelope) -> str:
        print("do something with the message data")
        return "hi"


# import aiosmtpd.controller

# class CustomSMTPHandler:
#     async def handle_DATA(self, server, session, envelope):
#         myqueue.queue.put(envelope.content)
#         return '250 OK'

# handler = CustomSMTPHandler()
# self.server = aiosmtpd.controller.Controller(handler)
# self.server.start()
# input("Server started. Press Return to quit.")
# self.server.stop()
