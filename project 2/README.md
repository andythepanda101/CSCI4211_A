# CSCI4211_rdt_python


## Andy Chen, Zhang CSCI4211, 15/11/2021 Python3,Server.py,,Server.py

## Compilation/Code Setup

There is no compilation. The necessary setup is unzipping the folder containing the files. Find `AndyChen-Project2.zip`, then extract the contents, `Project 1` to any destination of your choice. Also ensure that a version of Python3 is installed on the machine.

## Execution/Running

1. Open a terminal. Navigate to the directory containing the unzipped Project 2 folder, which should be `<dir>/Project 2/`
2. Navigate to either the `go_back_n` or `stop_and_wait` folder containing the `main.py` file and `pj2` folder
3. You can change the simulator settings to what you desire by editing `pj2/simulator.py`
4. Run the simulator with the command `python3 main.py`

## Description

The program simulates sending packets from a Sender A to a Receiver B using 2 different reliable data transfer protocols, Go Back N, and Stop and Wait (aka. rdt3.0, and Alternating-Bit-Protocol). The simulator uses A to send packets to B under different conditions based on the protocol used and the simulator settings.

### Stop and Wait
Stop and Wait is a simple protocol where the sender A sends a packet to the receiver B, then stops sending while waiting for B to receive the packet and send an acknowledgement to A. If the sender A doesn't receive a response of acknowledgement from B in time, A will resend the packet for B to resend the ack.

#### A Initialization
* Sets the expected RTT of sending a packet and receiving a response.
* Initializes a var to track the current sequence number of the packet that's to be sent, either number 0 or 1.
* Initializes a var to track the packet sent in case a retransmission is necessary.
* Initializes a var to track the current state of the A, either waiting to send a packet to B, or waiting for a ack response from B.
#### A_input()
* If A is in state waiting for ack and receives an ack packet:
* And if packet is not corrupted and it's the expected ack, stop the timer, flips the sequence no. value (if it's 0, change to 1, and vice versa), then sets the state to be ready to send.
* And if the packet is corrupted and/or not the expected one, resend the packet.
#### A_output()
* If A is in state waiting to send packet, then send the next packet and start the timer, replace the packet stored in the packet tracker with the current sent packet, and changes state to be waiting for a ack response.
#### A_timerinterrupt()
* Called when A timeouts on waiting for a correct ack response packet from B, resend the packet and restart A's timer.
#### B Initialization
* Initializes a variable to track the current expected packets sequence number, either 0 or 1.
* Initializes a variable to track the previous acknowledged packet's sequence number
#### B_input()
* When B receives a packet and it's not corrupted and it's the expected sequence number, print the data, send acknowledgement of that packet to A, and flip the expected packet and previous packet tracker variables.
* Otherwise, this means that the packet was corrupted and/or the wrong packet was sent, request a resend of the previous packet from A.

### Go Back N
Go Back N has a sliding window, a range of packets to send and to be sent. Upon receiving an ack for one of the sent packets, slide the window forward to the new oldest unacked packet. There is a timer for the "left most" (tracked by variable "base") packet in the window and when it times out, all send packets are resent.
The way A.py is implemented in this Go Back N version, the buffer's sole purpose is to act just as a large sliding window, and will not buffer additional packets outside the window. There is commented out code for a theoretical implementation where we would want the window, and the extra buffer for unsent packets.
#### A Initialization
* Initializes the expected RTT of sending a packet and receiving a response.
* Initializes variables to track the base and next sequence number of the packet to send, for the window
* Initializes a circular buffer to act as the window for A
#### A_input()
* If an ack packet is received by A and it's not corrupted and is an  expected ack num, shift the window forward accordingly (because of the way B receiver is set up, it only acks packets received in order, so upon receiving an ack, it's assumed that all previous packets have been ack'd as well regardless of if those acks have successfully been received by A or not). Then do the following:
* If the new "left most" packet (tracked by variable "base") of the window has not yet been sent, then A doesn't need a timer so turn it off
* Otherwise start a new timer for the new "left most" packet in the window
#### A_output()
* If the buffer is full, drop the packet
* Otherwise, send the next packet and add it to buffer, if the packet just sent is now the new "left most" packet in buffer, start a timer for it.
#### A_timerinterrupt()
* If the timer expires, call this. This means that the "left most" packet in the window/buffer has timed out without receiving an ack for it, retransmit all sent packets
#### B Initialization
* Initializes a variable to track the expected sequence number
#### B_input()
* If the packet is not corrupted and it's the expected sequence number (in order), send ack for the packet and update the next expected sequence number.

### Test Cases
#### Stop and Wait
Stop and wait works in all the conditions I've tested, and works every time with the default settings in simulator.py
#### Go Back N
Go Back N works every time with the default settings in simulator.py and with default buffer size 10, and testing increasing num packets to send doesn't affect it. This works up until lostprob = 0.6 and corruptprob = 0.5. At this stage, increasing the buffer/window size will accommodate for that and it becomes reliable again.
