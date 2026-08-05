import serial

ser = serial.Serial(
    port = "COM5",
    baudrate = 115200,
    timeout = 1
)
def cmd(comando):
    ser.write((comando + "\n").encode())

display =float(input("Display: ") or "9")
ch0 = int(input("Setgain ch0: ") or "0")
ch1 = int(input("Setgain ch1: ") or "1")
magnitude = int(input("Magnitude: ")or "1")
count = int(input("Count: ") or "136")
sweep_type = input("Sweep Type Frequency: ") or "1 1000"
inico,fim = sweep_type.split()
cmd(f"sweep_type {inico} {fim}")
sweep_scale = input("Sweep Type Scale: ") or "log"


def medir():
    cmd("z")

    medidas = []

    for _ in range(136):
        medidas.append(ser.readline().decode().strip())

    return medidas

def main ():
    return medir()

if __name__ == "__main__":
    dados = main()

    medidas = main()

    for linha in medidas:
        print(linha)


#short
##Short calibration can be performed only when gain channel 1 is set to 0 or 1. When channel 1 is in gain 1, the magnitude of the source must be less than 0.2Vpk.
#a unica diferença entre os 3 é a magnitude do short


##ser.write(b"setgain ch0 \r\n")
#ouu se usa cmd


#coisas que da pra mudar
##display
##count
##sweep_type frequency 1 1000
##?delay
##magnitude
##ch0 e ch1
##sweep_scale
##??frequency
##average
##?offset


##def definir_ganho(porta_serial, canal: str, valor: int):

    # comandos
    #comando = f"setgain {canal} {valor}\r\n".encode('utf-8')
    #porta_serial.write(comando)

    #resposta = porta_serial.readline().decode('utf-8').strip()
    #prompt = porta_serial.readline().decode('utf-8').strip()

    #print(f"[{canal} -> {valor}] Resposta: {resposta} | Prompt: {prompt}")
    #return resposta


#definir_ganho(ser, "ch0", 0)
#definir_ganho(ser, "ch1", 1)


