# Telegram Remote Administration Bot

A lightweight Telegram bot that allows you to remotely monitor and control your own Windows computer from anywhere.

This project started as a way to remotely check on my PC while away from home, but has since grown into a fully fletched remote administration tool with live shell access, system monitoring, screenshots and more to come. why? cuz i was bored

> ⚠️ This project is intended for **personal use on machines you own or are explicitly authorized to administer.**

---

## Features

### System Monitoring

- CPU usage
- RAM usage
- GPU usage
- Disk usage
- System uptime
- Interactive status refresh buttons

### Remote Shell

- Execute shell commands remotely
- Persistent shell sessions
- Live command output streaming
- Working directory persists between commands

### Remote Desktop

- Capture desktop screenshots
- Continuous screenshot watcher
- Adjustable capture interval
- JPEG compression for fast uploads

### Power Management

- Shutdown
- Restart
- Lock workstation

### Process Management *(planned)*

- List running processes
- Kill processes
- Start applications

### Notifications *(planned)*

- Battery events
- Charger connected/disconnected
- High CPU usage
- High GPU temperature
- Custom alert thresholds

  
## Example Commands

```text
/status
```

Display current system information.

```text
/shell start
```

Start a persistent shell session.

```text
/shell dir
```

Execute a command.

```text
/screenshot
```

Capture and send the current desktop.

```text
/watch 10
```

Receive a screenshot every 10 seconds.

```text
/restart
```

Restart the computer.

```text
/shutdown
```

Power off the computer.

```text
/lock
```

Lock the workstation.

---

## How It Works

The bot runs locally on the target computer and communicates through the Telegram Bot API. Since all commands are initiated from Telegram, no ports need to be opened or forwarded. think of it as kind of a better SSH session but through telegram.

---

### How to use properly:
 
Go to @BotFather on telegram and create a bot, copy the token (if you want you can also set bot commands). put the token in the ```secrets.env``` file in the ```TOKEN``` variable. also get your numerical telegram id (with @userinfobot) and put it in the ```OWNER_ID``` variable in ```secrets.env```. its a list so you can whitelist multiple users to use the bot. 

---

## Security

This bot is designed for personal use. don't even think about using this as a backdoor RAT on other people's computers. if anyone does, i am not responsible in any shape or form.

some recommendations:

- Restrict access to your Telegram user ID.
- Review shell commands carefully before executing them.

---

## Roadmap

- [x] System monitoring
- [x] Screenshot capture
- [x] Screenshot watcher
- [x] Remote shell
- [x] Persistent shell sessions
- [x] Power controls
- [ ] Process manager
- [ ] File explorer
- [ ] Notification system
- [ ] Service manager
- [ ] Clipboard support
