from app.database.db import db
from app.models.activity_log import ActivityLog


class ActivityLogService:

    # ---------------------------------
    # Create Activity
    # ---------------------------------

    @staticmethod
    def create(user_id, activity, module):

        log = ActivityLog(

            user_id=user_id,

            activity=activity,

            module=module

        )

        db.session.add(log)
        db.session.commit()

        return log

    # ---------------------------------
    # Get All Logs
    # ---------------------------------

    @staticmethod
    def get_all():

        return ActivityLog.query.order_by(

            ActivityLog.created_at.desc()

        ).all()

    # ---------------------------------
    # Get One Log
    # ---------------------------------

    @staticmethod
    def get(log_id):

        return db.session.get(ActivityLog, log_id)

    # ---------------------------------
    # Delete One Log
    # ---------------------------------

    @staticmethod
    def delete(log_id):

        log = db.session.get(ActivityLog, log_id)

        if log:

            db.session.delete(log)

            db.session.commit()

            return True

        return False

    # ---------------------------------
    # Delete All Logs
    # ---------------------------------

    @staticmethod
    def delete_all():

        ActivityLog.query.delete()

        db.session.commit()

        return True

    # ---------------------------------
    # Count Logs
    # ---------------------------------

    @staticmethod
    def total_logs():

        return ActivityLog.query.count()

    # ---------------------------------
    # Recent Logs
    # ---------------------------------

    @staticmethod
    def recent(limit=10):

        return ActivityLog.query.order_by(

            ActivityLog.created_at.desc()

        ).limit(limit).all()