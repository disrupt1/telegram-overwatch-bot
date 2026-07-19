# Telegram Remote Administration Bot

A lightweight Telegram bot that allows you to remotely monitor and control your own Windows computer from anywhere.

This project started as a way to remotely check on my PC while away, but has since grown into a full-featured remote administration tool with live shell access, system monitoring, screenshots, process management, and more.

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

### File Management *(planned)*

- Browse directories
- Upload files
- Download files
- Delete files

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

The bot runs locally on the target computer and communicates through the Telegram Bot API. Since all commands are initiated from Telegram, no ports need to be opened or forwarded.

Long-running tasks such as monitoring and screenshot watching are handled asynchronously using `asyncio` and the built-in JobQueue provided by `python-telegram-bot`.

---

## Security

This bot is designed for personal use.

Some recommendations:

- Never commit your bot token.
- Store secrets in environment variables.
- Restrict access to your Telegram user ID.
- Consider adding a whitelist for authorized users.
- Review shell commands carefully before executing them.

---

## Roadmap

- [x] System monitoring
- [x] Screenshot capture
- [x] Screenshot watcher
- [x] Remote shell
- [x] Persistent shell sessions
- [ ] Power controls
- [ ] Process manager
- [ ] File explorer
- [ ] Notification system
- [ ] Service manager
- [ ] Clipboard support
- [ ] Multi-user support
- [ ] Plugin system

---

## License

MIT License
