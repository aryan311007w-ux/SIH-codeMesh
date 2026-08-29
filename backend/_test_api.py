import urllib.request, json, urllib.error

addr = "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD38"
base = "http://localhost:8000"
endpoints = [
    "/api/health",
    "/api/chains",
    "/api/trace?wallet=" + addr + "&chain=ethereum",
    "/api/risk/" + addr,
    "/api/history",
    "/api/vasps",
]

for ep in endpoints:
    url = base + ep
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            body = json.loads(resp.read())
        print("\n=== " + ep + " ===")
        print("Status: " + str(status))
        print(json.dumps(body, indent=2)[:500])
    except urllib.error.HTTPError as e:
        print("\n=== " + ep + " ===")
        print("HTTP Error: " + str(e.code))
        print(e.read().decode()[:200])
    except Exception as ex:
        print("\n=== " + ep + " ===")
        print("Error: " + str(ex))

# Test report endpoint
print("\n=== /api/report/{wallet} ===")
url2 = base + "/api/report/" + addr
try:
    req2 = urllib.request.Request(url2)
    with urllib.request.urlopen(req2) as resp2:
        data = resp2.read()
    print("Status: " + str(resp2.status))
    ct = resp2.headers.get('Content-Type', '')
    print("Content-Type: " + ct)
    print("Size: " + str(len(data)) + " bytes")
    if data[:4] == b'%PDF':
        print("Valid PDF header confirmed")
    else:
        print("WARNING: Not a PDF")
except urllib.error.HTTPError as e:
    print("HTTP Error: " + str(e.code))
    print(e.read().decode()[:200])
except Exception as ex:
    print("Error: " + str(ex))

# Test alerts endpoint
print("\n=== /api/alerts/high-risk ===")
try:
    req3 = urllib.request.Request(base + "/api/alerts/high-risk")
    with urllib.request.urlopen(req3) as resp3:
        data3 = json.loads(resp3.read())
    print(json.dumps(data3, indent=2)[:300])
except Exception as ex:
    print("Error: " + str(ex))
