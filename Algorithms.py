#
# COMP 4300 Final Project - By: Jacob Broggy & Sebastien Pichon
#
# Algorithms.py can be run with python3 to produce test data that compares 3 separate algorithms.
# Our research project's main focus is to implement several mock algorithms and test them against the same
# randomized data in order to compare their overall efficiency. We test under the assumption that packets
# will arrive at different times, as is usually the case with realistic network transfer.
# The data can be outputed as console output and with pyplot
#
# The 3 algorithms being tested and compared against each other are:
# - FIFO (First in First Out)
# - Round Robin
# - Priority Queue
#
import random

#constants
PACKET_ARRAY_SIZE = 10 #amount of packets to test
PACKET_MAX_SIZE = 30 #maximum size of individual packet
PACKET_MAX_PRIO = 10 #maximum priority of individual packet
PRINT_OUTPUT = True #boolean which allows you to enable or disable console printing of algorithm output data

#Packet data object class
class Packet:
    def __init__(self, header_id, size, prio, header_class):
        self.header_id = header_id
        self.size = size #time it takes to process a packet
        self.prio = prio #priority class given to the packet
        self.header_class = header_class #header classification to sort the packet in a Round Robin alg
    
    def __cmp__(self, other):
        return cmp(self.prio, other.prio)

#classless function to initalize randomized packet array for testing        
def initialize_packet_array(array_size):
    packet_array = []
    for x in range(array_size):
        packet_id = x
        #generate random packet attributes
        packet_size = random.randint(1,PACKET_MAX_SIZE)
        packet_prio = random.randint(1,PACKET_MAX_PRIO)
        packet_header_class = random.randint(1,3)
        #create the packet
        new_packet = Packet(packet_id, packet_size, packet_prio, packet_header_class)
        #append it to the array
        packet_array.append(new_packet)
    return packet_array
    
#FIFO class which implements the First In First Out algorithm
class FIFO:
    def __init__(self, packets, delay):
        self.packets = packets
        self.delay = delay

    #FIFO scheduling algorithm
    def scheduler(self):
        packet_wait_time = []
        count = 0
        prev_completion_time = 0

        #Process each packet in order. Assuming a buffer of unlimited size / big enough to contain all packets
        for packet in packets:
            arrival_time = self.delay * count
            wait_time = prev_completion_time - arrival_time
            if wait_time < 0:
                wait_time = 0
            completion_time = arrival_time + packet.size + wait_time
            packet_wait_time.append(completion_time-arrival_time)
            prev_completion_time = completion_time
            count += 1

            #testing output (if enabled)
            if PRINT_OUTPUT:
                print('---[Packet ' + str(count) + ' Size:' + str(packet.size) + ']---')
                print('Arrival Time: ' + str(arrival_time))
                print('Wait Time: ' + str(wait_time))
                print('Completion Time: ' + str(completion_time))
                print('Packet Total Processing Time: ' + str(completion_time-arrival_time) + '\n')

class PriorityQueue:
    def __init__(self, packets, delay):
        self.packets = packets
        self.delay = delay
    
    #PriotiyQueue scheduling algorithm
    def scheduler(self):
        packet_wait_time = []
        doing_work = False
        packet_buffer = [] 
        packet_count = 0
        curr_time = 0
        start_time = 0
        processing_time = 0

        #while there are still packets incoming and the buffer is not empty
        while packet_count < len(self.packets) or len(packet_buffer) > 0: 
            #add in a packet to the buffer when it arrives
            if curr_time == packet_count * self.delay and packet_count < len(self.packets):
                packet_buffer.append(self.packets[packet_count])
                #re-sort the priority queue, ignoring the first element
                end_of_buffer = len(packet_buffer)
                if end_of_buffer > 1:
                    packet_buffer[1:end_of_buffer] = sorted(packet_buffer[1:end_of_buffer],key=lambda x: x.prio)
                packet_ID = packets[packet_count].header_id
                packet_size = packets[packet_count].size
                packet_prio = packets[packet_count].prio
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

                #testing output (if enabled)
                if PRINT_OUTPUT:
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
            curr_time += 1
          
