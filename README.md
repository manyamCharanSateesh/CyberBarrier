# 🛡️ CyberBarrier

### A Lightweight Website Blocking & Digital Safety Tool

**CyberBarrier** is a Python-based website blocking application designed to provide users with simple and direct control over websites that can be accessed on their system.

The application works by managing the operating system's **hosts file**, redirecting blocked domains to the local machine instead of allowing them to resolve normally.

It provides a simple interface for:

* 🚫 Blocking websites
* ✅ Unblocking websites
* 📋 Viewing currently blocked websites
* 🔄 Synchronizing blocked websites from a server
* 🌐 Handling common alternative domains
* 🧹 Flushing the DNS cache after changes

---

## 🚀 Features

### 🚫 Website Blocking

Users can enter a website or domain and block it directly.

For example:

```text
youtube.com
instagram.com
facebook.com
```

CyberBarrier adds the required domain entries to the system hosts file and redirects them to:

```text
127.0.0.1
```

and:

```text
::1
```

This prevents the specified domains from resolving normally.

---

### 🔓 Website Unblocking

Blocked websites can be removed from the hosts file through the application.

The application identifies the relevant domain entries and removes them while preserving unrelated hosts-file entries.

---

### 📋 Blocked Website Management

CyberBarrier reads the system hosts file and displays domains currently redirected to the local machine.

The interface provides a list of active blocks and allows individual websites to be unblocked.

---

### 🌐 Alternative Domain Handling

CyberBarrier includes mappings for common alternative domains.

Currently supported mappings include:

```text
YouTube
 ├── youtube.com
 ├── youtu.be
 ├── m.youtube.com
 └── music.youtube.com

Facebook
 ├── facebook.com
 ├── fb.com
 └── m.facebook.com

Twitter / X
 ├── twitter.com
 ├── t.co
 └── x.com

Instagram
 ├── instagram.com
 └── instagr.am

Reddit
 ├── reddit.com
 ├── redd.it
 └── old.reddit.com

LinkedIn
 ├── linkedin.com
 └── lnkd.in
```

This allows the application to account for commonly associated domains when blocking a supported website.

---

### 🔄 Server Synchronization

The application includes a synchronization feature that accepts a server URL and retrieves additional blocked-site information.

The mobile interface provides a:

```text
Server IP:8000
```

input field and a **SYNC** button for this purpose.

---

### 🧹 DNS Cache Flush

After modifying the hosts file, CyberBarrier attempts to flush the Windows DNS cache using:

```bash
ipconfig /flushdns
```

This helps apply host-resolution changes without waiting for the existing DNS cache to expire.

---

## 🏗️ Architecture

```text
                 ┌─────────────────────┐
                 │        User         │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   CyberBarrier UI   │
                 │   Python Interface  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  BlockerManager     │
                 │                     │
                 │ • Block Website     │
                 │ • Unblock Website   │
                 │ • Read Blocks       │
                 │ • Sync Blocks       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Hosts File       │
                 │                     │
                 │ 127.0.0.1 domain    │
                 │ ::1 domain           │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    DNS Resolution   │
                 │    / DNS Flush      │
                 └─────────────────────┘
```

---

## 🔧 How It Works

CyberBarrier follows a straightforward workflow:

```text
User enters website
        ↓
Hostname extraction
        ↓
Check supported alternative domains
        ↓
Add domain to hosts file
        ↓
127.0.0.1 / ::1 redirection
        ↓
Flush DNS cache
        ↓
Website becomes blocked
```

For unblocking:

```text
User selects blocked website
        ↓
Identify domain entries
        ↓
Remove matching hosts-file entries
        ↓
Flush DNS cache
        ↓
Website becomes accessible again
```

The core implementation is contained in `blocker_manager.py`.

---

## 🛠️ Technology Stack

| Technology                | Purpose                                 |
| ------------------------- | --------------------------------------- |
| 🐍 Python                 | Core application logic                  |
| 🎨 CustomTkinter          | Desktop UI dependency                   |
| 📱 Kivy                   | Mobile-style interface                  |
| 🌐 Hosts File             | Website blocking mechanism              |
| 🖥️ Windows APIs/Commands | System-level configuration              |
| 🔄 HTTP Synchronization   | Server-based block-list synchronization |
| 📦 Packaging              | Executable distribution                 |

The repository's `requirements.txt` currently specifies **CustomTkinter** and **packaging**.

---

## 📂 Project Structure

```text
CyberBarrier/
│
├── .github/
│   └── workflows/
│
├── CyberBarrier1.exe
│
├── main.py
│
├── blocker_manager.py
│
├── requirements.txt
│
└── README.md
```

### `main.py`

Provides the application interface and connects the UI to the blocking functionality.

The current implementation creates the **CyberBarrier Mobile** interface with:

* Website input
* BLOCK button
* Server synchronization input
* SYNC button
* Status display
* Blocked-sites list
* Unblock controls

### `blocker_manager.py`

Contains the main website-blocking logic.

