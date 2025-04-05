from apps.services.notifications import NotificationService


class NotificationAdapter:
    @staticmethod
    def handle_notification(user, title, message, category):
        NotificationService.create(
            user=user,
            title=title,
            message=message,
            category=category,
        )