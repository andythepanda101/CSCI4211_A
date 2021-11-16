from pj2.simulator import to_layer_five
from pj2.packet import send_ack

class B:
    def __init__(self):
        # initialization of the state of B
        # the sequence number expected by receiver
        self.recseqnum = 1
        return

    def B_input(self, pkt):
        # process the packet recieved from the layer 3
        # verify checksum
        # if checksum is correct and the packet is the expected number
        if pkt.checksum == pkt.get_checksum() and pkt.seqnum == self.recseqnum:
            to_layer_five("B", pkt.payload.data)
            # send ACK
            send_ack("B", pkt.seqnum)
            self.recseqnum += 1
        # we ignore out of order packets and wait for sender timeout for sender to retransmit
        # B.py guarentees acknowledge a pkt and send ACK in correct order
        return

    def B_output(self, m):
        return

    def B_handle_timer(self):
        return


b = B()
