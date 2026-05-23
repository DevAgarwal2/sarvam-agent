# Invoice PDF Download via Curl

## Command
```bash
curl -L -o invoice.pdf "http://host.docker.internal:8069/my/invoices/11?access_token=TOKEN&download=1"
```

## Steps
1. Get portal URL: `ODOO model account.move call get_portal_url --method-args '[11]'`
2. Extract the URL and access token
3. Use curl with `&download=1` parameter for direct PDF download
4. Save to file with `-o invoice.pdf`

## Notes
- Portal URL format: `/my/invoices/{id}?access_token={generated_token}`
- Add `&download=1` parameter for direct PDF download
- Requires proper authentication token
- Works for posted invoices only