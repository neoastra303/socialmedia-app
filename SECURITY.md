# Security Policy

## Supported Versions

We support security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | ✅ Yes             |
| < 1.0   | ❌ No              |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it to us responsibly.

**Do not report security vulnerabilities through public GitHub issues.**

Instead, please email us at [your-security-email@example.com](mailto:your-security-email@example.com) with the following information:

- A description of the vulnerability
- Steps to reproduce the issue
- Potential impact of the vulnerability
- Any possible mitigations

### What to Expect

- **Acknowledgment**: Within 48 hours of your report
- **Status Updates**: Every 7 days until resolution
- **Resolution Timeline**: Within 30 days, depending on severity

## Security Best Practices

### For Users
- Use strong, unique passwords
- Enable two-factor authentication when available
- Keep your application updated
- Review connected applications and services regularly

### For Developers
- Validate and sanitize all user inputs
- Use parameterized queries to prevent SQL injection
- Implement proper authorization checks
- Follow the principle of least privilege
- Regular security audits and testing

## Security Features

This application includes several security features:

- **Rate Limiting**: Protection against brute force and DoS attacks
- **File Validation**: Secure file type and size validation
- **CSRF Protection**: Built-in Django CSRF protection
- **XSS Prevention**: Automatic template escaping
- **SQL Injection Prevention**: ORM-based queries
- **Authentication**: Secure user authentication system

## Dependencies Security

We maintain security by:
- Regularly updating dependencies
- Using tools like `pip-audit` to check for vulnerabilities
- Following security best practices in dependency usage

## Security Headers

The application implements the following security headers:
- HTTP Strict Transport Security (HSTS)
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection

For production deployments, additional security headers should be configured.