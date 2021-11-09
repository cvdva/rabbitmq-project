#!/bin/bash

#Starts all handler queues for listening

export PYTHONPATH="/Users/cassie/Documents/School Stuff/CNU/Thesis Monster/PyCharm Projects/RabbitMQ/"
echo Starting Queues...
echo

echo Starting register queue...
python3 register_queue.py &
echo

echo Starting hello queue...
python3 init_queue.py &
echo

echo Starting  announce queue...
python3 announce_queue.py &
echo

echo Starting request queue...
python3 request_queue.py &
echo

echo Starting need data queue...
python3 need_data_queue.py &
echo

echo Starting final queue...
python3 final_queue.py &
echo

echo All queues started
