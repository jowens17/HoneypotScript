# HoneypotScript

**Simple WordPress Honeypot**
Hello Everyone! This is my final capstone project for my network security course. It’s a basic honeypot that looks like a real WordPress login page to attract attackers and log their activity.

It logs stuff like:

Login page visits

Login attempts (including usernames + passwords they try)

Suspicious requests (like people looking for WordPress admin pages or config files)

I built it using Python and the built-in http.server — no fancy frameworks needed.

Features
- Fake WordPress login page
- Logs IP addresses, user agents, paths, and attempted credentials
- Easy to deploy (no extra software required)
- Generates JSON logs you can analyze later


**How to Run It**

1.Clone this Repo 
2.Run the Honeypot through your code editor or command on your desired OS. 
    - For Windows, open command Prompt and type "**python honeypot.py**"

That is it and it should start running on: 
**http://localhost:8080**

You can visit **http://localhost:8080/wp-login.php** to see the fake WordPress login page.

**Viewing the Logs **

- All activity gets saved in a file called honeypot_log.json


**Deployment of the Honeypot**

You can run this honeypot just on your computer (localhost), on your home network (so other devices like your phone can access it), or you can even make it public on the internet using ngrok.

Option 1: Local Network
To access it on other devices (like your phone):

Find your local IP address

Windows: ipconfig

Mac/Linux: ifconfig or ip a

Visit it on another device like:
**http://<your-local-ip>:8080**

Option 2: Make it Public with ngrok

This is cool if you want to show it off or attract real internet traffic (be careful though!).

Download ngrok: https://ngrok.com/download

In another terminal run ngrok: 
  ngrok http 8080
  
ngrok will give you a link like:
**https://example.ngrok.io**


**DISCLAIMER** ⚠️

This is for educational purposes only. Don't use it to break laws or attack real people. Hosting honeypots to the public internet can be risky, so be careful and monitor what happens. Please use a virual machine or sandbox to be safe and most importantly- Use for ethical use only!




