# Gmail Setup Guide for Himalaya

## Prerequisites

1. **Enable 2-Factor Authentication** on your Google Account
2. **Generate App Password** for Himalaya access
3. **Configure Himalaya** with proper folder aliases

## Step 1: Generate App Password

1. Go to your Google Account: https://myaccount.google.com/
2. Navigate to **Security**
3. Ensure **2-Step Verification** is enabled
4. Click on **App passwords** under "Signing in to Google"
5. Generate new password:
   - Select "Mail" for the app
   - Select "Other (Custom name)" and name it "Himalaya"
   - Click "Generate"
   - Copy the 16-character password

## Step 2: Update Himalaya Configuration

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
auth.cmd = "echo 'YOUR_16_CHAR_APP_PASSWORD'"

[accounts.gmail.message.send.backend]
type = "smtp"
host = "smtp.gmail.com"
port = 587
encryption.type = "start-tls"
login = "your.email@gmail.com"
auth.type = "password"
auth.cmd = "echo 'YOUR_16_CHAR_APP_PASSWORD'"

[accounts.gmail.folder.aliases]
inbox = "INBOX"
sent = "[Gmail]/Sent Mail"
drafts = "[Gmail]/Drafts"
trash = "[Gmail]/Trash"
```

## Step 3: Test Configuration

```bash
# Test account connectivity
himalaya account doctor gmail

# Test folder access
himalaya folder list

# Test email sending
echo "Test message" | himalaya template send
```

## Important Notes

- **Never use your regular Gmail password** - always use App Passwords
- **App Passwords are specific** to the app and device
- **16-character passwords** are one-time use
- **Rotate App Passwords** regularly for security
- **Gmail folder naming** requires `[Gmail]/` prefix for folders

## Common Gmail Issues

### "Invalid credentials"
- **Fix**: Generate new App Password, ensure using 16-character password
- **Check**: 2-step verification is enabled

### "Folder doesn't exist"
- **Fix**: Use correct Gmail folder naming with `[Gmail]/` prefix
- **Example**: `[Gmail]/Sent Mail` not `Sent Mail`

### Connection timeouts
- **Fix**: Check network connectivity, try different network
- **Test**: Connect with regular email client first

## Security Recommendations

1. **Use password manager** instead of hardcoded App Password
2. **Limit App Password usage** to Himalaya only
3. **Monitor account activity** for unauthorized access
4. **Use separate Gmail account** for business automation
5. **Regularly review** connected apps in Google Account settings

## Troubleshooting Gmail

### Debug Mode
```bash
RUST_LOG=debug himalaya envelope list
```

### Account Doctor
```bash
himalaya account doctor gmail --fix
```

### Reset Configuration
```bash
rm ~/.config/himalaya/config.toml
himalaya account configure gmail
```