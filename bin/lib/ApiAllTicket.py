import requests
import time


class ApiAllTicket:
    def __init__(self, token, event_name, cookie):
        # Clean token and cookie to ensure they're proper strings without newlines and decode if needed
        if isinstance(token, bytes):
            self.token = token.decode('utf-8').strip()
        else:
            self.token = str(token).strip() if token else ""
            
        if isinstance(cookie, bytes):
            self.cookie = cookie.decode('utf-8').strip()
        else:
            self.cookie = str(cookie).strip() if cookie else ""
            
        # Remove any BOM or special characters
        self.token = self.token.replace('\ufeff', '').replace('\n', '').replace('\r', '')
        self.cookie = self.cookie.replace('\ufeff', '').replace('\n', '').replace('\r', '')
        
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

    def get_seats(self, perform_id, round_id, zone_id, number_of_seats):
        """ดึงที่นั่งที่ว่างจาก API"""
        url = f'{self.base_url}get-seat'
        payload = {'performId': perform_id, 'roundId': round_id, 'zoneId': zone_id}

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            seat_data = response.json().get("data", {}).get("seats_available", [])

            available_seats = [
                f"{seat['rowName']}_{seat['seatNo']}"
                for zone in seat_data
                for seat in zone['seat']
                if seat['status'] == "A"
            ]
            print(f"available_seats {number_of_seats}",)
            return available_seats[:number_of_seats]

        except requests.RequestException as e:
            print(f"Error getting seats: {e}",)
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
            response.raise_for_status()
            return response.json().get("data", {}).get("uuid")

        except requests.RequestException as e:
            print(f"Error reserving seats: {e}")
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

    def handler_check_booking(self, uuid, status_text=None, cancellation_flag=None):
        """Check booking status until completion or timeout"""
        print(f"[BOOKING_CHECK] Starting booking status check")
        print(f"[BOOKING_CHECK] UUID: {uuid}")
        print(f"[BOOKING_CHECK] Max attempts: 60 (5 minutes)")
        
        if not uuid:
            print(f"[BOOKING_CHECK] ERROR: No UUID provided")
            return None
            
        url = f'{self.base_url.replace("api-booking", "api-verify")}check-booking'
        payload = {'uuid': uuid}
        max_attempts = 60  # 5 minutes with 5-second intervals
        attempt = 0
        
    def handler_check_booking(self, uuid, status_text=None, cancellation_flag=None):
        """Check booking status until completion or timeout"""
        print(f"[BOOKING_CHECK] Starting booking status check")
        print(f"[BOOKING_CHECK] UUID: {uuid}")
        print(f"[BOOKING_CHECK] Max attempts: 4 (5s intervals)")
        
        if not uuid:
            print(f"[BOOKING_CHECK] ERROR: No UUID provided")
            return None
            
        url = f'{self.base_url.replace("api-booking", "api-verify")}check-booking'
        payload = {'uuid': uuid}
        max_attempts = 4  # 4 attempts total
        attempt = 0
        
        print(f"[BOOKING_CHECK] API URL: {url}")
        print(f"[BOOKING_CHECK] Payload: {payload}")
        
        if status_text:
            status_text.insert("end", f"Checking booking status for UUID: {uuid}...\n")
        
        # Print to console for logging
        print(f"Checking booking status for UUID: {uuid}...")
        
        while attempt < max_attempts:
            # Check for cancellation
            if cancellation_flag and hasattr(cancellation_flag, '__call__') and cancellation_flag():
                cancel_msg = "🛑 Booking status check cancelled by user"
                print(f"[BOOKING_CHECK] CANCELLED: {cancel_msg}")
                if status_text:
                    status_text.insert("end", f"{cancel_msg}\n")
                return None
            
            try:
                print(f"[BOOKING_CHECK] Attempt {attempt + 1}/{max_attempts}")
                
                response = requests.post(url, headers=self.headers, json=payload)
                print(f"[BOOKING_CHECK] HTTP Status: {response.status_code}")
                
                response.raise_for_status()
                data = response.json()
                
                print(f"[BOOKING_CHECK] Response: {data}")
                
                if status_text:
                    status_text.insert("end", f"Attempt {attempt + 1}: Checking status...\n")
                
                # Check if booking is complete (success)
                if data.get("success") and data.get("code") == "100":
                    success_msg = "✓ Booking confirmed successfully!"
                    reserve_id = data.get('data', {}).get('reserveId', 'N/A')
                    
                    # Print to console for logging
                    print(f"[BOOKING_CHECK] SUCCESS: {success_msg}")
                    print(f"[BOOKING_CHECK] Reserve ID: {reserve_id}")
                    
                    if status_text:
                        status_text.insert("end", f"{success_msg}\n")
                        status_text.insert("end", f"Reserve ID: {reserve_id}\n")
                    return data
                
                # Check if still waiting
                elif data.get("code") == "51002":
                    wait_time = 5  # Consistent 5-second intervals
                    remaining_attempts = max_attempts - attempt - 1
                    processing_msg = f"Booking still processing... ({remaining_attempts} attempts remaining, wait {wait_time} seconds)"
                    
                    # Print to console for logging
                    print(f"[BOOKING_CHECK] WAITING: {processing_msg}")
                    
                    if status_text:
                        status_text.insert("end", f"{processing_msg}\n")
                    
                    # Only wait if there are more attempts remaining
                    if remaining_attempts > 0:
                        # Wait with cancellation check during wait period
                        print(f"[BOOKING_CHECK] Waiting {wait_time} seconds before next attempt...")
                        for i in range(wait_time):
                            if cancellation_flag and hasattr(cancellation_flag, '__call__') and cancellation_flag():
                                cancel_msg = "🛑 Booking status check cancelled during wait"
                                print(f"[BOOKING_CHECK] CANCELLED: {cancel_msg}")
                                if status_text:
                                    status_text.insert("end", f"{cancel_msg}\n")
                                return None
                            time.sleep(1)
                    
                    attempt += 1
                    continue
                
                # Handle other response codes
                else:
                    error_msg = f"Unexpected response: {data.get('message', 'Unknown error')}"
                    print(f"[BOOKING_CHECK] UNEXPECTED: {error_msg}")
                    print(f"[BOOKING_CHECK] Full response: {data}")
                    
                    if status_text:
                        status_text.insert("end", f"{error_msg}\n")
                    return data
                    
            except requests.RequestException as e:
                error_msg = f"Network error during status check: {e}"
                print(f"[BOOKING_CHECK] NETWORK_ERROR: {error_msg}")
                
                if status_text:
                    status_text.insert("end", f"{error_msg}\n")
                
                # Wait before retry for network errors, but check for cancellation
                print(f"[BOOKING_CHECK] Waiting 5 seconds before retry due to network error...")
                for i in range(5):
                    if cancellation_flag and hasattr(cancellation_flag, '__call__') and cancellation_flag():
                        cancel_msg = "🛑 Booking status check cancelled during network error retry"
                        print(f"[BOOKING_CHECK] CANCELLED: {cancel_msg}")
                        if status_text:
                            status_text.insert("end", f"{cancel_msg}\n")
                        return None
                    time.sleep(1)
                
                attempt += 1
                continue
        
        # Timeout reached
        timeout_msg = f"⚠ Booking status check timed out after 4 attempts."
        manual_check_msg = f"Please check your booking manually with UUID: {uuid}"
        
        # Print to console for logging
        print(f"[BOOKING_CHECK] TIMEOUT: {timeout_msg}")
        print(f"[BOOKING_CHECK] MANUAL_CHECK: {manual_check_msg}")
        print(f"[BOOKING_CHECK] Final attempt count: {attempt}")
        
        if status_text:
            status_text.insert("end", f"{timeout_msg}\n")
            status_text.insert("end", f"{manual_check_msg}\n")
        
        return None