import io
import json
import unittest
from email.message import Message
from unittest.mock import patch
import mcp_client as m

class Response:
    def __init__(self, data, typ="application/json", session=None):
        self.data=data
        self.headers=Message()
        self.headers["Content-Type"]=typ
        if session: self.headers["Mcp-Session-Id"]=session
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def read(self): return self.data

class Tests(unittest.TestCase):
    def test_json(self):
        self.assertEqual(m.decode_response(b'{"result":1}',"application/json"), {"result":1})
    def test_sse(self):
        self.assertEqual(m.decode_response(b'event: message\\ndata: {"result":2}\\n\\n'.replace(b'\\n',b'\n'), "text/event-stream"), {"result":2})
    def test_session_and_methods(self):
        calls=[]
        def opener(req, timeout):
            body=json.loads(req.data)
            calls.append((body,req.headers.get("Mcp-session-id")))
            if body["method"]=="initialize":
                return Response(json.dumps({"jsonrpc":"2.0","id":body["id"],"result":{"protocolVersion":m.PROTOCOL}}).encode(),session="session-1")
            if body["method"]=="notifications/initialized":
                return Response(b'')
            return Response(json.dumps({"jsonrpc":"2.0","id":body["id"],"result":{"content":[]}}).encode())
        c=m.MCPClient(opener=opener)
        c.initialize()
        self.assertEqual(c.list()["result"], {"content":[]})
        self.assertEqual([x[0]["method"] for x in calls],["initialize","notifications/initialized","tools/call"])
        self.assertEqual(calls[2][1],"session-1")
        self.assertEqual(calls[2][0]["params"]["name"],"list_bounties")
    def test_error(self):
        c=m.MCPClient(opener=lambda req,timeout: Response(b'{"error":{"message":"failed"}}'))
        with self.assertRaises(ValueError): c.list()

if __name__=="__main__": unittest.main()
