# PTR---Polarized-User-and-Topic-Tracking
Polarized-User-and-Topic-Tracking Algorithm

Digital traces of conversations in micro-blogging platforms and in OSNs provide information about user opinion with a high degree of resolution. These information sources can be exploited to understand and monitor collective behaviors. In this work, we focus on polarization classes, i.e., those topics that require the user to side exclusively with one position. The proposed method provides an iterative classification of users and keywords: first, polarized users are identified, then polarized keywords are discovered by monitoring the activities of previously classified users. This method thus allows to track users and topics over time.

The algorithm is written in Python. Data are stored in MongoDB.
Install it before running the code (MongoDB and Pymongo).
The algorithm uses the following default libraries:
  + sys
  + operator
  + dateutils
  + ast
  + numpy
  + time and datetime
  
  
Run the file alg.py through the shell: 

```
pyhton alg.py arg1 arg2 arg3 arg4 arg5 arg6 arg7 

```

arg1= name of DB (database in MongoDB where to store data)

arg2= name of Colleciton in MongoDB to be used (or a new name to create one)

arg3= input file with Twitter data in json structure as it is from APIs (example in file 'data' attached to the project)

arg4= boolean (1 or 0) to indicate which version of the algorithm to be used: 1 = Time PTR, 0 = PTR

arg5= number or iterations of the algorithm (PTR) or number of days in the windows at each step (TPTR)

arg6= file with the initial seed for polarizing procedure (example in file 'class.txt' attached to the project). Text file with a list of hashtags separated by " " (space). One line per class of polarization and at least one hashtag per line. 

arg7= param which indicates the threashold in hashtag extraction procedure (default= 0.02)



## Contact

Mauro Coletto, CNR Pisa - IMT Lucca

mauro.coletto@isti.cnr.it

mauro.coletto@imtlucca.it

