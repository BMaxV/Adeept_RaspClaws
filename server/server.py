#!/usr/bin/env/python
# File name   : server.py
# Description : main programe for RaspClaws
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/08/22

import socket
import time
import threading
import move
import adafruit_pca9685
from rpi_ws281x import *
import argparse
import os
import FPV
import psutil




import LED

# this is taken from one of the adafruit examples, let's assume
# everything is identical, because it's using the same pca?

from board import SCL, SDA
import busio

step_set = 1
speed_set = 100
DPI = 17

new_frame = 0
direction_command = 'no'
turn_command = 'no'

i2c = busio.I2C(SCL,SDA)
pwm = adafruit_pca9685.PCA9685(i2c)
pwm.set_pwm_freq(50)
LED = LED.LED()

SmoothMode = 0
steadyMode = 0

def breath_led():
    LED.breath(255)

def  ap_thread():
    os.system("sudo create_ap wlan0 eth0 AdeeptCar 12345678")


def get_cpu_tempfunc():
    """ Return CPU temperature """
    result = 0
    mypath = "/sys/class/thermal/thermal_zone0/temp"
    with open(mypath, 'r') as mytmpfile:
        for line in mytmpfile:
            result = line

    result = float(result)/1000
    result = round(result, 1)
    return str(result)


def get_gpu_tempfunc():
    """ Return GPU temperature as a character string"""
    res = os.popen('/opt/vc/bin/vcgencmd measure_temp').readline()
    return res.replace("temp=", "")


def get_cpu_use():
    """ Return CPU usage using psutil"""
    cpu_cent = psutil.cpu_percent()
    return str(cpu_cent)


def get_ram_info():
    """ Return RAM usage using psutil """
    ram_cent = psutil.virtual_memory()[2]
    return str(ram_cent)


def get_swap_info():
    """ Return swap memory  usage using psutil """
    swap_cent = psutil.swap_memory()[3]
    return str(swap_cent)


def info_get():
    global cpu_t,cpu_u,gpu_t,ram_info
    while 1:
        cpu_t = get_cpu_tempfunc()
        cpu_u = get_cpu_use()
        ram_info = get_ram_info()
        time.sleep(3)


def move_thread():
    # so the global keyword gives access to certain values,
    # between threads
    
    # because it's a daemon thread, it will die when the main process
    # dies.
    step_set
    stand_stu = 1
    while 1:
        if not self.steadyMode:
            if direction_command == 'forward' and turn_command == 'no':
                if SmoothMode:
                    move.dove(step_set,35,0.001,DPI,'no')
                    step_set += 1
                    if step_set == 5:
                        step_set = 1
                    continue
                else:
                    move.move(step_set, 35, 'no')
                    time.sleep(0.1)
                    step_set += 1
                    if step_set == 5:
                        step_set = 1
                    continue
            elif direction_command == 'backward' and turn_command == 'no':
                if SmoothMode:
                    move.dove(step_set,-35,0.001,DPI,'no')
                    step_set += 1
                    if step_set == 5:
                        step_set = 1
                    continue
                else:
                    move.move(step_set, -35, 'no')
                    time.sleep(0.1)
                    step_set += 1
                    if step_set == 5:
                        step_set = 1
                    continue
            else:
                pass

            if turn_command != 'no':
                if SmoothMode:
                    move.dove(step_set,35,0.001,DPI,turn_command)
                    step_set += 1
                    if step_set == 5:
                        step_set = 1
                    continue
                else:
                    move.move(step_set, 35, turn_command)
                    time.sleep(0.1)
                    step_set += 1
                    if step_set == 5:
                        step_set = 1
                    continue
            else:
                pass

            if turn_command == 'no' and direction_command == 'stand':
                move.stand()
                step_set = 1
            pass
        else:
            move.steady_X()
            move.steady()
            #print('steady')
            #time.sleep(0.2)


def info_send_client():
    SERVER_IP = addr[0]
    SERVER_PORT = 2256   #Define port serial 
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)
    Info_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Set connection value for socket
    Info_Socket.connect(SERVER_ADDR)
    print(SERVER_ADDR)
    while 1:
        try:
            Info_Socket.send((get_cpu_tempfunc()+' '+get_cpu_use()+' '+get_ram_info()).encode())
            time.sleep(1)
        except:
            pass


def FPV_thread():
    """this is an openCV communication thread
    """
    fpv
    fpv = FPV.FPV()
    fpv.capture_thread(addr[0])

def destory():
    move.clean_all()

