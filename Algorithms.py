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
import matplotlib.pyplot as plt

#constants
PACKET_ARRAY_SIZE = 10000 #amount of packets to test
PACKET_MAX_SIZE = 30 #maximum size of individual packet
PACKET_MAX_PRIO = 10 #maximum priority of individual packet
PRINT_OUTPUT = False #boolean which allows you to enable or disable console printing of algorithm output data
GRAPHING = True #boolean which allows you to enable or disable the display of graphs
DELAY = 20 #amount of time between packets arriving

#enum for priority queue scheduler
RANDOM_PRIO = 0
SMALL_PRIO = 1
LARGE_PRIO = 2

random.seed(10)

#Packet data object class
class Packet:
    def __init__(self, header_id, size, prio, header_class):
        self.header_id = header_id
        self.size = size #time it takes to process a packet
        self.prio = prio #priority class given to the packet
        self.header_class = header_class #header classification to sort the packet in a Round Robin alg
        self.process_time = 0 #used to keep track of how long it took to be processed in the scheduling algorithms
    
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

#classless functions to build an array of integers from the array of Packet objects for graphing    
def get_packet_time_array(packet_array):
    packet_times = []
    for packet in packet_array:
        packet_times.append(packet.process_time)
    return packet_times    
def get_packet_size_array(packet_array):
    packet_sizes = []
    for packet in packet_array:
        packet_sizes.append(packet.size)
    return packet_sizes
def get_packet_prio_array(packet_array):
    packet_prios = []
    for packet in packet_array:
        packet_prios.append(packet.prio)
    return packet_prios
def get_packet_header_array(packet_array):
    packet_headers = []
    for packet in packet_array:
        packet_headers.append(packet.header_class)
    return packet_headers

#FIFO class which implements the First In First Out algorithm
class FIFO:
    def __init__(self, packets, delay):
        self.packets = packets
        self.delay = delay

    #FIFO scheduling algorithm
    def scheduler(self):
        if PRINT_OUTPUT:
            print("=-=-=-= FIFO =-=-=-=\n")
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
            prev_completion_time = completion_time
            count += 1

            #testing output (if enabled)
            if PRINT_OUTPUT:
                print('---[Packet ' + str(count) + ' Size:' + str(packet.size) + ']---')
                print('Arrival Time: ' + str(arrival_time))
                print('Wait Time: ' + str(wait_time))
                print('Completion Time: ' + str(completion_time))
                print('Packet Total Processing Time: ' + str(completion_time-arrival_time) + '\n')
            
            #create packet and add it to the array with all relevant info
            processed_packet = Packet(packet.header_id, packet.size, packet.prio, packet.header_class)
            processed_packet.process_time = completion_time - arrival_time
            packet_wait_time.append(processed_packet)
        print("FIFO COMPLETION TIME = "+str(prev_completion_time))
        return packet_wait_time

