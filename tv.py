# Sony Simple IP Control script
# Licensed by GPL

# !!! REPLACE TO YOUR VALUES
TVIP = "192.168.1.43"
TVMAC = "fc:f1:52:9c:cb:5a"
SOCKETTIMEOUR = 5	

# Simple IP port
TVPORT = 20060

recordWidth = 24
cmdPrefix = "*S"
cmdSuffix = "\n"
cmdPrefixLen = len(cmdPrefix)
cmdWidth = 4
cmdTypeWidth = 1
paramWidth = 16
maxResCount = 3

import os, sys, getopt
import socket, time

def usage():
	name = os.path.basename(sys.argv[0])
	print("Usage: %s [<command>] | [(-?|-h|--help) | (-w|--wol) | (-a|--answer)]" % name)
	print("")
	print("       --help    - This message")
	print("       --wol     - power-on TV (Wake-on-LAN)")
	print("       --answer  - Waiting power-on notification")
	print("")
	print("List of commands: 'http://shop.kindermann.com/erp/KCO/avs/3/3005/3005000168/01_Anleitungen+Doku/Steuerungsprotokoll_1.pdf'")
	print("")
	print("Full command format:")
	print("  Type    (1 char)   : 'C' - set param, 'E' - get param")
	print("  Command (4 char)   : 'POWR', 'VOLU'... See specification")
	print("  Params  (16 chars) : '0000000000000030', '0000000100000003'")
	print("")
	print("  Samples:")
	print("   '%s CVOLU0000000000000030' - set volume to 30" % name)
	print("   '%s EVOLU################' - get current volume level" % name)
	print("")
	print("Short command format (not support for all commands):")
	print("  Command         (4 char)      : 'POWR', 'VOLU'...")
	print("  '?' or <Params> (<= 16 chars) : '?' - get param, <Param> - parameter value without leading zeros ('100000003', '50')")
	print("")
	print("  Samples:")
	print("    '%s VOLU50' - set volume to 50 (short command)" % name)
	print("    '%s VOLU?' - get current volume level (short command)" % name)
	print("    '%s INPT100000003' - change input to HDMI 3" % name)
	print("    '%s POWR0' - power off" % name)
	print("    '%s POWR1' - power on" % name)


def wakeOnLan():
	print("Wake on LAN: " + TVMAC)
	import struct
	addr_byte = TVMAC.split(':')
	hw_addr = struct.pack('BBBBBB', int(addr_byte[0], 16),
	int(addr_byte[1], 16),
	int(addr_byte[2], 16),
	int(addr_byte[3], 16),
	int(addr_byte[4], 16),
	int(addr_byte[5], 16))
	msg = b'\xff' * 6 + hw_addr * 16
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.sendto(msg, ('<broadcast>', 9))
	s.close()


def doCommand(cmd, isWait):


	def getCmd(aFullCmd):
		return aFullCmd[cmdPrefixLen + cmdTypeWidth:cmdPrefixLen + cmdTypeWidth + cmdWidth]

	def getType(aFullCmd):
		return aFullCmd[cmdPrefixLen:cmdPrefixLen + cmdTypeWidth]


	if len(cmd) < cmdTypeWidth + cmdWidth + paramWidth:
		command = cmd[0:cmdWidth]
		arg = cmd[cmdWidth:paramWidth + cmdWidth]

		if (len(arg) == 0) | (arg == "") | (arg == "?"):
			arg = ""
			cmdType = "E"
			cmdFill = "#"
		else:
			cmdType = "C"
			cmdFill = "0"

		fullCmd = cmdPrefix + cmdType + command + arg.rjust(paramWidth, cmdFill) + cmdSuffix
	else:
		fullCmd = cmdPrefix + cmd + cmdSuffix

	fullCmd = fullCmd.upper()

	# Get current command
	currentCommand = getCmd(fullCmd)

	def processMsg():
		# Reading answers
		try:
			s = socket.socket()
			s.settimeout(SOCKETTIMEOUR)

			s.connect((TVIP, TVPORT))

			sended = s.send(fullCmd.encode("ascii"))
			if sended != recordWidth:
				return False, "Can't send command"
	
			resCount = 0			
			while resCount < maxResCount:
				resCount = resCount + 1

				res = s.recv(recordWidth).decode("ascii")
				if len(res) != recordWidth:
					continue

				resCommand = getCmd(res)
				resType = getType(res)
				# Is answer for current command
				if (resCommand == currentCommand) & (resType == "A"):
					resCount = maxResCount

		except OSError as msg:
			return False, str(msg)
                		
		# Return flag
		errorFlagIdx = len(cmdPrefix) + cmdTypeWidth + cmdWidth	
		if res[errorFlagIdx] == "F":
			# Error
			return False, "Command error"
		elif res[errorFlagIdx] == "N":
			# No data
			return True
		else:
			try: 
				intVal = int(res[errorFlagIdx:errorFlagIdx + paramWidth])
				# Integer value
				return True, str(intVal)
			except ValueError:
				# Raw data
				return True, res

		return True


	isOk = False
	strMsg = ""
	while not isOk:
		isOk, strMsg = processMsg()
		if (not isOk) & (not isWait):
			isOk = True

	print(strMsg)

	sys.exit(isOk)



def main():
	 	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "?hwa", ["?", "help", "wol", "answer"])
	except getopt.GetOptError as err:
		print(str(err))
		showHelp()
		sys.exit(2)

	for o, a in opts:
		if o in ("-?", "-h", "--help"):
			usage()
			sys.exit(0)
		elif o in ("-w", "--wol"):
			wakeOnLan()
			sys.exit(0)
		elif o in ("-a", "--answer"):
			doCommand("POWR1", True)

	if len(sys.argv) == 2:
		doCommand(sys.argv[1], False)
	else:
		usage()
		sys.exit(0)	

if __name__ == "__main__":
	main()