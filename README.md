# alx_travel_app_0x03
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

## Background Tasks with Celery

This project uses Celery with RabbitMQ to handle background tasks.

### How to Run
1. Start RabbitMQ
2. Run migrations:
   python manage.py migrate
3. Start Django server:
   python manage.py runserver
4. Start Celery worker:
   celery -A alx_travel_app worker -l info

Booking confirmation emails are sent asynchronously using Celery.
