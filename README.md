This project was writted for CS442 Distributed Systems and Algorithms at Bilkent University by Abdul Razak Khatib.
In this project I created an NP number of processes and a multiprocessing queue.This queue is what I use to send a broadcast.
Each process checks its queue for any messages then checks the time for broadcasting, if broadcasting time arrives it sends a message to all other processes.
When each process receives a message from its queue it takes the Logical Clock value from the sender if it is larger than the current Logical Clock value, otherwise it ignores it. 
I used a timer at the beginning to be sure all processes start at the same time, and I used global variable for the command line arguments to make them more accessible, once all processes return the program is terminated.
Processes were chosen since the algorithm uses a FIFO container like a queue and queues work better with processes.
