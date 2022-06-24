# -*- coding: utf-8 -*-
"""This module contain the confuguration for the application."""
import json
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from smtplib import SMTP_SSL, SMTPException

import boto3


class KinesisFirehoseDeliveryStreamHandler(logging.StreamHandler):
    """This class sends our logs to Amazon Kinesis."""

    def __init__(self):
        """Initialize the firehose stream.."""
        # By default, logging.StreamHandler uses sys.stderr if stream parameter is not specified
        logging.StreamHandler.__init__(self)

        self.__firehose = None
        self.__stream_buffer = []

        try:
            self.__firehose = boto3.client('firehose')
        except Exception:
            print('Firehose client initialization failed.')

        self.__delivery_stream_name = "flask-logging-firehose-stream"

    def emit(self, record):
        """Send the formatted log to AWS Firehose."""
        try:
            msg = self.format(record)

            if self.__firehose:
                self.__stream_buffer.append({
                    'Data': msg.encode(encoding="UTF-8", errors="strict")
                })
            else:
                stream = self.stream
                stream.write(msg)
                stream.write(self.terminator)

            self.flush()
        except Exception:
            self.handleError(record)

    def flush(self):
        """Flush the log buffer."""
        self.acquire()

        try:
            if self.__firehose and self.__stream_buffer:
                self.__firehose.put_record_batch(
                    DeliveryStreamName=self.__delivery_stream_name,
                    Records=self.__stream_buffer
                )

                self.__stream_buffer.clear()
        except Exception as e:
            print("An error occurred during flush operation.")
            print(f"Exception: {e}")
            print(f"Stream buffer: {self.__stream_buffer}")
        finally:
            if self.stream and hasattr(self.stream, "flush"):
                self.stream.flush()

            self.release()


class CustomEmailLogger(logging.Handler):
    """Custom email logger."""

    def __init__(self) -> None:
        """Initialize the logger."""
        logging.Handler.__init__(self)
        self.mailport = 465
        self.mailhost = "email-smtp.us-east-1.amazonaws.com"
        self.fromaddr = 'lyceokoth@gmail.com'
        self.toaddrs = 'lyceokoth@gmail.com'
        self.username = 'AKIA52VMBL5RHSMWE5XT'
        self.password = 'BHxLrWkMAfFbRCfGiASofC7K8L+SmUDRdQB72wKcjIz4'
        self.sender_name = 'Lyle from Amazon'

    def emit(self, record):
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        try:
            log_record = json.loads(self.format(record))

            # Try to send the message.
            if log_record['levelname'] in ['WARNING', 'CRITICAL']:
                with SMTP_SSL(self.mailhost, self.mailport) as server:
                    SUBJECT = log_record['levelname']
                    BODY_HTML = f"""
                    <html>
                        <head>
                        </head>
                        <body>
                            <h1>
                                {log_record['name']}
                            </h1>
                            <p>
                                {log_record['message']}
                            </p>
                        </body>
                    </html>"""
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = SUBJECT
                    msg['From'] = formataddr((self.sender_name, self.fromaddr))
                    msg['To'] = self.toaddrs

                    part2 = MIMEText(BODY_HTML, 'html')

                    msg.attach(part2)
                    server.login(self.username, self.password)
                    server.sendmail(self.fromaddr, self.toaddrs, msg.as_string())
                    server.close()
                    print("Email sent!")

        except SMTPException as e:
            print("Error: ", e)
        except Exception as e:
            print(f"Exception: {e}")

    def close(self):
        """Terminate the handler."""
        logging.Handler.close(self)
