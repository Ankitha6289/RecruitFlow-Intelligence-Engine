from datetime import datetime

import requests
from flask import current_app


class ZoomMeetingError(RuntimeError):
    pass


class ZoomMeetingService:
    TOKEN_URL = "https://zoom.us/oauth/token"
    MEETINGS_URL = "https://api.zoom.us/v2/users/me/meetings"

    @staticmethod
    def create_meeting(topic, interview_date, interview_time):
        account_id = current_app.config.get("ZOOM_ACCOUNT_ID")
        client_id = current_app.config.get("ZOOM_CLIENT_ID")
        client_secret = current_app.config.get("ZOOM_CLIENT_SECRET")

        if not all((account_id, client_id, client_secret)):
            raise ZoomMeetingError(
                "Online interviews require Zoom Server-to-Server OAuth credentials."
            )

        try:
            token_response = requests.post(
                ZoomMeetingService.TOKEN_URL,
                params={
                    "grant_type": "account_credentials",
                    "account_id": account_id,
                },
                auth=(client_id, client_secret),
                timeout=8,
            )
            token_response.raise_for_status()
            access_token = token_response.json().get("access_token")
            if not access_token:
                raise ZoomMeetingError("Zoom did not return an access token.")

            try:
                start_time = datetime.fromisoformat(
                    f"{interview_date}T{interview_time}"
                ).isoformat()
            except (ValueError, TypeError) as dt_err:
                raise ZoomMeetingError(
                    f"Invalid interview date/time format: {interview_date} {interview_time}. "
                    "Expected YYYY-MM-DD and HH:MM."
                ) from dt_err

            meeting_response = requests.post(
                ZoomMeetingService.MEETINGS_URL,
                headers={"Authorization": f"Bearer {access_token}"},
                json={
                    "topic": topic,
                    "type": 2,
                    "start_time": start_time,
                    "duration": current_app.config[
                        "ZOOM_MEETING_DURATION_MINUTES"
                    ],
                    "timezone": current_app.config["ZOOM_TIMEZONE"],
                    "settings": {
                        "waiting_room": True,
                        "join_before_host": False,
                    },
                },
                timeout=8,
            )
            meeting_response.raise_for_status()
            join_url = meeting_response.json().get("join_url")
            if not join_url:
                raise ZoomMeetingError("Zoom did not return a meeting link.")
            return join_url
        except requests.RequestException as error:
            raise ZoomMeetingError(
                "Zoom could not create the meeting. Check the Zoom credentials and try again."
            ) from error
        except ZoomMeetingError:
            raise
        except Exception as error:
            raise ZoomMeetingError(
                f"Zoom meeting creation failed: {error}"
            ) from error