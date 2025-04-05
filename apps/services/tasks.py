
from app import celery
from apps.data.model.user import User
from apps.services.notificationadapter import NotificationAdapter
from apps.services.rollover import RollOverService



@celery.task
def process_rollover():
        roller_service = RollOverService(
            notification_handler = NotificationAdapter.handle_notification
            )
        roller_service.rollover_monthly_budget()

@celery.task
def send_budget_exceeded_notification(email, category, limit, current_spending):
    user = User.objects(email=email).first()
    if user:
        message =(
            f"Your {category} budget of ₦{limit:,.2f} for this month has been exceeded."
            f"Current spending: ₦{current_spending:,.2f}."
        )
        NotificationAdapter.handle_notification(
            user=user,
            title="Budget Limit Exceeded",
            message=message,
            category="budget exceeded"
        )

 # celery -A app.celery worker --loglevel=info --pool=solo