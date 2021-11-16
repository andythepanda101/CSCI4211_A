from typing import Sequence
from pj2.simulator import sim
from pj2.simulator import to_layer_three
from pj2.event_list import evl
from pj2.packet import *
from pj2.circular_buffer import circular_buffer

# rdt3.0 implementation aka Alternating-Bit-Protocol

# declaration of constants
WAIT_FOR_LAYER_5 = 0 # ready to send packet
WAIT_FOR_ACK = 1 # wait expecting packet ack


class A:
    def __init__(self):
        # using figure 3.15 in our textbook
        # initialization of the state of A
        self.estimated_rtt = 30 # yes
        self.nextseqnum = 0 # tracks seq num
        self.current_state = WAIT_FOR_LAYER_5 # state of sender (this class)
        self.previous_packet = None # last packet sent by sender


    def A_input(self, pkt):
        # recieve data from the other side
        # process the ACK, NACK from B
        if self.current_state == WAIT_FOR_ACK:
            # recieved packet, if checksum is correct
            if pkt.get_checksum() == pkt.checksum and pkt.acknum == self.previous_packet.seqnum:
                evl.remove_timer()
                self.nextseqnum = (self.nextseqnum + 1) % 2 # flip to 0 or 1, next seq no
                self.current_state = WAIT_FOR_LAYER_5 # change wait state
            else: # the receieved packet was not what was expected
                # resend packet
                to_layer_three("A", self.previous_packet)

        return

    def A_output(self, m):
        # recieve data from the other side
        # process the ACK, NACK from B
        if self.current_state == WAIT_FOR_LAYER_5:
            # construct and send packet to B
            pkt = packet(seqnum=self.nextseqnum,payload=m)
            to_layer_three("A", pkt)
            # save last packet in case it needs to be resent
            self.previous_packet = pkt
            # send pkt, sender now waits for B's ACK
            self.current_state = WAIT_FOR_ACK
            # start timeout timer for
            evl.start_timer("A", self.estimated_rtt)

    def A_handle_timer(self):
        # handler for time interrupt
        # resend the packet as needed
        # if the timeout happens while server has sent a packet and hasn't received ack
        if self.current_state == WAIT_FOR_ACK:
            # resend the last packet
            to_layer_three("A", self.previous_packet)
            # restart sender timer waiting for ack
            evl.start_timer("A", self.estimated_rtt)

        return


a = A()
