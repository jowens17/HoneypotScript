# Final Capstone Project 
#IDL Q4 Final Project 

from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
import json
import datetime

# Configuration of Port 
PORT = 8080
LOG_FILE = "honeypot_log.json"

# Basic suspicious paths
SUSPICIOUS_PATHS = ["/wp-admin", "/xmlrpc.php", "/wp-config", "shell", "upload"]

# Setting up simple logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

class SimpleHoneypotHandler(BaseHTTPRequestHandler):
    def log_request_details(self, extra_info=None):
        """Log IP, path, user-agent, and extra info (optional)."""
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "ip": self.client_address[0],
            "method": self.command,
            "path": self.path,
            "user_agent": self.headers.get('User-Agent', 'Unknown'),
        }
        if extra_info:
            log_entry.update(extra_info)

        # Logs are sent to console
        logging.info(json.dumps(log_entry))

        # Log to file
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def send_simple_page(self, content, status=200):
        """Helper to send a basic HTML response."""
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())

    def do_GET(self):
        if any(keyword in self.path.lower() for keyword in SUSPICIOUS_PATHS):
            self.log_request_details({"event": "suspicious GET"})
            self.send_simple_page("<h1>404 Not Found</h1>", status=404)
        elif self.path == "/wp-login.php":
            self.log_request_details({"event": "login page visited"})
            self.send_simple_page("""
<html lang="en-US"> 
<head>
    <meta charset="UTF-8">
    <title>Log In &lsaquo; My Fake WordPress Site &#8212; WordPress</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #f1f1f1; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif; }
        .login { width: 320px; padding: 8% 0 0; margin: auto; }
        .login h1 a { background-image:('wordpress-logo.png'); background-size: contain; width: 84px; height: 84px; display: block; margin: 0 auto 16px; text-indent: -9999px; }
        form { background: #fff; padding: 26px 24px 46px; border: 1px solid #c3c4c7; box-shadow: 0 1px 3px rgba(0,0,0,.04); }
        label { font-size: 14px; display: block; margin-bottom: 4px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 8px; box-sizing: border-box; margin-bottom: 16px; border: 1px solid #ddd; border-radius: 4px; }
        input[type="submit"] { background: #2271b1; border: none; color: #fff; padding: 8px 16px; border-radius: 4px; cursor: pointer; width: 100%; }
        input[type="submit"]:hover { background: #135e96; }
        .forgetmenot { margin-bottom: 16px; }
        .wp-pwd { position: relative; }
        .nav { margin-top: 16px; text-align: center; }
        .nav a { color: #2271b1; text-decoration: none; }
        .nav a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="login">
        <h1><a href="#" title="WordPress">WordPress</a></h1>
        <form method="POST">
            <label for="user">Username or Email Address</label>
            <input type="text" name="user" id="user" required>

            <label for="pass">Password</label>
            <input type="password" name="pass" id="pass" required>

            <div class="forgetmenot">
                <label><input name="rememberme" type="checkbox" value="forever"> Remember Me</label>
            </div>

            <input type="submit" value="Log In">
        </form>

        <p class="nav">
            <a href="#">Lost your password?</a>
        </p>
    </div>
</body>
</html>
            """) #Any UI fixes should be changed with HTML above
        else:
            self.log_request_details({"event": "normal GET"})
            self.send_simple_page("<h1>Welcome to the fake WordPress site</h1>")

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(length).decode()
        self.log_request_details({"event": "login attempt", "post_data": post_data})

        #  Ensuring that any login would always fail
        self.send_simple_page("<h1>Login Failed</h1><p>Invalid credentials</p>")

def run():
    server = HTTPServer(('', PORT), SimpleHoneypotHandler)
    print(f"Honeypot running on port {PORT} — press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down honeypot...")

if __name__ == "__main__":
    run()
