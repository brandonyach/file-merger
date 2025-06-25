Security Plan for File Merger Tool
Overview
The File Merger Tool is a Streamlit web application for merging two files (CSV or Excel) based on user-selected columns. It is designed to handle potentially sensitive data (e.g., employee or customer records) securely.
Security Measures
Data Handling

No Persistent Storage: Files are processed in memory and not saved to disk.
Encryption in Transit: Deployment will use HTTPS (e.g., via Nginx or cloud provider certificates).
Minimal Data Exposure: Users select only necessary columns from File 2, reducing output data.

Authentication

Planned Integration: Support for SSO (e.g., Okta, Azure AD) using streamlit-authenticator or similar.
Access Control: Role-based access to restrict usage to authorized team members.

Deployment

Recommended Hosting: Internal company server or secure cloud (e.g., AWS EC2 in a VPC, Azure App Service).
Network Security: Restrict access to company VPN or trusted IP ranges.
Containerization: Docker ensures consistent, isolated environments.

Logging

Audit Trail: Log user actions (e.g., file uploads, merges) to a secure location (e.g., AWS CloudWatch).
No Sensitive Data in Logs: Exclude file contents from logs.

Compliance

Data Protection: Aligns with GDPR/HIPAA (if applicable) by minimizing data retention and securing transmission.
IT Collaboration: Configurable to meet company security policies (e.g., encryption standards, audit requirements).

Next Steps

Collaborate with IT to select hosting platform and authentication method.
Implement logging and access controls per company standards.
Conduct a security review before production deployment.