class PriorityQueue:
    def __init__(self, packets, delay):
        self.packets = packets
        self.delay = delay
    
    #PriotiyQueue scheduling algorithm
    def scheduler(self, enum):
        if PRINT_OUTPUT:
            if enum == RANDOM_PRIO: pass
            print("=-=-=-= PRIO RANDOM =-=-=-=\n")
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
                packet_ID = packet_buffer[0].header_id
                packet_size = packet_buffer[0].size
                packet_prio = packet_buffer[0].prio
                packet_header_class = packet_buffer[0].header_class
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
                
                #create packet and add it to the array with all relevant info
                processed_packet = Packet(packet_ID, packet_size, packet_prio, packet_header_class)
                processed_packet.process_time = curr_time - packet_arrival_time
                packet_wait_time.append(processed_packet)

            #if its not currently processing a packet and there are packets in the buffer, start processing the next packet
            if not doing_work and len(packet_buffer) > 0:
                start_time = curr_time
                processing_time = packet_buffer[0].size
                doing_work = True
            curr_time += 1
        print("PRIO (random) COMPLETION TIME = "+str(curr_time))
        return packet_wait_time
        
    def scheduler_smaller_first(self):
        if PRINT_OUTPUT:
            print("=-=-=-= PRIO SMALLER FIRST =-=-=-=\n")
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
                    packet_buffer[1:end_of_buffer] = sorted(packet_buffer[1:end_of_buffer],key=lambda x: x.size)
                packet_ID = packets[packet_count].header_id
                packet_size = packets[packet_count].size
                packet_prio = packets[packet_count].prio
                packet_count += 1
                
            #check if the packet that was being worked on is done
            if doing_work and curr_time - start_time == processing_time:
                doing_work = False               
                packet_ID = packet_buffer[0].header_id
                packet_size = packet_buffer[0].size
                packet_prio = packet_buffer[0].size
                packet_header_class = packet_buffer[0].header_class
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
                
                #create packet and add it to the array with all relevant info
                processed_packet = Packet(packet_ID, packet_size, packet_prio, packet_header_class)
                processed_packet.process_time = curr_time - packet_arrival_time
                packet_wait_time.append(processed_packet)

            #if its not currently processing a packet and there are packets in the buffer, start processing the next packet
            if not doing_work and len(packet_buffer) > 0:
                start_time = curr_time
                processing_time = packet_buffer[0].size
                doing_work = True
            curr_time += 1
        print("PRIO (small first) COMPLETION TIME = "+str(curr_time))
        return packet_wait_time
        
    def scheduler_larger_first(self):
        if PRINT_OUTPUT:
            print("=-=-=-= PRIO LARGER FIRST =-=-=-=\n")
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
                    packet_buffer[1:end_of_buffer] = sorted(packet_buffer[1:end_of_buffer],key=lambda x: x.size, reverse=True)
                packet_ID = packets[packet_count].header_id
                packet_size = packets[packet_count].size
                packet_prio = packets[packet_count].prio
                packet_count += 1
                
            #check if the packet that was being worked on is done
            if doing_work and curr_time - start_time == processing_time:
                doing_work = False               
                packet_ID = packet_buffer[0].header_id
                packet_size = packet_buffer[0].size
                packet_prio = packet_buffer[0].size
                packet_header_class = packet_buffer[0].header_class
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
                
                #create packet and add it to the array with all relevant info
                processed_packet = Packet(packet_ID, packet_size, packet_prio, packet_header_class)
                processed_packet.process_time = curr_time - packet_arrival_time
                packet_wait_time.append(processed_packet)

            #if its not currently processing a packet and there are packets in the buffer, start processing the next packet
            if not doing_work and len(packet_buffer) > 0:
                start_time = curr_time
                processing_time = packet_buffer[0].size
                doing_work = True
            curr_time += 1      
        print("PRIO (large first) COMPLETION TIME = "+str(curr_time))
        return packet_wait_time
          
