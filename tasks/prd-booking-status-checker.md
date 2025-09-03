# Product Requirements Document: Booking Status Checker

## Introduction/Overview

This feature adds a booking status verification system to the ticket booking bot. After a reservation is made using `handler_reserve`, the system needs to continuously check the booking status until it's confirmed as complete. The AllTicket API requires polling to verify that a reservation has been successfully processed, as the initial reservation only returns a UUID but doesn't guarantee completion.

**Problem**: Currently, when users make a reservation, they receive a UUID but don't know if the booking was actually completed successfully. The reservation might still be processing, and users have no visibility into the final status.

**Goal**: Implement an automated polling system that checks booking status after reservation and provides real-time feedback to users about their booking completion.

## Goals

1. **Automated Status Verification**: Automatically check booking status after `handler_reserve` completes
2. **Real-time Feedback**: Provide continuous status updates to users via GUI
3. **Reliable Completion Detection**: Accurately determine when booking is fully processed
4. **Timeout Protection**: Prevent infinite polling with reasonable timeout limits
5. **Error Handling**: Gracefully handle API errors and network issues

## User Stories

1. **As a user making a ticket reservation**, I want to know when my booking is fully confirmed so that I can be confident my tickets are secured.

2. **As a user with a pending reservation**, I want to see real-time status updates so that I know the system is working on my booking.

3. **As a user experiencing booking delays**, I want the system to automatically retry checking my status so that I don't have to manually refresh.

4. **As a user with a failed booking**, I want to be notified immediately so that I can take alternative action.

## Functional Requirements

1. **R1**: The system must implement a `handler_check_booking(uuid)` function in the `ApiAllTicket` class
2. **R2**: The function must accept a UUID parameter returned from `handler_reserve` functions
3. **R3**: The function must make HTTP POST requests to `https://www.allticket.com/api-verify/check-booking`
4. **R4**: The function must use the same authentication headers as other API calls
5. **R5**: The function must send JSON payload with format `{"uuid": "provided_uuid"}`
6. **R6**: The function must parse response and detect "waiting" status (code "51002")
7. **R7**: The function must implement 5-second interval polling for "waiting" responses
8. **R8**: The function must detect successful completion (code "100") and return success data
9. **R9**: The function must implement timeout protection (maximum 5 minutes of polling)
10. **R10**: The function must update GUI status text with current checking status
11. **R11**: The function must handle network errors and API failures gracefully
12. **R12**: The function must be automatically called after successful `handler_reserve` operations
13. **R13**: The function must log all status updates to the GUI status text area
14. **R14**: The function must return booking confirmation data when successful
15. **R15**: The function must stop polling on timeout and notify user
16. **R16**: The function must maintain consistent error handling patterns with existing code
17. **R17**: The function must support both seated and festival (non-seated) booking types

## Non-Goals (Out of Scope)

1. **Manual Check Button**: No separate GUI button for manual status checking (automatic only)
2. **Booking Modification**: No ability to modify or cancel bookings through this function
3. **Multiple Booking Tracking**: No simultaneous tracking of multiple reservations
4. **Persistent Storage**: No saving of booking status to files or database
5. **Email Notifications**: No email alerts for booking completion
6. **Payment Processing**: No handling of payment-related status checks
7. **Booking History**: No tracking or display of historical booking attempts

## Technical Considerations

1. **Integration Point**: Function will be called immediately after `handler_reserve` and `handler_reserve_festival` return UUIDs
2. **Threading**: Should run in background thread to avoid blocking GUI
3. **API Compatibility**: Must use existing authentication and header patterns from `ApiAllTicket` class
4. **Error Consistency**: Follow same error handling patterns as `get_seats()` and other methods
5. **Timeout Strategy**: Use 5-minute total timeout with 5-second intervals (60 maximum attempts)
6. **GUI Updates**: Update status text area with polling progress and final results

## Success Metrics

1. **Completion Rate**: 95%+ of successful reservations are properly verified as complete
2. **Response Time**: Average polling time under 30 seconds for typical bookings
3. **Error Handling**: 100% of network/API errors handled without crashing
4. **User Feedback**: Clear status messages displayed for all polling states
5. **Timeout Effectiveness**: No infinite polling scenarios occur

## Implementation Flow

```
handler_reserve() → UUID returned → handler_check_booking(UUID) → {
  While booking not complete AND not timeout:
    - Send check-booking request
    - If "waiting" (51002): wait 5 seconds, retry
    - If "success" (100): return booking data, update GUI
    - If error: handle gracefully, potentially retry
    - If timeout: notify user, stop polling
}
```

## Open Questions

1. Should the polling interval be configurable or fixed at 5 seconds?
2. What specific booking data should be displayed to users on successful completion?
3. Should failed bookings trigger any automatic retry of the original reservation?
4. How should the system handle rate limiting from the AllTicket API?
