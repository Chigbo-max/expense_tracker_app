import traceback
from datetime import datetime, timedelta

from apps.data.model.budget import Budget


class RollOverService:
    def __init__(self, notification_handler = None):
        self.notification_handler = notification_handler

    def rollover_monthly_budget(self):
        now = datetime.now()
        last_month = now.replace(day=1) - timedelta(days=1)

        for budget in Budget.objects(
                month=last_month.month,
                year=last_month.year,
                rollover_enabled=True
                        ):
            try:
                unused_amount = max(0, budget.limit - budget.current_spending)
                if unused_amount <= 0:
                    continue

                next_month_date = (last_month + timedelta(days=32)).replace(day=1)

                Budget.objects(
                    user=budget.user,
                    category=budget.category,
                    month=next_month_date.month,
                    year=next_month_date.year,
                ).modify(
                    upsert=True,
                    new=True,
                    set__limit = budget.limit + unused_amount,
                    set__rollover_enabled = True,
                    set__current_spending = 0.0,
                    set__last_updated = now
                )

                if self.notification_handler:
                    self.notification_handler(
                        user = budget.user,
                        title= "Budget Roll Over Successful",
                        message = f"₦{unused_amount:,.2f} rolled over to {next_month_date.strftime('%B')} {budget.category} budget!",
                        category = "Budget_rollover",
                    )
            except Exception as e:
                print(traceback.format_exc())
                if self.notification_handler:
                    self.notification_handler(
                        user = budget.user,
                        title= "Roll Over Failed",
                        message = str(e),
                        category = "Error: Budget_rollover failed",
                    )