#constructor class fifo (array of packets, delay)
class RoundRobin:
    def __init__(self, packets, delay):
        self.packets = packets
        self.delay = delay

    #Link to cycle when all 3 buffers send a packet
    def cycle_3(self, packet_1,packet_2,packet_3,packet_time,current_time):
        quantum = 3
        notDone = 1
        cycles = 0
        elapsed_time_1 = 0
        elapsed_time_2 = 0
        elapsed_time_3 = 0
        size_1 = packet_1.size
        size_2 = packet_2.size
        size_3 = packet_3.size

        while size_1 > 0 or size_2 > 0 or size_3 > 0:
            if size_1 > 0:
                if size_1 <= quantum:
                    elapsed_time_1 += size_1
                    size_1 -= size_1
                    packet_1.process_time = (current_time + elapsed_time_1) - packet_1.process_time
                    packet_time.append(packet_1)
                else:
                    size_1 -= quantum
                    elapsed_time_1 += quantum
            if size_2 > 0:
                if size_2 <= quantum:
                    elapsed_time_2 += size_2
                    size_2 -= size_2
                    packet_2.process_time = (current_time + elapsed_time_2) - packet_2.process_time
                    packet_time.append(packet_2)
                else:
                    size_2 -= quantum
                    elapsed_time_2 += quantum
            if size_3 > 0:
                if size_3 <= quantum:
                    elapsed_time_3 += size_3
                    size_3 -= size_3
                    packet_3.process_time = (current_time + elapsed_time_3) - packet_3.process_time
                    packet_time.append(packet_3)
                else:
                    size_3 -= quantum
                    elapsed_time_3 += quantum
            cycles += 1
        elapsed_time = [elapsed_time_1,elapsed_time_2,elapsed_time_3]
        return elapsed_time

    #Link to cycle when 2 of the 3 buffers send a packet
    def cycle_2(self, packet_1,packet_2,packet_time,current_time):
        quantum = 3
        notDone = 1
        cycles = 0
        elapsed_time_1 = 0
        elapsed_time_2 = 0
        size_1 = packet_1.size
        size_2 = packet_2.size

        while size_1 > 0 or size_2 > 0:
            if size_1 > 0:
                if size_1 <= quantum:
                    elapsed_time_1 += size_1
                    size_1 -= size_1
                    packet_1.process_time = (current_time + elapsed_time_1) - packet_1.process_time
                    packet_time.append(packet_1)
                else:
                    size_1 -= quantum
                    elapsed_time_1 += quantum
            if size_2 > 0:
                if size_2 <= quantum:
                    elapsed_time_2 += size_2
                    size_2 -= size_2
                    packet_2.process_time = (current_time + elapsed_time_2) - packet_2.process_time
                    packet_time.append(packet_2)
                else:
                    size_2 -= quantum
                    elapsed_time_2 += quantum
            cycles += 1
        elapsed_time = [elapsed_time_1,elapsed_time_2]
        return elapsed_time

    #Link to cycle a single packet
    def cycle_1(self, packet_1,packet_time,current_time):
        quantum = 3
        notDone = 1
        cycles = 0
        elapsed_time_1 = 0
        size_1 = packet_1.size

        while size_1 > 0:
            if size_1 > 0:
                if size_1 <= quantum:
                    elapsed_time_1 += size_1
                    size_1 -= size_1
                    packet_1.process_time = (current_time + elapsed_time_1) - packet_1.process_time
                    packet_time.append(packet_1)
                else:
                    size_1 -= quantum
                    elapsed_time_1 += quantum
            cycles += 1
        elapsed_time = [elapsed_time_1]
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
        packet_wait_time = []
        
        #run the algorithm until all incoming packets have been dealt with
        while len(buffer_1) > 0 or len(buffer_2) > 0 or len(buffer_3) > 0 or remaining_packets > 0:
            if curr_time == packet_count * self.delay and packet_count < len(self.packets):
                #distribute packets into buffers for processing
                if self.packets[packet_count].header_class == 1:
                    self.packets[packet_count].process_time += curr_time
                    buffer_1.append(self.packets[packet_count])
                elif self.packets[packet_count].header_class == 2:
                    self.packets[packet_count].process_time += curr_time
                    buffer_2.append(self.packets[packet_count])
                else:
                    self.packets[packet_count].process_time += curr_time
                    buffer_3.append(self.packets[packet_count])
                
                packet_count += 1
                remaining_packets -= 1
            #if cycler is not running, queue up a new cycle
            if not doing_work:
                if len(buffer_1) > 0 and len(buffer_2) > 0 and len(buffer_3) > 0:
                    cycle_time = sum(self.cycle_3(buffer_1[0],buffer_2[0],buffer_3[0],packet_wait_time,curr_time))
                elif len(buffer_1) > 0 and len(buffer_2) > 0:
                    cycle_time = sum(self.cycle_2(buffer_1[0],buffer_2[0],packet_wait_time,curr_time))
                elif len(buffer_2) > 0 and len(buffer_3) > 0:
                    cycle_time = sum(self.cycle_2(buffer_2[0],buffer_3[0],packet_wait_time,curr_time))
                elif len(buffer_1) > 0 and len(buffer_3) > 0:
                    cycle_time = sum(self.cycle_2(buffer_1[0],buffer_3[0],packet_wait_time,curr_time))
                elif len(buffer_1) > 0:
                    cycle_time = sum(self.cycle_1(buffer_1[0],packet_wait_time,curr_time))
                elif len(buffer_2) > 0:
                    cycle_time = sum(self.cycle_1(buffer_2[0],packet_wait_time,curr_time))
                elif len(buffer_3) > 0:
                    cycle_time = sum(self.cycle_1(buffer_3[0],packet_wait_time,curr_time))
                
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
        print("ROUND ROBIN COMPLETION TIME = "+str(curr_time))
        return packet_wait_time

