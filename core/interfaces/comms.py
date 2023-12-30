from abc import ABC, abstractmethod


class CommunicationsInterface(ABC):
    def send_auto(self, contact_type: str, contact_value: str, subject, message):
        if contact_type == 'email':
            self.send_email(contact_value, subject, message)
        if contact_type == 'phone':
            self.send_sms(contact_value, f"{subject}: {message}")

    @abstractmethod
    def send_sms(self, destination: str, message: str):
        """send the message to the destination number"""

    @abstractmethod
    def send_email(self, destination_email: str, subject: str, body: str):
        """send the email to the destination address"""
