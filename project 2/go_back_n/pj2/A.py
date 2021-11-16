from pj2.simulator import sim
from pj2.simulator import to_layer_three
from pj2.event_list import evl
from pj2.packet import *
from pj2.circular_buffer import circular_buffer

# GBN implementation of the methods

class A:
    def __init__(self):
        # using figure 3.20 in our textbook
        # initialization of the state of A
        self.estimated_rtt = 30
        # window pointers
        self.base = 1
        self.nextseqnum = 1
        # OK SO THE INSTRUCTIONS ARE CONFUSING, SO FOR MY PURPOSES
        # THE BUFFERSIZE IS THE WINDOW SIZE
        self.windowsize = 8 # UNUSED I GUESS
        # setup circular buffer, arg is size of buffer
        buffer_size = 10 # change this to change buffer size
        self.buffer = circular_buffer(buffer_size)
        """ if we want an actual buffer that's window size + unsent packets
        # if so then we treat the first circular buffer as window, the second to buffer
        # packets to send that are outside window scope
        self.extrabuffer = circular_buffer(10)
        #"""
        return

    def A_input(self, pkt):
        # upon RECEIVING data from the other side
        # check if packet corrupted or not
        if pkt.checksum == pkt.get_checksum() and pkt.acknum >= self.base: # if not corrupted and not old unexpected ACK (ack num > base)

            # because of how B.py is setup, we can assume with any ack packet
            # recieved here that all the previous seq nums have been ack'd as well
            # we pop the proper number accordingly
            while self.base < pkt.acknum + 1:
                self.buffer.pop()
                # print("popped") # for testing purposes
                self.base += 1 # increment base as window slides
            # buffer empty (window empty)
            if self.base == self.nextseqnum:
                evl.remove_timer()
            else: # timer for expecting ack for new base of window
                """ if we want an actual buffer that's window size + unsent packets
                xbuf = self.extrabuffer.read_all()
                xbuflen = len(xbuf)
                i = 0
                print("boop")
                while len(self.buffer.read_all()) < 8 and xbuflen > 0:
                    to_layer_three("A", xbuf[i])
                    self.buffer.push(xbuf[i])
                    self.extrabuffer.pop()
                    xbuflen -= 1
                    i += 1
                    self.nextseqnum += 1
                    print("test")
                #"""
                evl.start_timer("A", self.estimated_rtt)
        else: # checksum failed, corrupted and/or old unexpected ACK, ignore
            return -1

        return

    def A_output(self, m):
        # called from layer 5, pass the data to the other side
        # check if buffer full

        if self.buffer.isfull(): # buffer is full
            return -1 # do nothing (drop packet m)
        else:
            """ uncomment this and the rest of the labeled lines if we want an
            # actual buffer that's window size + unsent packets, also unindent this
            elif self.nextseqnum < (self.base + self.windowsize): # if nextseqnum is within our window
            #"""
            # construct and send packet to B, add to buffer to await ack
            pkt = packet(seqnum=self.nextseqnum, payload=m)
            to_layer_three("A", pkt) # send packet
            self.buffer.push(pkt) # add to buffer
            if self.base == self.nextseqnum: # start timer to await ack for the base pck in buffer window
                evl.start_timer("A",self.estimated_rtt)
            self.nextseqnum += 1
        """ if we want an actual buffer that's window size + unsent packets
        else:
            pkt = packet(seqnum=self.nextseqnum, payload=m)
            self.extrabuffer.push(pkt) # just buffer because it's outside window
        # """
        return

    def A_handle_timer(self):
        # handler for time interrupt
        # resend the packet as needed
        # buffer contains all the sent packets in the window, resend all on
        # timeout of base, which should be the only thing timing out
        evl.start_timer("A", self.estimated_rtt)
        for p in self.buffer.read_all():
            to_layer_three("A", p)

        return


a = A()
