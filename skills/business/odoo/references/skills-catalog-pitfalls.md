# Odoo Skills Catalog Pitfalls

## Common Issues and Solutions

### Empty Skills List
**Problem**: The skills catalog appears empty when queried via `skills_list`, but skills can still be loaded individually with `skill_view(name)` and used immediately.

**Solution**: Don't rely on `skills_list` for workflow. Use `skill_view(name)` to load specific skills when needed.

### Authentication Issues
**Problem**: `NOT_CONFIGURED` or `AUTH_FAILED` errors when using Odoo skills.

**Solution**: 
1. Run `python scripts/setup.py --check` to verify credentials
2. If `NOT_CONFIGURED`, run `python scripts/setup.py --store <url> <db> <user> <password>`
3. Verify with `ODOO check` before using any Odoo skill

### Module vs Model Confusion
**Problem**: Some modules (Project, Timesheets, etc.) use the generic `model` subcommand instead of module-specific subcommands.

**Solution**: 
- Use module-specific subcommands when available (e.g., `odoo-crm crm`)
- Fall back to `model` subcommand for modules that don't have dedicated commands
- Check the module-specific skill for domain-specific operations

### Permission Issues
**Problem**: `Access Denied` errors when performing operations.

**Solution**: Verify the user has appropriate permissions for the requested operation/model. The configured user may need elevated privileges for certain operations.

### Connection Problems
**Problem**: `CONNECTION_FAILED` errors.

**Solution**: 
- Check that the Odoo URL is reachable and the port is correct
- Verify firewall settings allow connections to the Odoo instance
- Ensure the database name exists and is accessible

### Data Validation
**Problem**: `Missing required field` errors.

**Solution**: Check `ODOO model <model> fields` for required fields before creating/updating records.

### Record Dependencies
**Problem**: `You cannot delete a record` errors.

**Solution**: Remove dependencies first. Records referenced by other records cannot be deleted until those dependencies are removed.

### Server Processing
**Problem**: `current transaction is aborted` errors.

**Solution**: The server is processing a scheduled action; wait a few seconds and retry the operation.

## Debugging Workflow

1. **Check Setup**: Always run `ODOO check` first
2. **Verify Module**: Use `python scripts/odoo_api.py --help` to see available commands
3. **Test Simple**: Start with a basic `ODOO model res.partner search` to test connectivity
4. **Check Logs**: Enable debug mode with `ODOO --debug` for detailed error information
5. **Validate Input**: Use `ODOO model <model> fields` to understand required fields

## Best Practices

- Always confirm destructive actions before execution
- Use the appropriate module-specific skill for domain-aware operations
- Present data as tables for better readability
- Handle API errors gracefully and provide user-friendly explanations
- Use named flags when available over raw domain filters
- Verify credentials before each session involving Odoo