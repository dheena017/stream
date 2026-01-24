
import json
import unittest
import sys
import os

# Ensure root is in path
sys.path.append(os.getcwd())

from PIL import Image
from ui.chat_utils import serialize_messages

class TestExport(unittest.TestCase):
    def test_serialize_messages(self):
        # Create dummy image
        img = Image.new('RGB', (10, 10), color = 'red')

        messages = [
            {
                "role": "user",
                "content": "Look at this image",
                "images": [img],
                "timestamp": "12:00:00"
            },
            {
                "role": "assistant",
                "content": "Nice red square",
                "images": [],
                "timestamp": "12:00:05"
            }
        ]

        serialized = serialize_messages(messages)

        # Check if serializable
        try:
            json_str = json.dumps(serialized)
        except TypeError:
            self.fail("serialized messages are not JSON serializable")

        # Check content
        self.assertTrue(isinstance(serialized[0]["images"][0], str))
        print(f"Serialized image desc: {serialized[0]['images'][0]}")
        self.assertIn("Image <None (10, 10)>", serialized[0]["images"][0])

if __name__ == '__main__':
    unittest.main()