#RUN TESTS HERE

#set the data
packets = initialize_packet_array(PACKET_ARRAY_SIZE)

#FIFO algorithm test
fifoAlg = FIFO(packets, DELAY)
fifo_packets = fifoAlg.scheduler()

#Priority Queue algorithm test
prioAlg = PriorityQueue(packets, DELAY)
prio_packets = prioAlg.scheduler(RANDOM_PRIO);
prio_small = prioAlg.scheduler_smaller_first()
prio_large = prioAlg.scheduler_larger_first()

#Round Robin algorithm test
round_robin_alg = RoundRobin(packets, DELAY)
rr_packets = round_robin_alg.scheduler()


#Graphing
if GRAPHING:
    #Initial Packet Array
    '''
    initial_sizes = get_packet_size_array(packets)
    plt.title("Initial Packet Array")
    plt.plot(initial_sizes, label="sizes")
    plt.xlabel("Packet")
    plt.ylabel("Size")
    plt.show()
    '''
    
    #FIFO
    fifo_times = get_packet_time_array(fifo_packets)
    print("total time (FIFO) = "+str(sum(fifo_times)))
    average_fifo = sum(fifo_times)/len(fifo_times)
    plt.plot(fifo_times, label="FIFO")
    plt.title("FIFO processing time, average: "+str(average_fifo))
    plt.xlabel("Packet")
    plt.ylabel("Processing Time")
    plt.show()
    
    #Priority Queue
    prio_times = get_packet_time_array(prio_packets)
    print("total time (prio random) = "+str(sum(prio_times)))
    prio_small_times = get_packet_time_array(prio_small)
    print("total time (prio small) = "+str(sum(prio_small_times)))
    prio_large_times = get_packet_time_array(prio_large)
    print("total time (prio large) = "+str(sum(prio_large_times)))
    average_prio = sum(prio_times)/len(prio_times)
    average_small = sum(prio_small_times)/len(prio_small_times)
    average_large = sum(prio_large_times)/len(prio_large_times)
    plt.plot(prio_times, label="PRIO (random priority) : "+str(average_prio))
    plt.plot(prio_small_times, label="PRIO (smaller first) : "+str(average_small))
    plt.plot(prio_large_times, label="PRIO (larger first) : "+str(average_large))
    plt.title("Priority queue processing time")
    plt.xlabel("Packet")
    plt.ylabel("Processing Time")
    plt.legend()
    plt.show()
    
    #Round Robin
    rr_time = get_packet_time_array(rr_packets)
    print("total time (RR) = "+str(sum(rr_time)))
    average_rr = sum(rr_time)/len(rr_time)
    plt.plot(rr_time, label = "ROUND ROBIN : "+str(average_rr))
    plt.title("Round Robin processing time")
    plt.xlabel("Packet")
    plt.ylabel("Processing Time")
    plt.legend()
    plt.show()
