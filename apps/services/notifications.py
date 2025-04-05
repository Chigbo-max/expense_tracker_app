from apps.data.model.notifications import Notifications


class NotificationService:
    @staticmethod
    def create(user, title, message, category='system'):
        notification = Notifications(
            user=user,
            title=title,
            message=message,
            category=category,
        ).save()
        return notification