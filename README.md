# COMP 4300 Final Project

## Instructions to run
- In a console, navigate to the folder containing "Algorithms.py" and type "python3 Algorithms.py"
- In Algorithms.py are a couple boolean flags for controlling output:
	+ PRINT_OUTPUT: Controls whether or not output is printed to the console when each packet completes being processed
	+ GRAPHING: Controls whether or not graphs are displayed at the end. matplotlib.pyplot must be installed for this to work.
	
## Scheduling Algorithms Implemented
- FIFO (First In First Out): Packets are processed in the order they arrive.
- Priority Queue: Similar to FIFO, however packets in the buffer with a higher priority are processed first.
- Round Robin: A round of up to 3 packets are processed concurrently, each packet taking turns being processed until all are completed.

## The Experiment and Results
- An array of packets is generated with packets of random size and priority class.
- Each individual packet is passed to the schedulers after a short delay.
- The scheduler keeps track of when a packet arrives in the buffer and when the packet completes being processed.
- Once all packets have been processed, the scheduler returns a new array of times in the order of packets that were processed.
	+ For FIFO the order is the same as the initial packet array, but for priority queue and round robin the packets may be processed in a different order.
- Results can be found in the "graph data" folder, sorted by experiment parameters (delay and array size)
	+ Graphs showing the process time of each individual packet.
	+ Run times of each scheduling algorithm.
