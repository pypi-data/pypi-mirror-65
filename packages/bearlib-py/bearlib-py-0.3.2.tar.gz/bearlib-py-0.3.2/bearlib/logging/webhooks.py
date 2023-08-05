import requests
import json
from datetime import datetime


tstamp_template = "%Y-%m-%dT%H:%M:%S.%f"

"""
Webhook Handler for logging.core

Notes:

Setting an error_limit of -1 disables the error limit, default 10
"""


class WebhookFailException(Exception):
    def __init__(self, hook_type, error_code):
        self.hook_type = hook_type
        self.error_code = error_code


class Webhook:
    messages = []

    def __init__(
        self,
        hook_url,
        summary,
        error_limit=10,
        notify_only=False,
        log_path=None,
    ):
        self.summary = summary
        self.hook_url = hook_url
        if type(error_limit) == int:
            self.error_limit = error_limit
        else:
            self.error_limit = 10
        if notify_only is True:
            self.notify_only = True
        else:
            self.notify_only = False
        self.log_path = log_path

    def add_message(self, level, message, tstamp):
        if self.error_limit > 0 and len(self.messages) < self.error_limit:
            self.messages.append(
                {"level": level, "tstamp": tstamp, "message": message}
            )
        elif len(self.messages) == self.error_limit:
            self.messages[-1] = {
                "level": "WARNING",
                "tstamp": tstamp,
                "message": f"More than {self.error_limit} errors occured. "
                + "Please view logs",
            }

    def send_to_hook(self):
        if len(self.messages) == 0:
            return
        if self.notify_only:
            self.messages = [
                {
                    "level": "INFO",
                    "tstamp": datetime.now().strftime(tstamp_template),
                    "message": f"Program had messages, but is in notify-only mode. "
                    + "Please check logs to see messages",
                }
            ]
        msg = self.get_formatted_msg()
        headers = {"Content-Type": "application/json"}
        try:
            req = requests.post(
                self.hook_url, headers=headers, data=json.dumps(msg)
            )
        except ConnectionError as e:
            raise WebhookFailException(
                self.__class__.__name__, e.args[0].message
            )
        if req.status_code < 200 or req.status_code >= 300:
            raise WebhookFailException(
                self.__class__.__name__, req.status_code
            )
        self.messages = []

    def get_formatted_msg(self):
        pass


class Teams(Webhook):
    def __init__(
        self,
        hook_url,
        summary,
        error_limit=10,
        notify_only=False,
        log_path=None,
        subtitle=None,
    ):
        super().__init__(hook_url, summary, error_limit, notify_only, log_path)
        if subtitle is None:
            if log_path is not None:
                subtitle = log_path
            else:
                subtitle = "No log for this program"
        self.subtitle = subtitle

    def get_formatted_msg(self):
        tmp = [x for x in self.messages]
        self.messages = []
        for t in tmp:
            level = t["level"]
            tstamp = t["tstamp"]
            message = t["message"]
            self.messages.append(
                {"name": level, "value": f"[{tstamp}] {message}"}
            )
        teams_message = {
            "@type": "MessageCard",
            "summary": self.summary,
            "sections": [
                {
                    "activityTitle": self.summary,
                    "activitySubtitle": self.subtitle,
                    "facts": self.messages,
                    "markdown": True,
                }
            ],
        }
        return teams_message


class Discord(Webhook):
    embed_color = int("F6B000", 16)  # UNCO Gold

    def __init__(
        self,
        hook_url,
        summary,
        error_limit=10,
        notify_only=False,
        log_path=None,
    ):
        super().__init__(hook_url, summary, error_limit, notify_only, log_path)

    def get_formatted_msg(self):
        embed = {
            "color": self.embed_color,
            "timestamp": datetime.now().isoformat(),
            "footer": {"text": "Sent using BearLib"},
            "fields": [],
        }
        for message in self.messages:
            embed["fields"].append(
                {
                    "name": message["level"],
                    "value": f"[{message['tstamp']}] {message['message']}",
                }
            )
        discord_message = {"content": self.summary, "embeds": [embed]}
        return discord_message


class Slack(Webhook):
    attachment_color = "#F6B000"  # UNCO Gold

    def __init__(
        self,
        hook_url,
        summary,
        error_limit=10,
        notify_only=False,
        log_path=None,
    ):
        super().__init__(hook_url, summary, error_limit, notify_only, log_path)

    def get_formatted_msg(self):
        slack_message = {
            "attachments": [
                {
                    "fallback": self.summary,
                    "color": self.attachment_color,
                    "text": self.summary,
                    "fields": [],
                }
            ]
        }
        for message in self.messages:
            slack_message["attachments"][0]["fields"].append(
                {
                    "value": f"[{message['tstamp']}] [{message['level']}] {message['message']}",
                    "short": False,
                }
            )
        return slack_message


types = [Teams, Discord, Slack]


def register_webhook(hook):
    if Webhook in hook.__mro__:
        if hook not in types:
            types.append(hook)
            return f"Registered {hook.__class__.__name__} as valid webhook"
        else:
            return f"{hook.__class__.__name__} already registered as valid webhook"
    return f"{hook.__class__.__name__} is not a valid webhook. Please use superclass Webhook"
