# Himalaya Configuration Guide

## Basic Configuration Structure

```toml
[accounts.personal]
email = "you@example.com"
display-name = "Your Name"
default = true

[accounts.personal.backend]
type = "imap"
host = "imap.example.com"
port = 993
encryption.type = "tls"
login = "you@example.com"
auth.type = "password"
auth.cmd = "pass show email/imap"  # Secure password retrieval

[accounts.personal.message.send.backend]
type = "smtp"
host = "smtp.example.com"
port = 587
encryption.type = "start-tls"
login = "you@example.com"
auth.type = "password"
auth.cmd = "pass show email/smtp"

[accounts.personal.folder.aliases]
inbox = "INBOX"
sent = "Sent Mail"
drafts = "Drafts"
trash = "Trash"
```

## Gmail-Specific Configuration

```toml
[accounts.gmail]
email = "your.email@gmail.com"
display-name = "Your Name"
default = true

[accounts.gmail.backend]
type = "imap"
host = "imap.gmail.com"
port = 993
encryption.type = "tls"
login = "your.email@gmail.com"
auth.type = "password"
auth.cmd = "pass show gmail/imap"  # Use App Password

[accounts.gmail.message.send.backend]
type = "smtp"
host = "smtp.gmail.com"
port = 587
encryption.type = "start-tls"
login = "your.email@gmail.com"
auth.type = "password"
auth.cmd = "pass show gmail/smtp"

[accounts.gmail.folder.aliases]
inbox = "INBOX"
sent = "[Gmail]/Sent Mail"  # Gmail uses special naming
drafts = "[Gmail]/Drafts"
trash = "[Gmail]/Trash"
```

## Authentication Methods

### Password Manager (Recommended)
```toml
auth.cmd = "pass show email/imap"
```

### Environment Variable
```toml
auth.cmd = "echo $EMAIL_PASSWORD"
```

### Script-based
```toml
auth.cmd = "/usr/local/bin/get_password.sh imap"
```

## Common Issues and Solutions

### Folder Alias Problems
- **Issue**: "Folder doesn't exist" errors
- **Solution**: Use Gmail's special folder naming with `[Gmail]/` prefix
- **Example**: `sent = "[Gmail]/Sent Mail"` not `sent = "Sent Mail"`

### Authentication Failures
- **Issue**: "Invalid credentials" errors
- **Solution**: Use App Passwords for Gmail, not regular passwords
- **Setup**: Enable 2FA, generate App Password in Google Account settings

### Connection Issues
- **Issue**: "Connection refused" to IMAP/SMTP servers
- **Solution**: Verify IMAP/SMTP are enabled in your email client
- **Test**: Try connecting with a regular email client first

## Security Best Practices

1. **Never hardcode passwords** in configuration files
2. **Use password managers** for credential storage
3. **Enable 2FA** for all email accounts
4. **Use App Passwords** instead of regular passwords
5. **Regularly rotate** credentials
6. **Limit access** to configuration files

## Testing Configuration

### Verify Account Setup
```bash
himalaya account doctor <account-name>
```

### Test IMAP Connection
```bash
himalaya account doctor <account-name> --fix
```

### Test Email Sending
```bash
echo "Test message" | himalaya template send
```

## Migration Notes

### From Older Versions
- v1.2.0+ requires `folder.aliases.X` syntax (plural)
- Old `[accounts.NAME.folder.alias]` syntax is ignored
- Update configuration files accordingly

### Multiple Accounts
```toml
[accounts.work]
email = "work@company.com"
default = false

[accounts.personal]
email = "personal@gmail.com"
default = true
```

## Debug Configuration

Enable debug logging:
```bash
RUST_LOG=debug himalaya envelope list
```

Full trace with backtrace:
```bash
RUST_LOG=trace RUST_BACKTRACE=1 himalaya envelope list
```