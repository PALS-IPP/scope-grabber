import os.path

import pyvisa

rm: pyvisa.ResourceManager = pyvisa.ResourceManager()

counter: int = 0
targetLabel: str = 'X'
angle: str = '130'
OAM: str = '8'
dataDir: str = 'data/' + targetLabel + '/' + OAM + '/' + angle
os.makedirs(dataDir, 0o777, True)

inst: pyvisa.Resource = rm.open_resource('TCPIP::192.168.0.12::INSTR')
print(inst.query("*IDN?"))
inst.timeout = None

while True:
    inst.write("ACQuire:STATE OFF")
    inst.write("ACQuire:STOPAfter SEQuence")

    inst.write("ACQuire:STATE ON")

    print(inst.query("*OPC?"))
    counter += 1

    for channel in ["CH1", "CH3", 'CH4']:
        inst.write("DATa:SOUrce " + str(channel))
        inst.write("DATa:ENCdg ASCIi")
        inst.write(":DATa:START 1")
        inst.write(":DATa:STOP 100000")
        inst.write("WFMOutpre:BYT_Nr 2")
        head = inst.query("WFMOutpre?")
        data = inst.query("CURVe?")
        while True:

            dataFileName: str = dataDir + "/" + str(counter) + '-' + str(channel) + "-data.data"
            headFileName: str = dataDir + "/" + str(counter) + '-' + str(channel) + "-head.data"
            if os.path.isfile(headFileName) or os.path.isfile(dataFileName):
                counter += 1
                print(counter)
            else:
                headFile = open(headFileName, "a")
                headFile.write(head)
                headFile.close()
                print("saved as " + headFileName)

                dataFile = open(dataFileName, "a")
                dataFile.write(data)
                dataFile.close()
                print("saved as " + dataFileName)
                break
    if counter > 19:
        break
print('done')
inst.close()
exit(0)
