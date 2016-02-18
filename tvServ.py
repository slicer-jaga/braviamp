import sys, socketserver, threading

# Debug server

TVIP = "127.0.0.1"
TVPORT = 20060

recordWidth = 24
cmdPrefix = "*S"
isNotify = True

class TvTCPHandler(socketserver.BaseRequestHandler):

	def handle(self):
		buf = self.request.recv(recordWidth).strip().decode('ascii')
		if (len(buf) == recordWidth - 1) & (buf[0:len(cmdPrefix)] == cmdPrefix):
			print("<<< " + buf)
			
                        # Correct answer			
			answer = buf[0:2] + "A" + buf[3:len(buf)] + "\n"
			# Wrong answer
			#answer = buf[0:2] + "AZZZZ" + buf[7:len(buf)] + "\n"
			print(">>> " + answer)
			
			self.request.send(answer.encode('ascii'))			
	
			if isNotify == False:
				def killServer():
                   			self.server.shutdown()
				t = threading.Thread(target=killServer)
				t.start()

def startNotifyServer():
	server = socketserver.TCPServer(("", TVPORT), TvTCPHandler)
	server.serve_forever()


if __name__ == "__main__":
	startNotifyServer()


