import multiprocessing
import os

bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
workers = int(os.getenv("WORKERS", str(multiprocessing.cpu_count() * 2 + 1)))
worker_class = "uvicorn.workers.UvicornWorker"
worker_tmp_dir = "/dev/shm"

loglevel = os.getenv("LOG_LEVEL", "info").lower()
accesslog = "-"
errorlog = "-"

graceful_timeout = 30
timeout = 60
keepalive = 5

max_requests = 1000
max_requests_jitter = 50
