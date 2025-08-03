# 📬 Mailchimp Audience ID Fetcher

This simple script uses `curl` to fetch all your Mailchimp audiences (lists) and their IDs via the Mailchimp Marketing API.

---

## 🔧 Requirements

- Bash shell (Linux, macOS, WSL, or Git Bash on Windows)
- `curl` installed
- A valid Mailchimp API key

---

## 🧰 Usage

### 1. 🔑 Find Your Mailchimp API Key

Log into Mailchimp, go to: Account > Extras > API Keys

Copy your API key (format: `1234567890abcdef-us20`).

### 2. 🌐 Identify Your Data Center

Your data center is the part **after the dash** in your API key.

For example:

| API Key | Data Center |
|---------|-------------|
| `abc123-us20` | `us20` |
| `xyz456-us5`  | `us5`  |

### 3. 🌀 Run the Script
bash
`curl -s -X GET "https://<dc>.api.mailchimp.com/3.0/lists" \
  -u "anystring:<your_api_key>"`

Replace:
	•	<dc> with your data center (e.g., us20)
	•	<your_api_key> with your actual Mailchimp API key

 📤 Output

The command returns a JSON response like:
{
  "lists": [
    {
      "id": "f2c123abc1",
      "name": "Main Newsletter"
    },
    {
      "id": "a6b789xyz3",
      "name": "VIP Contacts"
    }
  ]
}

You can then use the id for further API operations like adding subscribers, updating members, etc.
