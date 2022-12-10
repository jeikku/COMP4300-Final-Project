#
# COMP 4300 Final Project - By: Jacob Broggy & Sebastien Pichon
# File containing all the algorithms
#

class Packet:
    def __init__(self, header_id, size, prio, header_class):
        self.header_id = header_id
        self.size = size #time it takes to process a packet
        self.prio = prio #priority class given to the packet
        self.header_class = header_class #header classification to sort the packet in a RR
    
    def __cmp__(self, other):
        return cmp(self.prio, other.prio)
        
def sort_packet_buffer(packet_buffer):
    pass

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
        #while there are still packets incoming and the buffer is not empty
        while packet_count < len(self.packets) or len(packet_buffer) > 0: 
            #add in a packet to the buffer when it arrives
            if curr_time == packet_count * self.delay and packet_count < len(self.packets):
                packet_buffer.append(self.packets[packet_count])
                #resort the priority queue, ignoring the first element
                end_of_buffer = len(packet_buffer)
                if end_of_buffer > 1:
                    packet_buffer[1:end_of_buffer] = sorted(packet_buffer[1:end_of_buffer],key=lambda x: x.prio)
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

    def cycle_3(self, packet_1,packet_2,packet_3):
        quantum = 3
        notDone = 1
        cycles = 0
        size_1 = packet_1.size
        size_2 = packet_2.size
        size_3 = packet_3.size
        while size_1 > 0 or size_2 > 0 or size_3 > 0:
            size_1 -= quantum
            size_2 -= quantum
            size_3 -= quantum
            cycles += 1
        return cycles * quantum

    def cycle_2(self, packet_1,packet_2):
        quantum = 3
        notDone = 1
        cycles = 0
        size_1 = packet_1.size
        size_2 = packet_2.size
        while size_1 > 0 or size_2 > 0:
            size_1 -= quantum
            size_2 -= quantum
            cycles += 1
        return cycles * quantum

    def cycle_1(self, packet_1):
        quantum = 3
        notDone = 1
        cycles = 0
        size_1 = packet_1.size
        while size_1 > 0:
            size_1 -= quantum
            cycles += 1
        return cycles * quantum

    def scheduler(self):
        #initialize buffers for cycling
        buffer_1 = []
        buffer_2 = []
        buffer_3 = []
        cycle_time = 0
        #create a cycler which grabs the top packet in all 3 buffers and moves it into a link
        curr_time = 0
        packet_count = 0
        doing_work = False
        remaining_packets = len(self.packets)
        
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

#testing area
p1 = Packet(0,4,3, 1)
p2 = Packet(1,7,2, 1)
p3 = Packet(2,9,1, 2)
p4 = Packet(3,12,5, 3)
p5 = Packet(4,3,2, 1)
packets = [p1, p2, p3, p4, p5]
fifoAlg = FIFO(packets, 1)
fifoAlg.scheduler()

prioAlg = PriorityQueue(packets, 1)
prioAlg.scheduler();

round_robin_alg = RoundRobin(packets, 1)
round_robin_alg.scheduler()