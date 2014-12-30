import zbar
import qrtools
import sys
import pygame
from pygame import mixer
import sqlite3
import webbrowser

# qrcode.py
#
# Original Copyright 2013 psutton <zleap@zleap.net>
# Modified 2014 by AJ NOURI <ajn.bin@gmail.com>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.


class QRCode():

    data = None
    proc = None
    scanner = None

    def qr_handler(self,proc,image,closure):
        # extract results
        for symbol in image:
            if not symbol.count:
                self.data = symbol.data

    def __init__(self):
        self.proc = zbar.Processor()
        self.scanner = zbar.ImageScanner()
        self.scanner.parse_config('enable')

        self.proc.init("/dev/video0")
        self.proc.set_data_handler(self.qr_handler)
        self.proc.visible = True
        #display cam window if True,  hide if False
        self.proc.active = True

    def get_data(self):
        self.proc.process_one()
        return(self.data)



def sqlite_read():
    # READING OPERATIONS
    conn = sqlite3.connect(DBFILENAME)
    cursor = conn.execute("SELECT ID, FNAME, field1 from " + DBNAME)
    for row in cursor:
        print "ID = ", row[0]
        print "File name = ", row[1]
        print "Field1 = ", row[2], "\n"
        print "Operation done successfully";
    conn.close()


def sqlite_lookup(data):
    conn = sqlite3.connect(DBFILENAME)
    cursor = conn.execute(" SELECT FNAME, field1 from " + DBNAME + " where ID = " + data)
    for row in cursor:
        print row
        print row[0]
        print row[1]
    return row[0], row[1]
    conn.close()



DBNAME = 'BARCODETABLE'
DBFILENAME = 'barcodes.db'

inst = QRCode()
while 1:
    try:
        pygame.init()
        data = inst.get_data()

        sqlite_read()
        sound_file, url = sqlite_lookup(data)


        mixer.init()
        mixer.music.set_endevent(pygame.USEREVENT + 1)
        mixer.music.load(sound_file)
        mixer.music.play()

        #webbrowser.open_new(url)

        ev = pygame.event.wait()

    except KeyboardInterrupt:
        print "Bye"
        pygame.quit()
        sys.exit()