Responsibilities include:

* Reading the hosts file
* Extracting hostnames
* Blocking domains
* Unblocking domains
* Handling alternative domains
* Writing hosts-file entries
* Flushing DNS cache

### `CyberBarrier1.exe`

A packaged executable is included in the repository for convenient Windows execution.

---

# ⚙️ Installation

## Prerequisites

* Windows 10/11
* Python 3.x
* Administrator privileges for hosts-file modification
* Git

---

## 1. Clone the Repository

```bash
git clone https://github.com/manyamCharanSateesh/CyberBarrier.git
```

```bash
cd CyberBarrier
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

The current repository requirements include:

```text
customtkinter
packaging
```

---

## 3. Run as Administrator

Because CyberBarrier modifies the system hosts file, administrator privileges may be required.

Open **Command Prompt / PowerShell as Administrator** and run:

```bash
python main.py
```

---

# 🖥️ Windows Hosts File

On Windows, CyberBarrier works with:

```text
C:\Windows\System32\drivers\etc\hosts
```

The application detects the operating system and uses the appropriate hosts-file path.

A blocked domain may appear in the hosts file as:

```text
127.0.0.1 example.com
::1 example.com
```

This redirects the domain to the local machine.

---

# 🔐 Permissions

CyberBarrier requires elevated permissions when it needs to modify the hosts file.

If permission is denied, the application reports that it should be run with administrator privileges.

> ⚠️ Only modify your own computer's hosts file or systems for which you have authorization.

---

# 📱 Interface

The current application interface contains:

```text
┌────────────────────────────────────┐
│           CyberBarrier             │
├────────────────────────────────────┤
│ example.com             [ BLOCK ]  │
├────────────────────────────────────┤
│ Server IP:8000             [ SYNC ]│
├────────────────────────────────────┤
│ Status: Ready                      │
├────────────────────────────────────┤
│          Blocked Sites             │
│                                    │
│ youtube.com                  [ X ] │
│ instagram.com                [ X ] │
│ facebook.com                 [ X ] │
│                                    │
└────────────────────────────────────┘
```

The implementation uses Kivy widgets such as `BoxLayout`, `Label`, `TextInput`, `Button`, `ScrollView`, and `GridLayout` for the interface.

---

# 🔄 Server Sync

CyberBarrier includes a synchronization workflow:

```text
CyberBarrier Client
        │
        │ SYNC
        ▼
   Server URL
        │
        ▼
Fetch Block List
        │
        ▼
Add New Blocks
        │
        ▼
Refresh Blocked Sites
```

The synchronization operation runs in a separate thread so the UI does not remain blocked while the request is being processed.

---

# 🎯 Use Cases

CyberBarrier can be used for:

* 🧑‍🎓 Student digital-discipline environments
* 👨‍👩‍👧 Controlled family devices
* 🏢 Organization-managed systems
* 🧪 Cybersecurity learning
* 💻 Personal website-access control
* 🔐 Basic endpoint-level web restriction

---

# 🛡️ Security & Privacy

CyberBarrier operates locally by modifying the system's hosts file.

The project does not require a browser extension to perform its basic blocking function.

Important considerations:

* Run the application only on systems you control.
* Protect administrator privileges.
* Review the hosts file before and after making changes.
* Do not use the synchronization functionality with an untrusted server.
* Keep backups of important system configuration files.

---

# ⚠️ Limitations

The current implementation relies on hosts-file based blocking.

Therefore, it is not intended to replace:

* Enterprise firewalls
* DNS security systems
* Network intrusion-prevention systems
* Full parental-control platforms
* Endpoint Detection and Response (EDR)
* Enterprise web-filtering solutions

Hosts-file blocking also depends on domain-based resolution and may not cover every possible way a service can be accessed.

---

# 🔮 Future Enhancements

Potential improvements include:

* 🌐 Centralized web-based administration
* 👥 User profiles
* ⏰ Scheduled website blocking
* 📊 Usage statistics
* 🔐 Password-protected administrator mode
* 📋 Custom block lists
* 🗂️ Website categories
* 🔄 Improved server synchronization
* 📱 Improved Android deployment
* 🖥️ Enhanced Windows desktop interface
* 📈 Activity and blocking reports
* 🔔 Notifications
* ☁️ Cloud-based block-list management

---

# 📌 Project Status

**CyberBarrier is an actively developed prototype.**

The current repository contains a working Python-based website blocking implementation with hosts-file management and synchronization functionality.

---

# 👨‍💻 Author

**Manyam Charan Sateesh**

GitHub:

[Manyam Charan Sateesh — GitHub](https://github.com/manyamCharanSateesh?utm_source=chatgpt.com)

Project:

[CyberBarrier Repository](https://github.com/manyamCharanSateesh/CyberBarrier?utm_source=chatgpt.com)

---

# 📜 License

This project is intended for **educational, research, and authorized personal-use purposes**.

---

## 🛡️ CyberBarrier

> **Control access. Protect users. Build safer digital environments.**
