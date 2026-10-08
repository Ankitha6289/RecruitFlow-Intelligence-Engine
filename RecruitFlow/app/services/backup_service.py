import os
import subprocess
from datetime import datetime


class BackupService:

    DB_NAME = "recruitflow"

    DB_USER = "root"

    DB_PASSWORD = "anki2003"

    BACKUP_FOLDER = "backups"


    # ==========================================
    # Create Backup
    # ==========================================

    @staticmethod
    def create_backup():

        os.makedirs(

            BackupService.BACKUP_FOLDER,

            exist_ok=True

        )

        filename = f"recruitflow_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"

        filepath = os.path.join(

            BackupService.BACKUP_FOLDER,

            filename

        )

        command = (

            f'mysqldump -u {BackupService.DB_USER} '

            f'-p{BackupService.DB_PASSWORD} '

            f'{BackupService.DB_NAME} > "{filepath}"'

        )

        result = os.system(command)

        if result == 0:

            return filepath

        return None


    # ==========================================
    # Restore Backup
    # ==========================================

    @staticmethod
    def restore_backup(filepath):

        if not os.path.exists(filepath):

            return False

        command = (

            f'mysql -u {BackupService.DB_USER} '

            f'-p{BackupService.DB_PASSWORD} '

            f'{BackupService.DB_NAME} < "{filepath}"'

        )

        result = os.system(command)

        return result == 0


    # ==========================================
    # Latest Backup
    # ==========================================

    @staticmethod
    def latest_backup():

        if not os.path.exists(

            BackupService.BACKUP_FOLDER

        ):

            return None

        files = [

            os.path.join(

                BackupService.BACKUP_FOLDER,

                f

            )

            for f in os.listdir(

                BackupService.BACKUP_FOLDER

            )

            if f.endswith(".sql")

        ]

        if not files:

            return None

        return max(

            files,

            key=os.path.getctime

        )