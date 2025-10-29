# SOAR Platform Architecture and Integration

## Executive Summary

The SOAR (Security Orchestration, Automation and Response) platform integrates SIEM tools, Threat Intelligence feeds, and vulnerability scanners through specialized TIP and CSAM services. The platform provides centralized orchestration, automated workflows, and unified dashboards for comprehensive security operations.

---

## Platform Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    SOAR Core Platform                           │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐    │
│  │ SOAR        │  │ Playbook     │  │ Unified Dashboard   │    │
│  │ Platform    │  │ Engine       │  │ Security Operations │    │
│  │ Port: 443   │  │ Automated    │  │                     │    │
│  │ MongoDB     │  │ Workflows    │  │                     │    │
│  └─────────────┘  └──────────────┘  └─────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
           │                                          │
           │ HTTPS                           HTTPS    │
           │ tipHost:7000                csamHost:8229│
           ▼                                          ▼
┌─────────────────────┐                  ┌─────────────────────┐
│  TIP Service        │                  │  CSAM Service       │
│  Port 7000          │                  │  Port 8229          │
│  ┌───────────────┐  │                  │  ┌───────────────┐  │
│  │ TIP REST API  │  │                  │  │ CSAM REST API │  │
│  │ zona_tip_batch│  │                  │  │ securaa_csam  │  │
│  └───────────────┘  │                  │  └───────────────┘  │
│  ┌───────────────┐  │                  │  ┌───────────────┐  │
│  │ Elasticsearch │  │                  │  │ Elasticsearch │  │
│  │ Threat Intel  │  │                  │  │ Asset & Vuln  │  │
│  │ Database      │  │                  │  │ Database      │  │
│  └───────────────┘  │                  │  └───────────────┘  │
└─────────────────────┘                  └─────────────────────┘
           ▲                                          ▲
           │                                          │
┌─────────────────────┐                  ┌─────────────────────┐
│ TI Feed Sources     │                  │ Vulnerability       │
│ • Recorded Future   │                  │ Scanners           │
│ • MISP Platform     │                  │ • Nessus           │
│ • Abuse.ch         │                  │ • Qualys           │
│ • Bambenek         │                  │ • Cloud Scanners   │
└─────────────────────┘                  └─────────────────────┘

           External Integrations
┌─────────────────────────────────────────────────────────────────┐
│ SIEM Tools: Graylog, Elastic Security, QRadar, Splunk, Sentinel │
└─────────────────────────────────────────────────────────────────┘
```

### Core Components

| Component | Port | Database | Purpose |
|-----------|------|----------|---------|
| **SOAR Platform** | 443 | MongoDB | Central orchestration and case management |
| **TIP Service** | 7000 | Elasticsearch | Threat intelligence processing |
| **CSAM Service** | 8229 | Elasticsearch | Asset and vulnerability management |

---

## SIEM Integration

### Supported SIEM Platforms

**Enterprise SIEM Solutions:**
- **Graylog** - Open-source log management and analysis
- **Elastic Security** - Elasticsearch-based security analytics  
- **IBM QRadar** - Enterprise SIEM with threat detection
- **Splunk** - Data platform for security monitoring
- **Microsoft Sentinel** - Cloud-native SIEM solution
- **ArcSight ESM** - Enterprise security management
- **LogRhythm** - Unified security analytics platform

**Integration Methods:**
- REST API connections
- Webhook notifications
- Log forwarding (Syslog)
- Database connections

### SIEM Data Processing

```
SIEM Platform → Security Alert/Event → SOAR Platform
                                          ↓
                                   Create Incident
                                          ↓
                              Query TIP Service (Port 7000)
                                          ↓
                                  Threat Enrichment
                                          ↓
                                Execute Playbook
                                          ↓
                            Prioritized Alert → Analyst
