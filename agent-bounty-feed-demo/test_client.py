import io
import json
import unittest
from unittest.mock import patch
import client

class FakeResponse:
    def __init__(self, data):
        self.data = json.dumps(data).encode()
    def __enter__(self):
        return io.BytesIO(self.data)
    def __exit__(self, *args):
        return False

class FeedTests(unittest.TestCase):
    def test_list_feed(self):
        self.assertEqual(client.load_feed(opener=lambda req, timeout: FakeResponse([{"id":"one"}])), [{"id":"one"}])
    def test_items_feed(self):
        self.assertEqual(client.load_feed(opener=lambda req, timeout: FakeResponse({"items":[{"id":"two"}]})), [{"id":"two"}])
    def test_bounties_feed(self):
        self.assertEqual(client.load_feed(opener=lambda req, timeout: FakeResponse({"bounties":[]})), [])
    def test_invalid_structure(self):
        with self.assertRaises(ValueError):
            client.load_feed(opener=lambda req, timeout: FakeResponse({"unknown":[]}))

if __name__ == "__main__":
    unittest.main()
