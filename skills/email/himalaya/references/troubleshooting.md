# Himalaya Troubleshooting Guide

## Authentication Issues

### "Invalid credentials (Failure)"
- **Cause**: Wrong password or using regular password instead of App Password for Gmail
- **Fix**: Generate an App Password from Google Account settings (2-step verification required)
- **Example**: Use `auth.cmd = "pass show email/imap"` with password manager

### "Cannot build IMAP client"
- **Cause**: Authentication failure or network connectivity issues
- **Fix**: Test connection with `himalaya account doctor <account>`
- **Debug**: Run with `RUST_LOG=debug himalaya envelope list`

## Folder Configuration Issues

### "Folder doesn't exist" error
- **Cause**: Incorrect folder alias syntax for Gmail
- **Fix**: Use Gmail-specific folder names with `[Gmail]/` prefix
- **Correct aliases**:
  ```toml
  folder.aliases.inbox = "INBOX"
  folder.aliases.sent = "[Gmail]/Sent Mail"
  folder.aliases.drafts = "[Gmail]/Drafts"
  folder.aliases.trash = "[Gmail]/Trash"
  ```

### "Cannot resolve IMAP task"
- **Cause**: Gmail-specific folder naming requirements
- **Fix**: Ensure folder aliases match Gmail's exact naming scheme
- **Note**: v1.2.0+ requires `folder.aliases.X` syntax, not singular `alias`

## Connection Issues

### Connection refused to localhost:993/587
- **Cause**: IMAP/SMTP services not running or firewall blocking
- **Fix**: Verify IMAP/SMTP services are enabled in your email client
- **Test**: Try connecting with a regular email client first

### Network connectivity problems
- **Cause**: ISP blocking, DNS issues, or network restrictions
- **Fix**: Test with different network or check firewall settings
- **Debug**: Use `curl imap://imap.gmail.com:993` to test connectivity

## Password Security

### Best Practices
- Never hardcode passwords in configuration files
- Use password managers: `auth.cmd = "pass show email/imap"`
- For Gmail: Generate App Passwords instead of using regular passwords
- Consider environment variables: `auth.cmd = "echo $EMAIL_PASSWORD"`

### Configuration Examples
```toml
# Password manager integration
auth.cmd = "pass show email/imap"

# Environment variable
auth.cmd = "echo $GMAIL_PASSWORD"

# Script-based authentication
auth.cmd = "/usr/local/bin/get_password.sh email/imap"
```

## Debug Commands

### Enable debug logging
```bash
RUST_LOG=debug himalaya envelope list
```

### Full trace with backtrace
```bash
RUST_LOG=trace RUST_BACKTRACE=1 himalaya envelope list
```

### Verify account configuration
```bash
himalaya account doctor <account>
```

### Test connectivity
```bash
himalaya account doctor <account> --fix
```

## Gmail Specific Notes

- Always use App Passwords for authentication
- Folder names must include `[Gmail]/` prefix
- Enable 2-factor authentication before generating App Passwords
- Test with a simple email client first to verify account works

## Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| "Invalid credentials" | Wrong password/App Password | Generate new App Password |
| "Folder doesn't exist" | Incorrect folder alias | Use `[Gmail]/` prefix for Gmail |
| "Cannot build IMAP client" | Auth failure/network | Check credentials and connectivity |
| "Connection refused" | Service not running | Enable IMAP/SMTP in email client |
| "Unexpected NO response" | Server-side issue | Wait and retry, check Gmail status |