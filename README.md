# rabbitmq-project
Solving messaging issues one step at a time

### A guide to current files
- worker.py listens for messages on the queue named "hello"
- send.py sends the data in example_jason.json to the "hello" queue
- new_task.py and receive.py are just there for messing around and trying things
- handler.py is the start of the server handler which will recive messages from worker.py
- sourcelog.csv is a list of source IDs used by the handler. 
