#
# COMP 4300 Final Project - By: Jacob Broggy & Sebastien Pichon
# File containing all the algorithms
#

class Packet:
    def __init__(self, header_id, size, prio):
        self.header_id = header_id
        self.size = size #time it takes to process a packet
        self.prio = prio #priority class given to the packet

#constructor class fifo (array of packets, delay)
class FIFO:
    def __init__(self, packets, delay):
        self.packets = packets
        self.delay = delay

    def scheduler(self):
        #take the ordered array of packets and put them through the algorithm.
        packet_wait_time = []
        count = 0
        prev_completion_time = 0
        for packet in packets:
            arrival_time = self.delay * count
            wait_time = prev_completion_time - arrival_time
            if wait_time < 0:
                wait_time = 0
            completion_time = arrival_time + packet.size + wait_time
            packet_wait_time.append(completion_time-arrival_time)
            prev_completion_time = completion_time
            count += 1
            #testing output
            print('---[Packet ' + str(count) + ' Size:' + str(packet.size) + ']---')
            print('Arrival Time: ' + str(arrival_time))
            print('Wait Time: ' + str(wait_time))
            print('Completion Time: ' + str(completion_time))
            print('Packet Total Processing Time: ' + str(completion_time-arrival_time) + '\n')


class PriorityQueue:
    def __init__(self, packets, delay):
        self.packets = packets
        self.delay = delay
    
    def scheduler(self):
        packet_wait_time = []
        doing_work = False
        packet_buffer = []
        
        packet_count = 0
        curr_time = 0
        start_time = 0
        processing_time = 0
        #track arrival time of every packet = header_id * delay
        while packet_count < len(self.packets) or len(packet_buffer) > 0: #while there are still packets incoming
            #add in a packet to the buffer when it arrives
            if curr_time == packet_count * self.delay and packet_count < len(self.packets):
                packet_buffer.append(self.packets[packet_count])
                
                packet_ID = packets[packet_count].header_id
                packet_size = packets[packet_count].size
                packet_prio = packets[packet_count].prio
                #print("+Packet #" + str(packet_ID) + "(size: " +str(packet_size) + ", prio: " + str(packet_prio) + ") has been added to the buffer.")
                packet_count += 1
                
            #check if the packet that was being worked on is done
            if doing_work and curr_time - start_time == processing_time:
                doing_work = False
                packet_wait_time.append(curr_time - start_time)
                
                packet_ID = packet_buffer[0].header_id
                packet_size = packet_buffer[0].size
                packet_prio = packet_buffer[0].prio
                packet_arrival_time = packet_ID * self.delay
                wait_time = (curr_time - packet_size) - packet_arrival_time
                print('---[Packet ' + str(packet_ID) + ' Size:' + str(packet_size) + ' Prio:' + str(packet_prio) + ']---')
                print('Arrival Time: ' + str(packet_arrival_time))
                print('Wait Time: ' + str(wait_time))
                print('Completion Time: ' + str(curr_time))
                print("Packet Total Processing Time: " + str(curr_time - packet_arrival_time) + "\n")
                packet_buffer.pop(0)
            #if its not currently processing a packet and there are packets in the buffer, start processing the next packet
            if not doing_work and len(packet_buffer) > 0:
                start_time = curr_time
                processing_time = packet_buffer[0].size
                doing_work = True
            #print("curr time: "+str(curr_time))
            #print("*number of packets in buffer = "+str(len(packet_buffer)))
            curr_time += 1

            
#constructor class fifo (array of packets, delay)
class RoundRobin:
    def __init__(self, packets, delay):
        self.packets = packets
        self.delay = delay

    def scheduler(self):
        pass
        #take the ordered array of packets and put them through the algorithm.
        

#testing area
p1 = Packet(0,4,0)
p2 = Packet(1,7,0)
p3 = Packet(2,9,0)
p4 = Packet(3,12,0)
p5 = Packet(4,3,0)
packets = [p1, p2, p3, p4, p5]
myAlg = FIFO(packets, 5)
myAlg.scheduler()

prioAlg = PriorityQueue(packets, 5)
prioAlg.scheduler();