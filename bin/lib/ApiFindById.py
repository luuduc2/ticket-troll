import requests
import time

class ApiFindById():
    def __init__(self, token, name):
        # Clean token to ensure it's a proper string without newlines and decode if needed
        if isinstance(token, bytes):
            self.token = token.decode('utf-8').strip()
        else:
            self.token = str(token).strip() if token else ""
        
        # Remove any BOM or special characters
        self.token = self.token.replace('\ufeff', '').replace('\n', '').replace('\r', '')
        
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': self.token,  # replace with actual token
            'priority': 'u=1, i',
            'referer': f'https://www.allticket.com/event/{name}',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        }

    def get_event_id(self, name):

        # Get the current timestamp in milliseconds
        current_time_ms = int(time.time() * 1000)
        params = {
            'time': current_time_ms,
        }

        # Send the GET request
        url = f'https://www.allticket.com/master/event_info/{name}.json'
        response = requests.get(url, params=params, headers=self.headers)

        # Check if the response is successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            event_id = data.get("data", {}).get("event_id")

            # Print the event_id
            if event_id:
                return event_id
            else:
                print("Event ID not found in the response.")
                return None
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            return None