```

---

## Threat Intelligence Feeds

### TI Feed Sources

**Commercial Feeds:**
- **Recorded Future** - Commercial threat intelligence and IOCs
- **ThreatMon** - Real-time threat feeds and analysis

**Open Source Feeds:**
- **MISP Platform** - Community threat sharing
- **Abuse.ch** - Malware and botnet feeds
- **Bambenek** - Domain and IP intelligence  
- **Blocklist.de** - Attack source tracking
- **Firebog** - DNS blocking lists
- **BotScout** - Bot and spam detection

### TI Processing Architecture

```
TI Feed Sources → Data Normalizer → Elasticsearch Storage → TIP REST API
                                                                ↓
                                                        SOAR Integration
```

### Indicator Types Supported

| Type | Description | Primary Sources |
|------|-------------|-----------------|
| **IP Addresses** | Malicious IPs, C2 servers | Recorded Future, Abuse.ch |
| **Domain Names** | Malicious domains, DGA | MISP, Bambenek |
| **URLs** | Malicious URLs, phishing | Recorded Future, Firebog |
| **File Hashes** | Malware signatures | MISP, Abuse.ch |
| **Email Addresses** | Phishing sources | BotScout, MISP |

### TIP Service API

| Endpoint | Method | Purpose |
|----------|---------|---------|
| `/search/{userid}/{indicator}/{tiptype}/` | GET | Search threat indicators |
| `/datalist/` | POST | Retrieve indicator data |
| `/importindicators/` | POST | Import custom indicators |
| `/exportindicator/` | POST | Export threat data |

---

## Vulnerability Management

### CSAM Service Integration

**Vulnerability Scanners:**
- **Nessus** - Tenable vulnerability scanner
- **Qualys VMDR** - Cloud-based scanning
- **OpenVAS** - Open-source scanner
- **Rapid7 InsightVM** - Real-time scanning

**Cloud Platforms:**
- **AWS Security** - Config, Inspector, GuardDuty
- **Azure Security** - Security Center, Defender
- **GCP Security** - Security Command Center

### Asset Management Features

```
Cloud Platforms → Asset Discovery → CSAM Service (Port 8229)
                                          ↓
Vulnerability     → Risk Assessment → Elasticsearch Storage
Scanners                                  ↓
                                   Dashboard APIs
                                          ↓
                                  SOAR Integration
```

**Key Capabilities:**
- Asset inventory and tracking
- Vulnerability risk scoring (CVSS)
- Patch management tracking
- Compliance reporting

### CSAM Service API

| Endpoint | Method | Purpose |
|----------|---------|---------|
| `/assets` | GET | Asset information |
| `/vulnerability-details/{cve-id}` | GET | CVE details |
| `/tasks/asset-info` | POST | Asset tasks |
| `/dashboarddata` | GET | Metrics and reports |

---

## Service Communication

### Integration Configuration

**Service Endpoints:**
```yaml
TIP_Service:
  host: "${tipHost}"
  port: 7000
  protocol: "HTTPS"

CSAM_Service:
  host: "${csamHost}"
  port: 8229
  protocol: "HTTPS"

SOAR_Platform:
  port: 443
  database: "MongoDB"
```

**Authentication:**
- HTTPS with TLS certificates
- Elasticsearch basic authentication
- API token-based security

### Data Flow Patterns

1. **Real-time Integration** - Webhook event notifications
2. **Scheduled Polling** - Periodic data synchronization  
3. **On-demand Queries** - User-initiated data retrieval
4. **Batch Processing** - Bulk data import operations

---

## Conclusion

The SOAR platform provides comprehensive security orchestration through:

- **Multi-SIEM Support** - Integration with leading SIEM platforms
- **Threat Intelligence** - Automated TI feed processing and correlation
- **Vulnerability Management** - Cloud-native asset and vulnerability tracking
- **Unified Operations** - Centralized dashboard and workflow automation

This architecture enables organizations to achieve integrated security operations with automated threat detection, investigation, and response capabilities.

*Document reflects actual implementation based on zona_tip_batch and securaa_csam codebase analysis.*