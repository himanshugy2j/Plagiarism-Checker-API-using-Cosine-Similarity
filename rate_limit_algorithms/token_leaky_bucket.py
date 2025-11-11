# rate_limit_algorithms/token_leaky_bucket.py

import time
import threading

# ----------------------------
# Token Bucket Algorithm
# ----------------------------
class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity          # Max tokens
        self.tokens = capacity            # Current tokens
        self.refill_rate = refill_rate    # Tokens per second
        self.lock = threading.Lock()
        self.last_refill = time.time()

    def allow_request(self):
        with self.lock:
            now = time.time()
            # Refill tokens
            elapsed = now - self.last_refill
            refill = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + refill)
            self.last_refill = now

            if self.tokens >= 1:
                self.tokens -= 1
                return True
            else:
                return False

# ----------------------------
# Leaky Bucket Algorithm
# ----------------------------
class LeakyBucket:
    def __init__(self, capacity, leak_rate):
        self.capacity = capacity
        self.leak_rate = leak_rate      # Requests per second
        self.water = 0                  # Current requests in bucket
        self.lock = threading.Lock()
        self.last_check = time.time()

    def allow_request(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_check
            leaked = elapsed * self.leak_rate
            self.water = max(0, self.water - leaked)
            self.last_check = now

            if self.water < self.capacity:
                self.water += 1
                return True
            else:
                return False

# ----------------------------
# Example usage
# ----------------------------
if __name__ == "__main__":
    print("=== Token Bucket Example ===")
    tb = TokenBucket(capacity=5, refill_rate=1)  # 5 requests max, 1 token/sec refill
    for i in range(10):
        allowed = tb.allow_request()
        print(f"Request {i+1}: {'Allowed' if allowed else 'Rejected'}")
        time.sleep(0.5)

    print("\n=== Leaky Bucket Example ===")
    lb = LeakyBucket(capacity=5, leak_rate=1)   # 5 requests max, leaks 1 request/sec
    for i in range(10):
        allowed = lb.allow_request()
        print(f"Request {i+1}: {'Allowed' if allowed else 'Rejected'}")
        time.sleep(0.5)
