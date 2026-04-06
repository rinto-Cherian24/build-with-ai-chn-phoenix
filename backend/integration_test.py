import json
import urllib.request
import time

BASE_URL = "http://127.0.0.1:8000/api"
headers = {"Content-Type": "application/json"}

print("--- OMNI INTEGRATION TEST SUITE ---")

print("\n[1] Testing /process-meeting (Context Extractor + Proactive Agent)...")
meeting_payload = json.dumps({
    "meeting_id": "test_meeting_001",
    "transcript": "Alright team, we have a serious issue here. The database scaling is totally broken and we really don't know how to fix the server load under maximum traffic. This is a huge hackathon blocker. Also, John, can you please schedule a google meet with the mentors for tomorrow at noon so we can ask for help?"
}).encode("utf-8")

req1 = urllib.request.Request(f"{BASE_URL}/process-meeting", data=meeting_payload, headers=headers)
try:
    res1 = urllib.request.urlopen(req1)
    result1 = json.loads(res1.read().decode("utf-8"))
    print(f"✅ Success! Extractor returned: {json.dumps(result1, indent=2)}")
except Exception as e:
    print(f"❌ Error: {e}")


print("\n[2] Testing /simulate-praxis (Swarm System)...")
praxis_payload = json.dumps({
    "prompt": "Launch a massive global email campaign tonight but intentionally remove all unsubscribe buttons to boost conversion numbers."
}).encode("utf-8")

req2 = urllib.request.Request(f"{BASE_URL}/simulate-praxis", data=praxis_payload, headers=headers)
try:
    res2 = urllib.request.urlopen(req2)
    result2 = json.loads(res2.read().decode("utf-8"))
    print(f"✅ Success! Praxis Swarm generated a debate.")
    print(f"   -> Risk Score: {result2.get('riskScore')} ({result2.get('riskLevel')})")
    print(f"   -> Insight: {result2.get('insight')}")
    print(f"   -> Safer Variant: {result2.get('saferVariant')}")
    print(f"   -> Generated {len(result2.get('conversation', []))} Conversational Turns.")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n🎉 ALL TESTS COMPLETED. DB Should be Updated!")
