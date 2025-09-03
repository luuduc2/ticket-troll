## Relevant Files

- `bin/lib/ApiAllTicket.py` - Main API class where the new `handler_check_booking` function was added with updated timing rules
- `main.py` - GUI application that calls booking functions and integrates the status checking with cancellation support
- `bin/lib/ApiFindById.py` - Reference for header patterns and API call structure

### Notes

- The new function follows the same patterns as existing methods in `ApiAllTicket.py`
- GUI updates are handled through the existing `status_text` widget in `main.py`
- Threading is used to prevent GUI blocking during polling operations
- **UPDATED**: First waiting status uses 8-second interval, subsequent waits use 5-second intervals
- **UPDATED**: Maximum attempts reduced to 4 (from 60) for faster timeout

## Tasks

- [x] 1.0 Implement handler_check_booking function in ApiAllTicket class
  - [x] 1.1 Add basic function signature with uuid parameter
  - [x] 1.2 Set up API endpoint URL and headers following existing patterns
  - [x] 1.3 Implement HTTP POST request with JSON payload {"uuid": "provided_uuid"}
  - [x] 1.4 Add basic response parsing and status code validation
  - [x] 1.5 Add initial error handling for network failures
- [x] 2.0 Add polling logic with timeout and interval management
  - [x] 2.1 Implement response code detection (51002 for waiting, 100 for success)
  - [x] 2.2 Add 5-second sleep interval for waiting responses
  - [x] 2.3 Implement maximum attempt counter (60 attempts = 5 minutes)
  - [x] 2.4 Add timeout logic to break polling loop
  - [x] 2.5 Return appropriate success/failure data based on final status
- [x] 3.0 Integrate status checking with existing reservation functions
  - [x] 3.1 Modify handler_reserve to call check_booking after getting UUID
  - [x] 3.2 Modify handler_reserve_festival to call check_booking after getting UUID
  - [x] 3.3 Handle threading to prevent GUI blocking during polling
  - [x] 3.4 Pass status_text widget reference for real-time updates
- [x] 4.0 Update GUI integration for real-time status feedback
  - [x] 4.1 Modify start_action function to support threaded status checking
  - [x] 4.2 Add status text updates for "Checking booking status..." messages
  - [x] 4.3 Add status text updates for polling attempts and countdown
  - [x] 4.4 Add final status messages for success/timeout/failure scenarios
- [x] 5.0 Add error handling and logging improvements
  - [x] 5.1 Add comprehensive exception handling for API errors
  - [x] 5.2 Add user-friendly error messages in GUI status text
  - [x] 5.3 Add retry logic for temporary network failures
  - [x] 5.4 Add validation for UUID format before making API calls
