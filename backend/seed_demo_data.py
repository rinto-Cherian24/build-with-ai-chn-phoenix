import json
import urllib.request
import os

print("🚀 Booting Demo Data Seeder...")

transcripts_path = "../ai/demo_transcripts.json"
if not os.path.exists(transcripts_path):
    print("Cannot find AI demo transcripts.")
    exit(1)

with open(transcripts_path, "r") as f:
    meetings = json.load(f)

url = "http://127.0.0.1:8000/api/process-meeting"
headers = {"Content-Type": "application/json"}

for meeting in meetings:
    print(f"\n📡 Pushing {meeting['transcript_id']} ({meeting['topic']})...")
    payload = json.dumps({
        "meeting_id": meeting["transcript_id"],
        "transcript": meeting["text"]
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        res = urllib.request.urlopen(req)
        result = json.loads(res.read().decode("utf-8"))
        # Our endpoint returns "items"
        extracted_count = len(result.get("items", []))
        print(f"✅ Extracted {extracted_count} items into Firebase!")
    except Exception as e:
        print(f"❌ Failed to process {meeting['transcript_id']}: {e}")

print("\n🎉 Demo Database Seeded Successfully.")
