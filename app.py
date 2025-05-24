from flask import Flask, jsonify
import requests
from collections import deque
import time

app = Flask(__name__)
WINDOW_SIZE = 10
window = deque(maxlen=WINDOW_SIZE)

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzQ4MDY2ODU2LCJpYXQiOjE3NDgwNjY1NTYsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6ImIxNmMxNmE5LWJkYzktNGFjMC04NjFiLWVlZTNhMzc0Yjc3NiIsInN1YiI6InByYXNhbnRoNjA0NEBnbWFpbC5jb20ifSwiZW1haWwiOiJwcmFzYW50aDYwNDRAZ21haWwuY29tIiwibmFtZSI6InByYXNhbnRoIGsgciIsInJvbGxObyI6IjkyNzYyMmJhZDA0MiIsImFjY2Vzc0NvZGUiOiJ3aGVRVXkiLCJjbGllbnRJRCI6ImIxNmMxNmE5LWJkYzktNGFjMC04NjFiLWVlZTNhMzc0Yjc3NiIsImNsaWVudFNlY3JldCI6IlNZdmRrZXF2d1luZnJOZGIifQ.SyAADsFApTCkAhzO_ohksvytE77jmqr-TVOtfA_s8DM"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

TYPE_API = {
    "p": "http://20.244.56.144/evaluation-service/primes",
    "f": "http://20.244.56.144/evaluation-service/fibo",
    "e": "http://20.244.56.144/evaluation-service/even",
    "r": "http://20.244.56.144/evaluation-service/rand"
}

@app.route("/numbers/<string:numberid>", methods=["GET"])
def get_numbers(numberid):
    if numberid not in TYPE_API:
        return jsonify({"error": "Invalid number type"}), 400

    api_url = TYPE_API[numberid]
    prev_state = list(window)
    new_numbers = []

    try:
        start = time.time()
        response = requests.get(api_url, headers=HEADERS, timeout=0.5)
        elapsed = time.time() - start

        if response.status_code == 200 and elapsed <= 0.5:
            data = response.json()
            numbers = data.get("numbers", [])
            new_numbers = [n for n in numbers if n not in window]
            for num in new_numbers:
                window.append(num)
    except Exception as e:
        print("Error:", e)

    curr_state = list(window)
    average = round(sum(curr_state) / len(curr_state), 2) if curr_state else 0.0

    return jsonify({
        "windowPrevState": prev_state,
        "windowCurrState": curr_state,
        "numbers": new_numbers,
        "avg": average
    })

if __name__ == "__main__":
    app.run(port=9876)
