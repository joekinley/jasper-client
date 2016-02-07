from socket import *
import thread
import logging

class Listener(object):
    def __init__(self, mic, profile, queue):
        self._logger = logging.getLogger(__name__)
        self.mic = mic
        self.profile = profile
        self.queue = queue
        if 'listener_address' in profile:
            self.ip = profile['listener_address']
        else:
            self.ip = ''
        if 'listener_port' in profile:
            self.port = profile["listener_port"]
        else:
            self.port = 0
        if self.port > 0:
            thread.start_new_thread(self.start_listening, ())

    def start_listening(self):
        self._logger.info("Starting to listen on ip '%s' at port '%s'", self.ip, self.port)
        addr = (self.ip, self.port)
        self.serversocket = socket(AF_INET, SOCK_STREAM)
        self.serversocket.bind(addr)
        self.serversocket.listen(1)
        while 1:
            clientsocket, clientaddr = self.serversocket.accept()
            thread.start_new_thread(self.listen, (clientsocket, clientaddr, self.mic))
        self.serversocket.close()

    def listen(self, clientsocket, clientaddr, mic):
        self._logger.info("Client connected at %s", clientaddr)
        while 1:
            data = clientsocket.recv(1024)
            if not data: continue
            self._logger.debug("Received '%s'", data)
            if data.startswith("say!"):
                mic.say(data[4:])
                #print(data[4:])
            elif data.startswith("listen!"):
                //#answer = mic.activeListen()
                msg = new Message(self, "listen")
                self.queue.put(msg)
                self.queue.join()

                #answer = data[7:]
                clientsocket.send("said!"+msg.msg)
            elif data.startswith("quit"):
                clientsocket.close()
                break

# this should only run on direct call, for testing purposes
if __name__ == "__main__":
    listener = Listener("foo", ())
    print("Alright let's test this")
    while 1:
        1
        #print("")
