import sys
import os
import time
from unittest.mock import MagicMock

# Add root directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock streamlit
mock_st = MagicMock()
sys.modules["streamlit"] = mock_st

# Simple cache implementation for the mock
_cache = {}
def cache_resource_mock(func):
    def wrapper(*args, **kwargs):
        # Create a key based on function and arguments
        # args and kwargs items must be hashable
        key = (func, args, frozenset(kwargs.items()))
        if key not in _cache:
            _cache[key] = func(*args, **kwargs)
        return _cache[key]
    return wrapper

mock_st.cache_resource = cache_resource_mock
mock_st.cache_data = cache_resource_mock

# Now import brain
from brain import get_brain

def simulate_interaction():
    start_time = time.time()

    print("Getting Brain...")
    # This should be fast after the first call due to caching
    brain = get_brain()

    print("Processing prompt...")
    # prompt is not cached in process method, but safety check is cached
    response = brain.process("Hello world")

    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":
    print("Starting optimized load test...")
    durations = []
    # Run a few times
    # 1st run: Init (1s) + Check (0.5s) + Process (1s) = 2.5s
    # 2nd run: Init (cached) + Check (cached) + Process (1s) = 1.0s
    for i in range(3):
        duration = simulate_interaction()
        durations.append(duration)
        print(f"Interaction {i+1}: {duration:.2f}s")

    avg = sum(durations) / len(durations)
    print(f"Average time per interaction: {avg:.2f}s")
