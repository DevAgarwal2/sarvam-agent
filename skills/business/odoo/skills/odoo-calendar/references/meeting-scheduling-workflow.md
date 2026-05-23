# Meeting Scheduling Workflow

## Task: Schedule meeting for tomorrow at 11 AM

### Commands Used:
```bash
# Create calendar event for meeting with Suresh Mehta
python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py calendar create-event --name "Meeting with Suresh Mehta" --start "2026-05-24 11:00:00" --stop "2026-05-24 12:00:00" --partner-ids "[6]"
```

### Key Patterns:
- Date format: YYYY-MM-DD HH:MM:SS
- Duration: 1 hour (11:00-12:00)
- Partner IDs: JSON array format [6]
- Event name should be descriptive
- Include relevant partners as attendees