class RobotController():
        
    def run(self):
        # these are the variables that would be
        # access by the move thread, if it exists. so.
        # if I don't have a move thread, I don't need these.
        # or not like this.
        # direction_command, turn_command, SmoothMode, steadyMode

        while True:
            data = str(self.tcpCliSock.recv(self.BUFFER_SIZE).decode())
            if not data:
                continue
            
            self.set_inputs_for_moving_thread(data)
            self.set_inputs_for_LED(data)
            self.send_client_data(data)
            self.set_FPV_inputs(data)
            
    def set_FPV_inputs(data):
        if self.FPV_thread!=None:
            if 'Render' in data:
                if FPV.frameRender:
                    FPV.frameRender = 0
                else:
                    FPV.frameRender = 1

            elif 'WBswitch' in data:
                if FPV.lineColorSet == 255:
                    FPV.lineColorSet = 0
                else:
                    FPV.lineColorSet = 255

            elif 'lip1' in data:
                try:
                    set_lip1=data.split()
                    lip1_set = int(set_lip1[1])
                    FPV.linePos_1 = lip1_set
                except:
                    pass

            elif 'lip2' in data:
                try:
                    set_lip2=data.split()
                    lip2_set = int(set_lip2[1])
                    FPV.linePos_2 = lip2_set
                except:
                    pass

            elif 'err' in data:#2 end
                try:
                    set_err=data.split()
                    err_set = int(set_err[1])
                    FPV.findLineError = err_set
                except:
                    pass

            elif 'setEC' in data:#Z
                ECset = data.split()
                try:
                    fpv.setExpCom(int(ECset[1]))
                except:
                    pass

            elif 'defEC' in data:#Z
                fpv.defaultExpCom()

    def set_inputs_for_moving_thread(self,data):
        if self.moving_thread!=None:
            
            elif 'forward' == data:
                direction_command = 'forward'
            elif 'backward' == data:
                direction_command = 'backward'
            elif 'DS' in data:
                direction_command = 'stand'

            elif 'left' == data:
                turn_command = 'left'
            elif 'right' == data:
                turn_command = 'right'
            elif 'leftside' == data:
                turn_command = 'left'
            elif 'rightside'== data:
                turn_command = 'right'
            elif 'TS' in data:
                turn_command = 'no'

            elif 'headup' == data:
                move.look_up()
            elif 'headdown' == data:
                move.look_down()
            elif 'headhome' == data:
                move.look_home()

            elif 'headleft' == data:
                move.look_left()
            elif 'headright' == data:
                move.look_right()
    
    def set_inputs_for_LED(data):
        if self.LED!=None:
            if 'wsR' in data:
                try:
                    set_R=data.split()
                    ws_R = int(set_R[1])
                    LED.colorWipe(Color(ws_R,ws_G,ws_B))
                except:
                    pass
            elif 'wsG' in data:
                try:
                    set_G=data.split()
                    ws_G = int(set_G[1])
                    LED.colorWipe(Color(ws_R,ws_G,ws_B))
                except:
                    pass
            elif 'wsB' in data:
                try:
                    set_B=data.split()
                    ws_B = int(set_B[1])
                    LED.colorWipe(Color(ws_R,ws_G,ws_B))
                except:
                    pass
    
    def send_client_data(self,data):
        if self.tcpCliSock!=None:
            if 'FindColor' in data:
                LED.breath_status_set(1)
                fpv.FindColor(1)
                tcpCliSock.send(('FindColor').encode())

            elif 'WatchDog' in data:
                LED.breath_status_set(1)
                fpv.WatchDog(1)
                tcpCliSock.send(('WatchDog').encode())

            elif 'steady' in data:
                LED.breath_status_set(1)
                LED.breath_color_set('blue')
                steadyMode = 1
                tcpCliSock.send(('steady').encode())

            elif 'funEnd' in data:
                LED.breath_status_set(0)
                fpv.FindColor(0)
                fpv.WatchDog(0)
                steadyMode = 0
                tcpCliSock.send(('FunEnd').encode())

            elif 'Smooth_on' in data:
                SmoothMode = 1
                tcpCliSock.send(('Smooth_on').encode())

            elif 'Smooth_off' in data:
                SmoothMode = 0
                tcpCliSock.send(('Smooth_off').encode())

            elif 'Switch_1_on' in data:
                switch.switch(1,1)
                tcpCliSock.send(('Switch_1_on').encode())

            elif 'Switch_1_off' in data:
                switch.switch(1,0)
                tcpCliSock.send(('Switch_1_off').encode())

            elif 'Switch_2_on' in data:
                switch.switch(2,1)
                tcpCliSock.send(('Switch_2_on').encode())

            elif 'Switch_2_off' in data:
                switch.switch(2,0)
                tcpCliSock.send(('Switch_2_off').encode())

            elif 'Switch_3_on' in data:
                switch.switch(3,1)
                tcpCliSock.send(('Switch_3_on').encode())

            elif 'Switch_3_off' in data:
                switch.switch(3,0)
                tcpCliSock.send(('Switch_3_off').encode())

            if 'CVFL' in data:#2 start
                if not FPV.FindLineMode:
                    FPV.FindLineMode = 1
                    tcpCliSock.send(('CVFL_on').encode())
                else:
                    # move.motorStop()
                    # FPV.cvFindLineOff()
                    FPV.FindLineMode = 0
                    tcpCliSock.send(('CVFL_off').encode())
    
    def __init__(self):
        self.moving_thread = None
        self.info_thread = None
        
        self.step_set = 1
        self.speed_set = 100
        self.DPI = 17

        self.new_frame = 0
        self.direction_command = 'no'
        self.turn_command = 'no'
        
        # this is hardware again.
        
        i2c = busio.I2C(SCL,SDA)
        self.pwm = adafruit_pca9685.PCA9685(i2c)
        self.pwm.set_pwm_freq(50)
        self.LED = LED.LED()
        
        self.ws_R = 0
        self.ws_G = 0
        self.ws_B = 0
        
        self.SmoothMode = 0
        self.steadyMode = 0
        
        self.HOST = ''
        self.PORT = 10223                              
        self.BUFFER_SIZE = 1024                             
        self.ADDR = (HOST, PORT)
        
    def init_LED_thread(self):
        led_threading = threading.Thread(target=breath_led)         #Define a thread for LED breathing
        led_threading.setDaemon(True)                             #'True' means it is a front thread,it would close when the mainloop() closes
        led_threading.start()                                     #Thread starts
        LED.breath_color_set('blue')
        
    def init_move_thread(self):
        # https://docs.python.org/2/library/threading.html#thread-objects
        # look for daemon
        self.moving_thread=threading.Thread(target=move_thread)
        
        # 'True' means it is a front thread,
        # it would close when the mainloop() closes
        self.moving_thread.daemon = True                         
        self.moving_thread.start()                                 
        
    def init_info_thread(self):
        """
        this creates a thread, to create a socket to send ONE MESSAGE?
        For fucks sake...
        """
        # https://docs.python.org/2/library/threading.html#thread-objects
        # look for daemon
        self.info_thread = threading.Thread(target=info_send_client) 
        
        # 'True' means it is a front thread,
        # it would close when the mainloop() closes  
        self.info_thread.daemon = True                             
        self.info_thread.start()                                     

    
    def initialize_FPV(self):
        # threading.Thread creates a new thread
        # target is the executed executable in this case a function that
        # is then being run by the thread.
        # in this case it's targeting FPV, which is this robots 
        # openCV camera thing, which I don't necessarily want from the the start.
        self.fps_threading = threading.Thread(target=FPV_thread)         #Define a thread for FPV and OpenCV
        self.fps_threading.setDaemon(True)                             #'True' means it is a front thread,it would close when the mainloop() closes
        self.fps_threading.start()                                     #Thread starts
    
    def startup_wait(self,ADDR,FPV_thread):
    
        try:
            # if this works it breaks and starts running...
            # so this is a "starup wait thing"
            # it's creating a TCP socket and waiting for input? or connection?
            # hmmmmmmm. not sure if bad idea. might be. might be a good idea.
            self.tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcpSerSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            self.tcpSerSock.bind(ADDR)
            self.tcpSerSock.listen(5)                      #Start server,waiting for client
            print('waiting for connection...')
            self.tcpCliSock, self.other_addr = self.tcpSerSock.accept()
            print('...connected from :', self.other_addr)
            
            if False:
                
            
        except:
            pass
    
    def receiving_startup(self,ap_thread):
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect(("1.1.1.1",80))
            ipaddr_check=s.getsockname()[0]
            s.close()
            print(ipaddr_check)
        except:
            ap_threading = threading.Thread(target=ap_thread)   #Define a thread for data receiving
            ap_threading.setDaemon(True)                          #'True' means it is a front thread,it would close when the mainloop() closes
            ap_threading.start()                                  #Thread starts

            LED.colorWipe(Color(0,16,50))
            time.sleep(1)
            LED.colorWipe(Color(0,16,100))
            time.sleep(1)
            LED.colorWipe(Color(0,16,150))
            time.sleep(1)
            LED.colorWipe(Color(0,16,200))
            time.sleep(1)
            LED.colorWipe(Color(0,16,255))
            time.sleep(1)
            LED.colorWipe(Color(35,255,35))

def main():
    # do just Raspi things, if that works i can worry about starting 
    # up hardware.
    hardware = False
    R = RobotController()
    
    if hardware:
        import setup_hardware
        setup_hardware.main()
        R.initialize_FPV()



    while  1:
        R.receiving_startup(ap_thread)
    
        if R.startup_wait(ADDR,FPV_thread):
            break
    try:
        LED.breath_status_set(0)
        LED.colorWipe(Color(64,128,255))
    except:
        pass

    # try:
    run()   
    # except:
    LED.colorWipe(Color(0,0,0))
    destory()
    move.clean_all()
    switch.switch(1,0)
    switch.switch(2,0)
    switch.switch(3,0)

if __name__ == '__main__':
    #main()
    a=1
