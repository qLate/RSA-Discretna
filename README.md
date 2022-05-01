# RSA-Discretna

We got a script for the terminal chat program. Our main task was to make sending messages safe. For that, we were using the RSA algorithm. 

#####Our laboratory work consisted of 2 tasks:
1. Implementing the RSA algorithm for transmitting keys and encrypting messages.
2. Making a checker that ensures that the user gets a real message. 

###1. RSA algorithm

First, we had to put our message into the integer view. Then we encoded it using the RSA algorithm and transformed that into bytes for sending to another user. That user had to go by those steps vice versa.

###2. Hashing a message

To ensure that the final user got the right message, we used hashing functions sha256. We were sending messages in that form (hash_of_the_message + encrypted message)

If a user got a correct message, he could see (reached successfully) at the end of a message. If he wasn't (brought unsuccessfully), the message was delivered with mistakes. 

#####Here are some examples of the chat:

![example](RSA-Discretna/example.png)