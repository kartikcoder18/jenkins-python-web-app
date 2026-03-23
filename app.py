from flask import Flask, request
from prometheus_client import start_http_server, Counter, Histogram, Gauge
import time

app = Flask(__name__)

# METRICS
request_count = Counter('app_requests_total', 'Total number of requests')
request_latency = Histogram('app_request_latency_seconds', 'Request latency')
active_users = Gauge('active_users', 'Active users')

# Start Prometheus metrics server
start_http_server(8000)

current_users = 0

@app.before_request
def before():
    global current_users
    request.start_time = time.time()
    current_users += 1
    active_users.set(current_users)

@app.after_request
def after(response):
    global current_users

    # Count requests
    request_count.inc()

    # Measure latency
    latency = time.time() - request.start_time
    request_latency.observe(latency)

    # Decrease active users
    current_users -= 1
    active_users.set(current_users)

    return response

@app.route('/')
def home():
    return "Metrics Working"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
