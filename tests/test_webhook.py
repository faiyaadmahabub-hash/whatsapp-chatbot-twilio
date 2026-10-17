"""Exercise the real webhook locally; no WhatsApp/Twilio account is contacted."""
from pathlib import Path
import importlib.util
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('whatsapp_webhook', ROOT / 'Coding_For_Whatsapp_chatbot/main.py')
webhook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(webhook)


class WebhookTests(unittest.TestCase):
    def setUp(self):
        self.client = webhook.app.test_client()

    def test_keyword_replies_are_twiml(self):
        for message, expected in [
            ('hello', 'Hello! I am your WhatsApp bot.'),
            ('HELP', 'Available commands:\n- hello\n- info\n- bye'),
            ('info', 'This is a simple WhatsApp chatbot built from scratch.'),
            ('bye', 'Goodbye.'),
            ('unrecognized input', "Command not recognized. Type 'help'."),
        ]:
            with self.subTest(message=message):
                response = self.client.post('/whatsapp', data={'Body': message})
                self.assertEqual(response.status_code, 200)
                xml = ET.fromstring(response.data)
                self.assertEqual(xml.tag, 'Response')
                self.assertEqual(xml.findtext('Message/Body'), expected)

    def test_missing_body_uses_fallback_instead_of_crashing(self):
        response = self.client.post('/whatsapp', data={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ET.fromstring(response.data).findtext('Message/Body'), "Command not recognized. Type 'help'.")

    def test_webhook_accepts_post_only(self):
        self.assertEqual(self.client.get('/whatsapp').status_code, 405)


if __name__ == '__main__':
    unittest.main()