#constructor class fifo (array of packets, delay)
class RoundRobin:
    def __init__(self, packets, delay):
        self.packets = packets
        self.delay = delay

    #Link to cycle when all 3 buffers send a packet
    def cycle_3(self, packet_1,packet_2,packet_3):
        quantum = 3
        notDone = 1
        cycles = 0
        elapsed_time = 0
        size_1 = packet_1.size
        size_2 = packet_2.size
        size_3 = packet_3.size

        while size_1 > 0 or size_2 > 0 or size_3 > 0:
            if size_1 > 0:
                size_1 -= quantum
                elapsed_time += quantum
            if size_2 > 0:
                size_2 -= quantum
                elapsed_time += quantum
            if size_3 > 0:
                size_3 -= quantum
                elapsed_time += quantum
            cycles += 1
        return elapsed_time

    #Link to cycle when 2 of the 3 buffers send a packet
    def cycle_2(self, packet_1,packet_2):
        quantum = 3
        notDone = 1
        cycles = 0
        elapsed_time = 0
        size_1 = packet_1.size
        size_2 = packet_2.size

        while size_1 > 0 or size_2 > 0:
            if size_1 > 0:
                size_1 -= quantum
                elapsed_time += quantum
            if size_2 > 0:
                size_2 -= quantum
                elapsed_time += quantum
            cycles += 1
        return elapsed_time

    #Link to cycle a single packet
    def cycle_1(self, packet_1):
        quantum = 3
        notDone = 1
        cycles = 0
        elapsed_time = 0
        size_1 = packet_1.size

        while size_1 > 0:
            if size_1 > 0:
                size_1 -= quantum
                elapsed_time += quantum
            cycles += 1
        return elapsed_time

    #RoundRobin scheduling algorithm
    def scheduler(self):
        #initialize buffers for cycling
        buffer_1 = []
        buffer_2 = []
        buffer_3 = []

        cycle_time = 0
        curr_time = 0
        packet_count = 0
        doing_work = False
        remaining_packets = len(self.packets)
        
        #run the algorithm until all incoming packets have been dealt with
        while len(buffer_1) > 0 or len(buffer_2) > 0 or len(buffer_3) > 0 or remaining_packets > 0:
            if curr_time == packet_count * self.delay and packet_count < len(self.packets):
                #distribute packets into buffers for processing
                if self.packets[packet_count].header_class == 1:
                    buffer_1.append(self.packets[packet_count])
                elif self.packets[packet_count].header_class == 2:
                    buffer_2.append(self.packets[packet_count])
                else:
                    buffer_3.append(self.packets[packet_count])
                
                packet_count += 1
                remaining_packets -= 1
            #if cycler is not running, queue up a new cycle
            if not doing_work:
                if len(buffer_1) > 0 and len(buffer_2) > 0 and len(buffer_3) > 0:
                    cycle_time = self.cycle_3(buffer_1[0],buffer_2[0],buffer_3[0])
                elif len(buffer_1) > 0 and len(buffer_2) > 0:
                    cycle_time = self.cycle_2(buffer_1[0],buffer_2[0])
                elif len(buffer_2) > 0 and len(buffer_3) > 0:
                    cycle_time = self.cycle_2(buffer_2[0],buffer_3[0])
                elif len(buffer_1) > 0 and len(buffer_3) > 0:
                    ctcle_time = self.cycle_2(buffer_1[0],buffer_3[0])
                elif len(buffer_1) > 0:
                    cycle_time = self.cycle_1(buffer_1[0])
                elif len(buffer_2) > 0:
                    cycle_time = self.cycle_1(buffer_2[0])
                elif len(buffer_3) > 0:
                    cycle_time = self.cycle_1(buffer_3[0])
                
                #testing output (if enabled)
                if PRINT_OUTPUT:
                    print("Buffer lengths: ")
                    print("Buffer 1: " + str(len(buffer_1)))
                    print("Buffer 2: " + str(len(buffer_2)))
                    print("Buffer 3: " + str(len(buffer_3)))
                    print("Total time required to process the link packets in cycler: " + str(cycle_time))
                    print("---Total elapsed time: " + str(curr_time) + "---")
                    print("\n")
                if len(buffer_1) > 0:
                    buffer_1.pop(0)
                if len(buffer_2) > 0:
                    buffer_2.pop(0)
                if len(buffer_3) > 0:
                    buffer_3.pop(0)

                doing_work = True
            else: 
                cycle_time -= 1
            if cycle_time == 0:
                doing_work = False
            
            curr_time += 1        

#RUN TESTS HERE

#set the data
packets = initialize_packet_array(PACKET_ARRAY_SIZE)

#FIFO algorithm test
fifoAlg = FIFO(packets, 1)
fifoAlg.scheduler()

#Priority Queue algorithm test
prioAlg = PriorityQueue(packets, 1)
prioAlg.scheduler();

#Round Robin algorithm test
round_robin_alg = RoundRobin(packets, 1)
round_robin_alg.scheduler()
