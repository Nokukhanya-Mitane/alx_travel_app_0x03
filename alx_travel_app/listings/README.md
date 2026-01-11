## Chapa Payment Integration

This project integrates the Chapa payment gateway to enable secure booking payments.

### Payment Workflow
1. User creates a booking.
2. Payment is initiated via Chapa API.
3. Transaction is stored with status `Pending`.
4. Payment is verified after completion.
5. Status is updated to `Completed` or `Failed`.

### Environment Variables
- `CHAPA_SECRET_KEY`: Secret API key from Chapa

### Testing
Chapa sandbox environment was used to test payment initiation and verification.
