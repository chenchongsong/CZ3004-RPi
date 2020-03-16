#!/usr/bin/env python

# coding: utf-8

import socket, sys
import time
import threading

import io
import struct
import picamera
from PIL import Image


class im_conn(object):

    def __init__(self):
        self.ip = '192.168.18.18'
        self.port = 8000
        self.client = None
        self.conn = None
        self.im_conn_flag = False
        self.camera = picamera.PiCamera()
#        self.camera.vflip = True
#        self.camera.hflip = True
        self.camera.framerate = 30
        self.camera.start_preview()
        time.sleep(2)
        

    def init_im_conn(self):
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print('IMG Socket created at', self.ip)
            self.conn.bind((self.ip, self.port))
            print ('Waiting for client connection')
            self.conn.listen(5)
            self.client = self.conn.accept()[0]
            self.w_client = self.client.makefile('wb')
##            self.r_client = self.client.makefile('rb')
            print('Created IMG connection with client')
            self.im_conn_flag = True



        except Exception as e:
            print('ERROR init_img_conn', str(e))

    def close_im_conn(self):
        try:
            self.camera.stop_preview()
            if self.conn:
                self.conn.close()
            if self.client:
                self.client.close()
            print('Closed IMG Connection')
        except Exception as e:
            print('ERROR IMG close connection')

    def check_conn_status(self):

        return self.im_conn_flag


    def write_image(self, img_coor):

        try:
            stream = io.BytesIO()
            self.camera.capture(stream, 'jpeg')

            #ending marker
            if b'end' in img_coor:
                self.w_client.write(struct.pack('<L', 0))
                self.w_client.flush()
                print('\nprocessing images')
            else:
                self.w_client.write(struct.pack('<L', stream.tell()+len(img_coor)+1))
                self.w_client.flush()
                stream.seek(0)
                self.w_client.write(stream.read()+b'\n'+img_coor)
                print('\nwrote IMG')

        except Exception as e:
            print('ERROR IMG write', str(e))


    def read_image(self):

        try:
            image_data = self.client.recv(1024)
            return image_data
##            image_len = struct.unpack('<L', self.r_client.read(struct.calcsize('<L')))[0]
####            if not image_len:
####                break
##            
##            image_stream = io.BytesIO()
##            image_stream.write(self.r_client.read(image_len))
##            image_stream.seek(0)
##
##            if image_stream!=b'':
##                image_data = image_stream.getvalue()
##                image_stream.seek(0)
##                image_stream.truncate()
##                print('\nread from IMG')
##
##                return image_data
##
##        except struct.error:
##            pass
        
        except Exception as e:
            print('ERROR IMG read message', str(e))



##if __name__ == "__main__":
##    server = server_conn()
##    server.init_conn()
##
####    server.send_image()
##    server.send_image()
####    server.send_image()
####    server.send_image()
####    for i in range (0,3):
####        server.send_image()
####        time.sleep(2)
##
##    server.close_conn()


