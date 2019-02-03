PROMPT = """
Input a health check report with format below:
{"service_id": "myservice","status": {"healthy": true,"message": "Everything is OK"},"events": {"ok": 23,"error": 2}}
Or Input 'quit' to exit.
"""

EVENT_ROLLING_INTERVAL = 1000
MAX_ALLOWED_ERROR_RATE = 0.10
