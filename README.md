# alx_travel_app_0x03
alx_travel_app_0x02
Chapa Payment Integration
This project integrates the Chapa payment gateway to enable secure booking payments.

Payment Workflow
User creates a booking.
Payment is initiated via Chapa API.
Transaction is stored with status Pending.
Payment is verified after completion.
Status is updated to Completed or Failed.
Environment Variables
CHAPA_SECRET_KEY: Secret API key from Chapa
Testing
Chapa sandbox environment was used to test payment initiation and verification.
