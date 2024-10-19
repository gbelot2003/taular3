import multiprocessing

bind = "0.0.0.0:5000"
workers = 2
worker_class = "gevent"
timeout = 120
keepalive = 2