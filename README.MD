# BenchMark GO vs Python Flask Rest Api (Insert to Mongo)  

This is a Golang application managing tasks using a MongoDB and Gin as webservice framework.


`docker-compose up --build`  

`locust -f flask_post.py`  
RPS: 74  
Request: 3600  
Median: 7100ms  
Avg: 7304ms
Min: 59ms  
Max: 15690ms  

`locust -f go_post.py`  
RPS: 106  
Request: 2513  
Median: 2200ms  
Avg: 2402
Min: 55ms  
Max: 6896ms  
Fail: 2%
