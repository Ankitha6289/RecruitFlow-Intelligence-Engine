from app.database.db import db
from app.models.notification import Notification


class NotificationService:

    # -------------------------------------
    # Create Notification
    # -------------------------------------

    @staticmethod
    def create(
        title,
        message,
        notification_type="General",
        recipient_role="All"
    ):

        notification = Notification(
            title=title,
            message=message,
            notification_type=notification_type,
            recipient_role=recipient_role
        )

        db.session.add(notification)
        db.session.commit()

        return notification

    # -------------------------------------
    # Get All Notifications
    # -------------------------------------

    @staticmethod
    def get_all():

        return Notification.query.order_by(
            Notification.notification_id.desc()
        ).all()

    # -------------------------------------
    # Get Unread Notifications
    # -------------------------------------

    @staticmethod
    def unread():

        return Notification.query.filter_by(
            is_read=False
        ).order_by(
            Notification.notification_id.desc()
        ).all()

    # -------------------------------------
    # Count Unread
    # -------------------------------------

    @staticmethod
    def unread_count():

        return Notification.query.filter_by(
            is_read=False
        ).count()

    # -------------------------------------
    # Mark Read
    # -------------------------------------

    @staticmethod
    def mark_read(notification_id):

        notification = db.session.get(Notification, notification_id)

        if notification:

            notification.is_read = True

            db.session.commit()

    # -------------------------------------
    # Mark All Read
    # -------------------------------------

    @staticmethod
    def mark_all_read():

        Notification.query.update(
            {
                "is_read": True
            }
        )

        db.session.commit()

    # -------------------------------------
    # Delete One
    # -------------------------------------

    @staticmethod
    def delete(notification_id):

        notification = db.session.get(Notification, notification_id)

        if notification:

            db.session.delete(notification)

            db.session.commit()

    # -------------------------------------
    # Delete All
    # -------------------------------------

    @staticmethod
    def delete_all():

        Notification.query.delete()

        db.session.commit()