import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from hashlib import md5
import random, string

# Load helper
def load(path): return open(path).read().strip()

# Load config files
api_key = load("mailchimp_key.txt")         # Your API key
server_prefix = api_key.split("-")[-1]      # Extract 'us6', 'us20', etc.
audience_id = load("audience_id.txt")       # e.g., 226f74d719
recipient = load("recipient.txt")           # Your email
link = load("link.txt")                     # The link to embed
message_template = load("message.txt")      # Message with {link} placeholder

# Setup Mailchimp client
client = MailchimpMarketing.Client()
client.set_config({
    "api_key": api_key,
    "server": server_prefix
})

# Prepare HTML with link inside <a>
safe_html = message_template.replace(
    "{link}", f'<a href="{link}">{link}</a>'
)
html_content = f"<html><body><p>{safe_html}</p></body></html>"

try:
    # Add or update the recipient
    subscriber_hash = md5(recipient.lower().encode()).hexdigest()
    client.lists.set_list_member(audience_id, subscriber_hash, {
        "email_address": recipient,
        "status_if_new": "subscribed",
        "status": "subscribed",
        "merge_fields": {
            "FNAME": "Tester",
            "LNAME": "User"
        }
    })
    print(f"[+] Subscriber ready: {recipient}")

    # Create campaign
    campaign = client.campaigns.create({
        "type": "regular",
        "recipients": {"list_id": audience_id},
        "settings": {
            "subject_line": "Tracked Link Test",
            "title": "Campaign " + ''.join(random.choices(string.ascii_letters, k=6)),
            "from_name": "Tracker",
            "reply_to": recipient
        },
        "tracking": {
            "opens": True,
            "html_clicks": True,
            "text_clicks": True
        }
    })
    print(f"[+] Campaign created: {campaign['id']}")

    # Set HTML content
    client.campaigns.set_content(campaign['id'], {"html": html_content})
    print("[+] HTML content added.")

    # Send campaign
    client.campaigns.send(campaign['id'])
    print(f"[✓] Sent to {recipient}!")

except ApiClientError as e:
    print(f"[!] Mailchimp API Error:\n{e.text}")