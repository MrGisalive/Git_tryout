import requests
API_KEY = "7d97772fd62af034b1f860765b089dcf"
city = "Budapest"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

response = requests.get(url)
print(response)
print(response.json())