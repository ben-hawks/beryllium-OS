import board
import pwmio
import digitalio
import analogio
import busio
import time
import adafruit_ssd1306
import supervisor
import gc
import os

Exit = False
Exit_code = 0

class ljinux():
    class io(object):
        # activity led
        led = digitalio.DigitalInOut(board.LED)
        led.direction = digitalio.Direction.OUTPUT
        led.value = True
        # L R and Enter keys for basic io
        buttonl = digitalio.DigitalInOut(board.GP12)
        buttonl.switch_to_input(pull=digitalio.Pull.DOWN)
        buttonr = digitalio.DigitalInOut(board.GP13)
        buttonr.switch_to_input(pull=digitalio.Pull.DOWN)
        buttone = digitalio.DigitalInOut(board.GP11)
        buttone.switch_to_input(pull=digitalio.Pull.DOWN)
        # pc puzzer
        buzzer = pwmio.PWMOut(board.GP15, variable_frequency=True, frequency = 200, duty_cycle = 0)
        # volume knob
        volume = analogio.AnalogIn(board.GP26)
        
        def get_voltage(raw):
            return (raw * 3.3) / 65536

        def get_volume_val():
            return (ljinux.io.get_voltage(ljinux.io.volume.value)/3.3)

    class based(object):
        inputt = None
        def autorun():
            global Exit
            global Exit_code
            print("Attempting to open /Init.lja..")
            try:
                f = open("/Init.lja", 'r')
                lines = f.readlines()
                count = 0
                for line in lines:
                    lines[count] = line.strip()
                    count += 1
                for commandd in lines:
                    ljinux.based.shell(commandd)
                f.close()
            except OSError:
                print("Init.lja does not exist, dropping to prompt..\n")
                while not Exit:
                    try:
                        ljinux.based.shell()
                    except KeyboardInterrupt:
                        print("^C\n",end='')

        class command():
            def ls(dirr):
                argss_in = {}
                in_l = 0
                aa = False
                ll = False
                rett = ""
                directory_listing = os.listdir()
                try:
                    if ("-" == str(dirr[1])[:1]):
                        argss_in = list(str(dirr[1])[1:])
                except IndexError:
                    pass
                if ("l" in argss_in):
                    ll = True
                if ("a" in argss_in):
                    if ll:
                        print(".")
                        rett += (".")
                        print("..")
                        rett += ("..")
                    else:
                        print(".", end='   ')
                        rett += (".   ")
                        print("..", end='   ')
                        rett += ("..   ")
                    aa = True
                    in_l +=2
                for i in directory_listing:
                    if ((i)[:1] == "."):
                        if (aa):
                            if not (ll):
                                    print(i, end='   ')
                                    rett += (i + '   ')
                                    in_l += 1
                            else:
                                print(i)
                                rett += (i)
                                in_l += 1
                    else:
                        if not (ll):
                            print(i, end='   ')
                            rett += (i + '   ')
                            in_l += 1
                        else:
                            print(i)
                            rett += (i)
                            in_l +=1
                if not (ll):
                    print("\n", end='')
                    rett += ("\n")
                return rett

            def not_found(errr):
                print("based: " + errr[0] + ": command not found")
            def execc(whatt):
                print("not implemeneted - exec")
            def pwd(dirr):
                print(os.getcwd())
            def helpp(commd):
                print("not implemeneted - help")
            def printt(what):
                print("not implemeneted - print")
            def read(datatypee):
                print("not implemeneted - read")
            def exitt(returncode):
                global Exit
                global Exit_code
                print("Bye")
                Exit = True
                try:
                    Exit_code = returncode[1]
                except IndexError:
                    pass
            def unamee(optt):
                try:
                    if (optt[1] == "-a"):
                        tt = time.localtime()
                        print("Ljinux Raspberry Pi Pico 0.0.1 " + str(tt.tm_mday) + "/" + str(tt.tm_mon) + "/" + str(tt.tm_year) + " " + str(tt.tm_hour) + ":" + str(tt.tm_min) + ":" + str(tt.tm_sec) + " circuitpython Ljinux")
                except IndexError:
                    print("Ljinux")
            def cdd(optt):
                try:
                    os.chdir(optt[1])
                except OSError:
                    print("Error: Directory does not exist")
                except IndexError:
                    pass

        def shell(inp=None):
            global Exit
            function_dict = {'ls':ljinux.based.command.ls, 'error':ljinux.based.command.not_found, 'exec':ljinux.based.command.execc, 'pwd':ljinux.based.command.pwd, 'help':ljinux.based.command.helpp, 'print':ljinux.based.command.printt, 'read':ljinux.based.command.read, 'exit':ljinux.based.command.exitt, 'uname':ljinux.based.command.unamee, 'cd':ljinux.based.command.cdd}
            command_input = False
            if not Exit:
                while ((command_input == False) or (command_input == " ")):
                    if (inp == None):
                        print("[pi@pico | " + os.getcwd() + "]> ", end='')
                        command_input = ljinux.get_input.serial()
                    else:
                        command_input = inp
                command_split = command_input.split()
                if not (command_input == ""):
                    if (str(command_split[0])[:2] == "./"):
                        command_split[0] = str(command_split[0])[2:]
                        if (command_split[0] != ''):
                            function_dict["exec"](command_split)
                        else:
                            print("Error: No file specified")
                    elif ((command_split[0] in function_dict) and (command_split[0] != "error")):
                        function_dict[command_split[0]](command_split)
                    else:
                        ljinux.based.function_dict["error"](command_split)

    class farland(object):
        # the screen holder
        oled = None
        # the time variables
        timm_old = 0
        tp = [0, 0, 0, -1]
        poss = [0, 6, 16, 22, 11]
        poin = False
        offs = 50
        # fps stuff
        time_old = time.monotonic()
        time_new = None
        frames = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        frame_poi = 0
        frames_suff = False
        # ---
        
        def setup():
            ljinux.io.led.value = False
            i2c = busio.I2C(board.GP17, board.GP16)  # SCL, SDA
            ljinux.farland.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c) # I use the i2c cuz it ez
            ljinux.farland.oled.fill(0) # cuz why not
            ljinux.farland.oled.show()
            ljinux.io.led.value = True
        
        def frame():
            ljinux.farland.oled.show()
        
        def clear():
            ljinux.io.led.value = False
            ljinux.farland.oled.fill(0)
            ljinux.farland.oled.show()
            ljinux.io.led.value = True
        
        def pixel(x,y,col):
            ljinux.farland.oled.pixel(x, y, col)
        
        def text(strr,x,y,col):
            ljinux.farland.oled.text(strr,x,y,col)
        
        # getters
        def height():
            return int(ljinux.farland.oled.height)
        
        def width():
            return int(ljinux.farland.oled.width)
        
        # privitive graphics
        def draw_line(x,y,l,col):
            print("nothing yet")
        
        def draw_circle(xpos0, ypos0, rad, col=1):
            x = rad - 1
            y = 0
            dx = 1
            dy = 1
            err = dx - (rad << 1)
            while x >= y:
                ljinux.farland.oled.pixel(xpos0 + x, ypos0 + y, col)
                ljinux.farland.oled.pixel(xpos0 + y, ypos0 + x, col)
                ljinux.farland.oled.pixel(xpos0 - y, ypos0 + x, col)
                ljinux.farland.oled.pixel(xpos0 - x, ypos0 + y, col)
                ljinux.farland.oled.pixel(xpos0 - x, ypos0 - y, col)
                ljinux.farland.oled.pixel(xpos0 - y, ypos0 - x, col)
                ljinux.farland.oled.pixel(xpos0 + y, ypos0 - x, col)
                ljinux.farland.oled.pixel(xpos0 + x, ypos0 - y, col)
                if err <= 0:
                    y += 1
                    err += dy
                    dy += 2
                if err > 0:
                    x -= 1
                    dx += 2
                    err += dx - (rad << 1)
        
        def draw_top(): # to be made into an app
            for i in range(128):
                for j in range (11):
                    ljinux.farland.oled.pixel(i,j, True)
        
        #clock functions, to be made part of hs
        
        # init the clock
        def draw_init_clock():
            ljinux.farland.oled.text("0", ljinux.farland.poss[0] + ljinux.farland.offs, 2, False)
            ljinux.farland.oled.text("0", ljinux.farland.poss[1] + ljinux.farland.offs, 2, False)
            ljinux.farland.oled.text("0", ljinux.farland.poss[2] + ljinux.farland.offs, 2, False)
            ljinux.farland.oled.text("0", ljinux.farland.poss[3] + ljinux.farland.offs, 2, False)
        
        # each time increments if monotonic has gone up
        def draw_clock():
            ljinux.farland.timm_in = int(time.monotonic())
            if (ljinux.farland.timm_in != ljinux.farland.timm_old):
                ljinux.farland.timm_old = ljinux.farland.timm_in
                if (ljinux.farland.tp[3] != 9):
                    ljinux.farland.oled.text(str(ljinux.farland.tp[3]), ljinux.farland.poss[3] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[3] += 1
                    ljinux.farland.oled.text(str(ljinux.farland.tp[3]), ljinux.farland.poss[3] + ljinux.farland.offs, 2, False)
                elif (ljinux.farland.tp[2] != 5):
                    ljinux.farland.oled.text(str(ljinux.farland.tp[3]), ljinux.farland.poss[3] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[3] = 0
                    ljinux.farland.oled.text(str(ljinux.farland.tp[3]), ljinux.farland.poss[3] + ljinux.farland.offs, 2, False)
                    ljinux.farland.oled.text(str(ljinux.farland.tp[2]), ljinux.farland.poss[2] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[2] += 1
                    ljinux.farland.oled.text(str(ljinux.farland.tp[2]), ljinux.farland.poss[2] + ljinux.farland.offs, 2, False)
                elif (ljinux.farland.tp[1] != 9):
                    ljinux.farland.oled.text(str(ljinux.farland.tp[3]), ljinux.farland.poss[3] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[3] = 0
                    ljinux.farland.oled.text(str(ljinux.farland.tp[3]), ljinux.farland.poss[3] + ljinux.farland.offs, 2, False)
                    ljinux.farland.oled.text(str(ljinux.farland.tp[2]), ljinux.farland.poss[2] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[2] = 0
                    ljinux.farland.oled.text(str(ljinux.farland.tp[2]), ljinux.farland.poss[2] + ljinux.farland.offs, 2, False)
                    ljinux.farland.oled.text(str(ljinux.farland.tp[1]), ljinux.farland.poss[1] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[1] += 1
                    ljinux.farland.oled.text(str(ljinux.farland.tp[1]), ljinux.farland.poss[1] + ljinux.farland.offs, 2, False)
                elif (ljinux.farland.tp[0] != 5):
                    ljinux.farland.oled.text(str(ljinux.farland.tp[3]), ljinux.farland.poss[3] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[3] = 0
                    ljinux.farland.oled.text(str(ljinux.farland.tp[3]), ljinux.farland.poss[3] + ljinux.farland.offs, 2, False)
                    ljinux.farland.oled.text(str(ljinux.farland.tp[2]), ljinux.farland.poss[2] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[2] = 0
                    ljinux.farland.oled.text(str(ljinux.farland.tp[2]), ljinux.farland.poss[2] + ljinux.farland.offs, 2, False)
                    ljinux.farland.oled.text(str(ljinux.farland.tp[1]), ljinux.farland.poss[1] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[1] = 0
                    ljinux.farland.oled.text(str(ljinux.farland.tp[1]), ljinux.farland.poss[1] + ljinux.farland.offs, 2, False)
                    ljinux.farland.oled.text(str(ljinux.farland.tp[0]), ljinux.farland.poss[0] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[0] += 1
                    ljinux.farland.oled.text(str(ljinux.farland.tp[0]), ljinux.farland.poss[0] + ljinux.farland.offs, 2, False)
                ljinux.farland.poin = not (ljinux.farland.poin)
                ljinux.farland.oled.text(":", ljinux.farland.poss[4] + ljinux.farland.offs, 2, ljinux.farland.poin)
        
        def fps():
            if ((ljinux.farland.frame_poi <= 9)):
                ljinux.farland.time_new = time.monotonic()
                ljinux.farland.frames[ljinux.farland.frame_poi] = ljinux.farland.time_new - ljinux.farland.time_old
                ljinux.farland.time_old = time.monotonic()
                if ljinux.farland.frames_suff:
                    ljinux.farland.frames_av()
                ljinux.farland.frame_poi += 1
            else :
                ljinux.farland.frames_suff = True
                ljinux.farland.frames_av()
                ljinux.farland.frame_poi = 0
        
        def frames_av():
            average = 0
            for i in range(10):
                average += ljinux.farland.frames[i]
                average = 1/ (average / 10)
            print(average)

        tones = {
            'C0':16,
            'C#0':17,
            'D0':18,
            'D#0':19,
            'E0':21,
            'F0':22,
            'F#0':23,
            'G0':24,
            'G#0':26,
            'A0':28,
            'A#0':29,
            'B0':31,
            'C1':33,
            'C#1':35,
            'D1':37,
            'D#1':39,
            'E1':41,
            'F1':44,
            'F#1':46,
            'G1':49,
            'G#1':52,
            'A1':55,
            'A#1':58,
            'B1':62,
            'C2':65,
            'C#2':69,
            'D2':73,
            'D#2':78,
            'E2':82,
            'F2':87,
            'F#2':92,
            'G2':98,
            'G#2':104,
            'A2':110,
            'A#2':117,
            'B2':123,
            'C3':131,
            'C#3':139,
            'D3':147,
            'D#3':156,
            'E3':165,
            'F3':175,
            'F#3':185,
            'G3':196,
            'G#3':208,
            'A3':220,
            'A#3':233,
            'B3':247,
            'C4':262,
            'C#4':277,
            'D4':294,
            'D#4':311,
            'E4':330,
            'F4':349,
            'F#4':370,
            'G4':392,
            'G#4':415,
            'A4':440,
            'A#4':466,
            'B4':494,
            'C5':523,
            'C#5':554,
            'D5':587,
            'D#5':622,
            'E5':659,
            'F5':698,
            'F#5':740,
            'G5':784,
            'G#5':831,
            'A5':880,
            'A#5':932,
            'B5':988,
            'C6':1047,
            'C#6':1109,
            'D6':1175,
            'D#6':1245,
            'E6':1319,
            'F6':1397,
            'F#6':1480,
            'G6':1568,
            'G#6':1661,
            'A6':1760,
            'A#6':1865,
            'B6':1976,
            'C7':2093,
            'C#7':2217,
            'D7':2349,
            'D#7':2489,
            'E7':2637,
            'F7':2794,
            'F#7':2960,
            'G7':3136,
            'G#7':3322,
            'A7':3520,
            'A#7':3729,
            'B7':3951,
            'C8':4186,
            'C#8':4435,
            'D8':4699,
            'D#8':4978,
            'E8':5274,
            'F8':5588,
            'F#8':5920,
            'G8':6272,
            'G#8':6645,
            'A8':7040,
            'A#8':7459,
            'B8':7902,
            'C9':8372,
            'C#9':8870,
            'D9':9397,
            'D#9':9956,
            'E9':10548,
            'F9':11175,
            'F#9':11840,
            'G9':12544,
            'G#9':13290,
            'A9':14080,
            'A#9':14917,
            'B9':15804
        }

    class get_input(object):
        def left_key():
            if (ljinux.io.buttonl.value == True):
                return True
            else:
                return False
        def right_key():
            if (ljinux.io.buttonr.value == True):
                return True
            else:
                return False
        def enter_key():
            if (ljinux.io.buttone.value == True):
                return True
            else:
                return False
        def volume():
                return ljinux.io.get_volume_val()
        def serial():
            return input()

def lock(it_is): # to be made part of hs app
    if (it_is):
        oss.farland.pixel(2, 9, False)
        oss.farland.pixel(3, 9, False)
        oss.farland.pixel(4, 9, False)
        oss.farland.pixel(5, 9, False)
        oss.farland.pixel(6, 9, False)
        oss.farland.pixel(7, 9, False)
        oss.farland.pixel(8, 9, False)
        oss.farland.pixel(2, 8, False)
        oss.farland.pixel(3, 8, False)
        oss.farland.pixel(4, 8, False)
        oss.farland.pixel(5, 8, False)
        oss.farland.pixel(6, 8, False)
        oss.farland.pixel(7, 8, False)
        oss.farland.pixel(8, 8, False)
        oss.farland.pixel(2, 7, False)
        oss.farland.pixel(3, 7, False)
        oss.farland.pixel(4, 7, False)
        oss.farland.pixel(6, 7, False)
        oss.farland.pixel(7, 7, False)
        oss.farland.pixel(8, 7, False)
        oss.farland.pixel(2, 6, False)
        oss.farland.pixel(3, 6, False)
        oss.farland.pixel(4, 6, False)
        oss.farland.pixel(5, 6, False)
        oss.farland.pixel(6, 6, False)
        oss.farland.pixel(7, 6, False)
        oss.farland.pixel(8, 6, False)
        oss.farland.pixel(2, 5, False)
        oss.farland.pixel(3, 5, False)
        oss.farland.pixel(4, 5, False)
        oss.farland.pixel(5, 5, False)
        oss.farland.pixel(6, 5, False)
        oss.farland.pixel(7, 5, False)
        oss.farland.pixel(8, 5, False)
        #the hinge thing
        oss.farland.pixel(7, 4, False)
        oss.farland.pixel(7, 3, False)
        oss.farland.pixel(6, 2, False)
        oss.farland.pixel(5, 2, False)
        oss.farland.pixel(4, 2, False)
        oss.farland.pixel(3, 3, False)
        oss.farland.pixel(3, 4, False)
        oss.farland.pixel(3, 5, False)
    else:
        oss.farland.pixel(2, 9, False)
        oss.farland.pixel(3, 9, False)
        oss.farland.pixel(4, 9, False)
        oss.farland.pixel(5, 9, False)
        oss.farland.pixel(6, 9, False)
        oss.farland.pixel(7, 9, False)
        oss.farland.pixel(8, 9, False)
        oss.farland.pixel(2, 8, False)
        oss.farland.pixel(3, 8, False)
        oss.farland.pixel(4, 8, False)
        oss.farland.pixel(5, 8, False)
        oss.farland.pixel(6, 8, False)
        oss.farland.pixel(7, 8, False)
        oss.farland.pixel(8, 8, False)
        oss.farland.pixel(2, 7, False)
        oss.farland.pixel(3, 7, False)
        oss.farland.pixel(4, 7, False)
        oss.farland.pixel(6, 7, False)
        oss.farland.pixel(7, 7, False)
        oss.farland.pixel(8, 7, False)
        oss.farland.pixel(2, 6, False)
        oss.farland.pixel(3, 6, False)
        oss.farland.pixel(4, 6, False)
        oss.farland.pixel(5, 6, False)
        oss.farland.pixel(6, 6, False)
        oss.farland.pixel(7, 6, False)
        oss.farland.pixel(8, 6, False)
        oss.farland.pixel(2, 5, False)
        oss.farland.pixel(3, 5, False)
        oss.farland.pixel(4, 5, False)
        oss.farland.pixel(5, 5, False)
        oss.farland.pixel(6, 5, False)
        oss.farland.pixel(7, 5, False)
        oss.farland.pixel(8, 5, False)
        #the hinge thing
        oss.farland.pixel(7, 3, False)
        oss.farland.pixel(6, 2, False)
        oss.farland.pixel(5, 2, False)
        oss.farland.pixel(4, 2, False)
        oss.farland.pixel(3, 3, False)
        oss.farland.pixel(3, 4, False)
        oss.farland.pixel(3, 5, False)

oss = ljinux()
oss.farland.setup()
#oss.farland.draw_top()
#oss.farland.draw_init_clock()

#with open("/boot_out.txt", "r") as file:
#    if 'Unlocked' in file.read():
#        lock(False)
#    else:
#        lock(True)
#    file.close()

oss.farland.frame()
time.sleep(.4)

# initial center of the circle
center_x = 64
center_y = 40
# how fast does it move in each direction
x_inc = 1
y_inc = 1
# what is the starting radius of the circle
radius = 8
frame_time_old = time.monotonic()
frame_time_new = None

try:
    while not Exit:
        oss.based.autorun()
        ## undraw the previous circle
        #oss.farland.draw_circle(center_x, center_y, radius, col=0)
        #
        ## if bouncing off right
        #if center_x + radius >= oss.farland.width():
        #    # start moving to the left
        #    x_inc = -1
        ## if bouncing off left
        #elif center_x - radius < 0:
        #    # start moving to the right
        #    x_inc = 1
        #
        ## if bouncing off top
        #if center_y + radius >= oss.farland.height():
        #    # start moving down
        #    y_inc = -1
        ## if bouncing off bottom
        #elif center_y - radius < 0 + 12:
        #    # start moving up
        #    y_inc = 1
        #
        ## go more in the current direction
        #center_x += x_inc
        #center_y += y_inc
        #
        ## draw the new circle
        #oss.farland.draw_circle(center_x, center_y, radius)
        # show all the changes we just made
        #oss.farland.draw_clock()
        oss.farland.frame()
        #oss.farland.fps()
        gc.collect()
        print("Shell exited with exit code ", end='')
        print(Exit_code)
        time.sleep(1)
except EOFError:
    print("\nSerial Ctrl + D caught, exiting")
    ljinux.farland.clear()
    time.sleep(1)
    ljinux.io.led.value = False
    gc.collect()
