import smtplib
from pathlib import Path

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from typing import Sequence
from lhltools import email_conf_map


class EmailServerException(Exception):
    def __init__(self, message: str):
        super().__init__(f"email server exception: {message}")


class Attachment(object):
    path: str
    data: bytes
    name: str

    __slots__ = ["path", "data", "name"]

    def __init__(self, path: str = "", data: bytes = b"", name: str = "") -> None:
        self.path = path
        self.data = data
        self.name = name


class Email(object):
    subject: str
    receivers: Sequence[str]
    text: str
    html: str
    attachments: Sequence[Attachment]

    __slots__ = ["subject", "receivers", "text", "html", "attachments"]

    def __init__(
        self,
        subject: str,
        receivers: Sequence[str],
        text: str = "",
        html: str = "",
        attachments: Sequence[Attachment] = [],
    ):
        self.subject = subject
        self.receivers = receivers
        self.text = text
        self.html = html
        self.attachments = attachments


class EmailTool(object):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(EmailTool, cls).__new__(cls)
        return cls.__instance

    def send_email(self, email: Email):
        self.__check_email_server(email)
        message = MIMEMultipart()
        message["Subject"] = email.subject
        message["From"] = email_conf_map["user"]
        message["To"] = ",".join(email.receivers)
        message["Bcc"] = ",".join(email.receivers)

        if email.text:
            message.attach(MIMEText(email.text, "plain", "utf-8"))
        elif email.html:
            message.attach(MIMEText(email.html, "html", "utf-8"))

        # 附件
        if email.attachments:
            for attachment in email.attachments:
                if attachment.path != "":
                    with open(attachment.path, "rb") as f:
                        part = MIMEApplication(f.read())
                        if attachment.name == "":
                            part.add_header(
                                "Content-Disposition",
                                "attachment",
                                filename=Path(attachment.path).name,
                            )
                        else:
                            part.add_header(
                                "Content-Disposition",
                                "attachment",
                                filename=attachment.name,
                            )
                        message.attach(part)
                elif attachment.data != b"":
                    attachment.name = (
                        attachment.name
                        if attachment.name != ""
                        else "nonoNameAttachment"
                    )
                    part = MIMEApplication(attachment.data)
                    part.add_header(
                        "Content-Disposition", "attachment", filename=attachment.name
                    )
                    message.attach(part)

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(email_conf_map["host"], int(email_conf_map["port"]))
            smtpObj.login(
                user=email_conf_map["user"], password=email_conf_map["password"]
            )
            smtpObj.sendmail(
                email_conf_map["user"], email.receivers, message.as_string()
            )
        except smtplib.SMTPException as e:
            raise e

    def __check_email_server(self, email: Email):
        if not email_conf_map:
            raise EmailServerException("No email server config")
        if len(email.receivers) == 0:
            raise EmailServerException("No receivers")
