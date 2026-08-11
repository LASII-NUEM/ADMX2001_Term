import serial

ser = serial.Serial(
    port = "COM3",
    baudrate = 115200,
    timeout = 1
)
def cmd(comando):
    ser.write((comando + "\n").encode())

def calibrar():
    print("\n--- CALIBRATION ---")
    calibracoes = {
        "open": {
            "magnitude": "1",
            "comando": "calibrate open"
        },

        "short": {
            "magnitude": "0.2",
            "comando": "calibrate short"
        },

        "load": {
            "magnitude": "1",
            "comando": "calibrate load"
        }
    }
    escolha = input(
        "Qual calibração deseja fazer? "
        "(open, short, load ou todas): "
    ).lower()

    if escolha == "todas":
        for nome, configuracao in calibracoes.items():
            input(f"Conecte o {nome.upper()} e pressione ENTER")
            cmd(f"magnitude {configuracao['magnitude']}")
            cmd(configuracao["comando"])
    else:
        configuracao = calibracoes[escolha]
        input(f"Conecte o {escolha.upper()} e pressione ENTER")

        cmd(f"magnitude {configuracao['magnitude']}")
        cmd(configuracao["comando"])

def configurar_inicial():

    ch0 = input("Setgain ch0: ")
    ch1 = input("Setgain ch1: ")
    magnitude = input("Magnitude: ")
    offset = input("Offset: ")
    average = input("Average: ")
    delay = input("Trigger delay: ")
    frequency = input("Calibration frequency: ")

    cmd(f"setgain ch0 {ch0}")
    cmd(f"setgain ch1 {ch1}")
    cmd(f"magnitude {magnitude}")
    cmd(f"offset {offset}")
    cmd(f"average {average} ")
    cmd(f"tdelay {delay}")
    cmd(f"frequency {frequency}")

def configurar_sweep():
    print("\n--- SWEEP CONFIGURATION ---")
    display = input("Display: ") or "9"
    count = input("Count: ") or "136"

    sweep_type = input("Sweep Type Frequency: ") or "1 1000"
    inico, fim = sweep_type.split()
    sweep_scale = input("Sweep Type Scale: ") or "log"

    cmd(f"display {display}")
    cmd(f"count {count}")
    cmd(f"sweep_type frequency {inico} {fim}")
    cmd(f"sweep_scale {sweep_scale}")

    return int(count)

def medir(count):
    cmd("z")

    medidas = []

    for _ in range(count):
        medidas.append(ser.readline().decode().strip())

    return medidas

def main ():

    configurar_inicial()

    calibrado = input("O equipamento já foi calibrado? [s/n]: ")

    if calibrado.lower() != "s":
        calibrar()

    count = configurar_sweep()

    medidas = medir(count)

    return medidas

medidas = main()

for linha in medidas:
    print(linha)
