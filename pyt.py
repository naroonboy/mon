from flask import Flask, render_template
import requests

app = Flask(__name__)

# List of hostnames
HOSTS = ["host1.example.com", "host2.example.com", "host3.example.com"]

# List of ports to query per host
PORTS = [8443, 8444, 8445]

@app.route("/")
def index():
    data = []
    for hostname in HOSTS:
        for port in PORTS:
            url = f"https://{hostname}:{port}/adcs-health"
            try:
                response = requests.get(url, verify=False, timeout=5)
                if response.ok:
                    health = response.json()
                    data.append({
                        "hostname": hostname,
                        "port": port,
                        "status": health.get("status", "unknown"),
                        "upsince": health.get("upsince", "unknown"),
                        "uptime": health.get("uptime", "unknown")
                    })
                else:
                    data.append({
                        "hostname": hostname,
                        "port": port,
                        "status": "error",
                        "upsince": "-",
                        "uptime": "-"
                    })
            except Exception as e:
                data.append({
                    "hostname": hostname,
                    "port": port,
                    "status": "unreachable",
                    "upsince": "-",
                    "uptime": "-"
                })

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
