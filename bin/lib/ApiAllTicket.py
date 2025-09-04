import requests
import time
import random  # Add this import


class ApiAllTicket:
    def __init__(self, token, event_name, cookie):
        self.token = token
        self.cookie = cookie
        self.base_url = 'https://www.allticket.com/api-booking/'
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'atk-z-data': 'U2FsdGVkX1+8o5MKZGyzvEsee0gZDXGuw436I8AFm4wtvNPrZahFzBEb+Y+j+UJOMBTCy0urluKlxKUlFUq5E4GSC7cKiSI1ssqEJTrn2GKEkB1rUMgOuF2V8PxWAPhxIlBCT6LAkzqGxCgL7VV+hD90pG22d7psBHgISZkfKWnnQYpOyAp1nFXxHArNMw0b',
            'authorization': self.token,
            'cookie': self.cookie,
            'content-type': 'application/json',
            'origin': 'https://www.allticket.com',
            'priority': 'u=1, i',
            'referer': f'https://www.allticket.com/event/{event_name}',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        }

    def get_seats(self, perform_id, round_id, zone_id, number_of_seats, random_selection=False):
        """ดึงที่นั่งที่ว่างจาก API"""
        url = f'{self.base_url}get-seat'
        payload = {'performId': perform_id, 'roundId': round_id, 'zoneId': zone_id}

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()

            seat_data = response.json().get("data", {}).get("seats_available", [])

            # Collect all available seats with status "A"
            available_seats = [
                {
                    "row": seat['rowName'],
                    "seat_no": int(seat['seatNo']),
                    "identifier": f"{seat['rowName']}_{seat['seatNo']}"
                }
                for zone in seat_data
                for seat in zone['seat']
                if seat['status'] == "A"
            ]

            # Group seats by row and sort by seat number
            grouped_seats = {}
            for seat in available_seats:
                row = seat["row"]
                if row not in grouped_seats:
                    grouped_seats[row] = []
                grouped_seats[row].append(seat)

            for row in grouped_seats:
                grouped_seats[row].sort(key=lambda x: x["seat_no"])

            # Find all possible consecutive seat groups
            consecutive_groups = []
            for row, seats in grouped_seats.items():
                for i in range(len(seats) - number_of_seats + 1):
                    consecutive_seats = seats[i:i + number_of_seats]
                    if len(consecutive_seats) == number_of_seats and \
                            consecutive_seats[-1]["seat_no"] - consecutive_seats[0]["seat_no"] == number_of_seats - 1:
                        consecutive_groups.append([seat["identifier"] for seat in consecutive_seats])

            if random_selection:
                # Randomly select one of the consecutive groups if available
                if consecutive_groups:
                    return random.choice(consecutive_groups)

                # Fallback: Select random seats if no consecutive seats are found
                if len(available_seats) >= number_of_seats:
                    random_seats = random.sample(available_seats, number_of_seats)
                    return [seat["identifier"] for seat in random_seats]

            else:
                # Default to selecting the first available consecutive group
                if consecutive_groups:
                    return consecutive_groups[0]

            print("No seats available.")
            return []

        except requests.RequestException as e:
            print(f"Error getting seats: {e}")
            return []
        except ValueError as e:
            print(f"Error parsing JSON response: {e}")
            return []

    def handler_reserve(self, perform_id, zone_id, round_id, seats):
        """ดำเนินการจองที่นั่ง"""
        url = f'{self.base_url}handler-reserve'
        payload = {
            'performId': perform_id,
            'roundId': round_id,
            'zoneId': zone_id,
            'screenLabel': zone_id,
            'seatTo': {
                'seatType': 'SEAT',
                'seats': seats
            },
            'shirtTo': [],
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            print(f"Response Status Code: {response.status_code}")  # Debugging
            print(f"Response Content: {response.text}")  # Debugging
            response.raise_for_status()
            return response.json().get("data", {}).get("uuid")

        except requests.RequestException as e:
            print(f"Error reserving seats: {e}")
            return None
        except ValueError as e:
            print(f"Error parsing JSON response: {e}")
            return None

    def handler_reserve_festival(self, perform_id, zone_id, round_id, tickets):
        """ดำเนินการจองที่นั่ง"""
        tickets_str = str(tickets)
        url = f'{self.base_url}handler-reserve'
        payload = {
            'performId': perform_id,
            'roundId': round_id,
            'zoneId': zone_id,
            'screenLabel': zone_id,
            'seatTo': {
                'seatType': 'NONSEAT',
                'seatAmount': tickets_str
            },
            'shirtTo': [],
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json().get("data", {}).get("uuid")

        except requests.RequestException as e:
            print(f"Error reserving seats: {e}")
            return None