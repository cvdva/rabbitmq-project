# rabbitmq-project
Solving messaging issues one step at a time

### A guide to current files
- init_queue.py listens for messages on the queue named "hello", which will be the first contact when data is created
- send.py sends the data in example_jason.json to the "hello" queue
- new_task.py and receive.py are just there for messing around and trying things
- handler.py is the start of the server handler which will recive messages from worker.py
- sourcelog.csv is a list of source IDs used by the handler. 
- datalog.csv is a list of data IDs so the system doesn't duplicate the same data
- announce.py will send a message of choice to the announce queue
- announce_queue.py listens on the announce queue
- input_new_data.py asks for user input and sends json to the "hello" queue
