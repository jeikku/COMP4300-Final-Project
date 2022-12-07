#
# COMP 4300 Final Project - By: Jacob Broggy & Sebastien Pichon
# File containing all the algorithms
#

#constructor class fifo (array of packets, delay)
class FIFO:
    def __init__(self, packets, delay):
        self.packets = packets
        self.delay = delay

    def scheduler(self):
        #take the ordered array of packets and put them through the algorithm.
        packet_wait_time = []
        curr_time = 0
        prev_time = 0
        count = 0
        prev_completion_time = 0
        for packet in packets:
            arrival_time = self.delay * count
            wait_time = prev_completion_time - arrival_time
            if wait_time < 0:
                wait_time = 0
            completion_time = arrival_time + packet + wait_time
            packet_wait_time.append(completion_time-arrival_time)
            curr_time += completion_time
            prev_completion_time = completion_time
            count += 1
            #testing output
            print('---[Packet ' + str(count) + ' Size:' + str(packet) + ']---')
            print('Arrival Time: ' + str(arrival_time))
            print('Wait Time: ' + str(wait_time))
            print('Completion Time: ' + str(completion_time))
            print('Packet Wait Time: ' + str(completion_time-arrival_time) + '\n')
            
#constructor class fifo (array of packets, delay)
class RoundRobin:
    def __init__(self, packets, delay):
        self.packets = packets
        self.delay = delay

    def scheduler(self):
        #take the ordered array of packets and put them through the algorithm.
        

#testing area
packets = [4, 7, 9, 12, 3]
myAlg = FIFO(packets, 5)
myAlg.scheduler()