from pj2.simulator import to_layer_five
from pj2.packet import send_ack

class B:
    def __init__(self):
        # initialization of the state of B
        self.recseqnum = 0 # tracks seq no
        self.previous_ack = -1 # last packet ackd by client
        return

    def B_input(self, pkt):
        # process the packet recieved from the layer 3
        # verify checksum
        # send ACK
        # if packet is not corrupted and recieves the expected packet
        if pkt.get_checksum() == pkt.checksum and self.recseqnum == pkt.seqnum:
            to_layer_five("B", pkt.payload.data) # print
            send_ack("B", pkt.seqnum) # send ack to sender
            self.previous_ack = pkt.seqnum # keeps copy of last ackd num
            self.recseqnum = 1 - self.recseqnum # flip to 0 or 1, expected next seq no
        else:
            # else means packet is corrupted and/or wrong packet was sent
            # resend ack for last recieved packet
            send_ack("B", self.previous_ack)

        return

    def B_output(self, m):
        return

    def B_handle_timer(self):
        return


b = B()
