# 🚨 SECURITY INCIDENT RESPONSE PLAYBOOK
## Project Lessimp-Secure - CRITICAL Alert Response Protocol

**Version:** 1.0  
**Date:** February 1, 2026  
**Status:** OPERATIONAL  
**Classification:** INTERNAL USE - SECURITY OPERATIONS

---

## 📋 Executive Summary

This playbook defines the **Security Incident Response Protocol** for the Lessimp-Secure integration. It provides step-by-step procedures for investigating, validating, and responding to **CRITICAL Gmail alerts** triggered by unauthorized login attempts detected by the FinalLogic Python security analyzer.

---

## 🎯 Incident Scope

### What Triggers a CRITICAL Alert?

**FinalLogic Python Logic:**
```python
if username == "wipedclean" or current_hour == 9:
    status = "verified"
    alert_channel = "discord"  # Green notification only
else:
    status = "unauthorized"
    severity = "CRITICAL"
    alert_channel = "gmail"    # RED CRITICAL EMAIL
```

**Trigger Conditions:**
1. **User Validation Failure:** `username != "wipedclean"`
2. **Time Validation Failure:** `current_hour != 9`
3. **Both conditions must be FALSE** for CRITICAL alert

**Alert Destinations:**
- **Discord:** Red embed notification (immediate awareness)
- **Gmail:** HTML email to `info@lessimp.com` (CC: `wfrancois@lessimp.com`)

---

## 🔔 Alert Anatomy

### Gmail CRITICAL Incident Email

**From:** security@lessimp.com  
**To:** info@lessimp.com  
**CC:** wfrancois@lessimp.com  
**Subject:** 🚨 CRITICAL: Unauthorized Login Attempt - Lessimp Security Alert  
**Priority:** High (X-Priority: 1)

**Email Structure:**

```
┌─────────────────────────────────────────────────────────┐
│ 🚨 LESSIMP SECURITY INCIDENT ALERT                      │
│ [CRITICAL]                                              │ ← Red header
├─────────────────────────────────────────────────────────┤
│ ⚠️ WARNING: Automated security monitoring has detected  │
│ an unauthorized login attempt requiring immediate       │
│ investigation.                                          │
├─────────────────────────────────────────────────────────┤
│ INCIDENT DETAILS                                        │
│ ┌─────────────────────┬─────────────────────────────┐ │
│ │ User Identifier     │ intruder_hacker             │ │
│ │ Status              │ unauthorized                │ │
│ │ Timestamp           │ 2026-02-01T15:45:30         │ │
│ │ Test Case           │ TC001_SecureLogin           │ │
│ │ Phone Number        │ 5555559999                  │ │
│ │ Email Address       │ hacker@malicious.com        │ │
│ │ Hour of Attempt     │ 15                          │ │
│ │ Severity            │ CRITICAL                    │ │
│ └─────────────────────┴─────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│ IMMEDIATE ACTIONS REQUIRED                              │
│ ☑ Review Cerberus test execution logs                   │
│ ☑ Verify Firebase Authentication logs                   │
│ ☑ Check for unusual account activity                    │
│ ☑ Investigate source IP address                         │
│ ☑ Validate user identity claims                         │
│ ☑ Consider temporary account lockdown                   │
├─────────────────────────────────────────────────────────┤
│ [View Cerberus Logs] [View Firebase Logs]              │
└─────────────────────────────────────────────────────────┘
```

**8 Dynamic Fields (from FinalLogic output):**
1. **User Identifier:** Username detected in test execution
2. **Status:** "unauthorized" (hardcoded for CRITICAL path)
3. **Timestamp:** ISO 8601 format (e.g., 2026-02-01T15:45:30Z)
4. **Test Case:** "TC001_SecureLogin" (from Cerberus)
5. **Phone Number:** Phone number used in login attempt
6. **Email Address:** Email from Shuffle user credentials
7. **Hour:** Hour of day (0-23) when attempt occurred
8. **Severity:** "CRITICAL" (hardcoded for unauthorized path)

---

## 🚨 Incident Response Workflow

### Phase 1: Initial Alert Triage (0-2 minutes)

**When you receive the Gmail CRITICAL alert:**

#### Step 1: Acknowledge Receipt

**Action:** Reply to the alert email with acknowledgment.

**Template:**
```
Subject: RE: 🚨 CRITICAL: Unauthorized Login Attempt

Alert acknowledged by [Your Name] at [Current Time].
Beginning investigation per Security Incident Response Playbook.
Status: INVESTIGATING
```

---

#### Step 2: Verify Alert Authenticity

**Check Discord for Corresponding Red Notification:**

1. Open Discord channel (configured in Shuffle)
2. Look for red embed with same timestamp
3. Verify fields match Gmail email:
   - User Identifier
   - Phone Number
   - Timestamp

**If Discord notification is MISSING:**
- ⚠️ Possible false positive or routing error
- Proceed with caution
- Check Shuffle workflow execution logs

**If Discord notification is PRESENT:**
- ✅ Alert is authentic
- Proceed to forensic investigation

---

### Phase 2: Forensic Investigation (2-10 minutes)

#### Step 3: Extract Incident Details from Email

**Record the following from the 8-field incident table:**

| Field | Value | Notes |
|-------|-------|-------|
| User Identifier | _________________ | Who is claiming to be? |
| Phone Number | _________________ | Credentials used |
| Email Address | _________________ | Associated email |
| Timestamp | _________________ | When did it occur? |
| Hour | _________________ | Time-based validation |
| Test Case | _________________ | Should be TC001_SecureLogin |

---

#### Step 4: Access Cerberus Forensic Logs

**Navigate:** http://localhost:8888/TestCaseExecutionList.jsp

**Filter:**
- Test: `LoginTests`
- Test Case: `TC001_SecureLogin`
- Date: Match timestamp from email (e.g., 2026-02-01)
- Status: Any (even PASS - functional test may succeed)

**Find execution matching timestamp** (within 1-2 minutes of email timestamp)

**Click:** [View Details]

---

#### Step 5: Verify Step 6 Forensic Audit Trail

**Critical Step:** This is your primary evidence source!

**Navigate to Step 6 in execution log:**

1. Scroll to: **Step 6: Log test execution identity**
2. Look for: **Property: TEST_IDENTITY_LOG**
3. Expected format:
   ```
   Testing with: PHONE=5555559999, USER=Intruder Hacker, EMAIL=hacker@malicious.com, USER_ID=999
   ```

**Cross-Reference with Gmail Alert:**

| Gmail Field | Step 6 Value | Match? |
|-------------|--------------|--------|
| Phone Number | PHONE value | [ ] |
| Email Address | EMAIL value | [ ] |
| User Identifier | USER value | [ ] |

**If ALL match:**
- ✅ Forensic evidence validated
- ✅ Alert is confirmed accurate
- ✅ Proceed to impact assessment

**If ANY mismatch:**
- ⚠️ Data inconsistency detected
- Check Shuffle workflow logs
- Verify JSON mapping in GetShuffleUser service
- Possible data corruption or attack

---

#### Step 6: Check Shuffle Workflow Execution Logs

**Navigate:** Shuffle UI → Workflow Executions

**Find execution matching timestamp:**
- Time: Within 1 minute of Cerberus Step 16
- Workflow: Security validation workflow

**Check FinalLogic Node Output:**

```json
{
  "status": "unauthorized",
  "severity": "CRITICAL",
  "user": "intruder_hacker",
  "phone": "5555559999",
  "email": "hacker@malicious.com",
  "hour": 15,
  "alert_channel": "gmail"
}
```

**Verify:**
- [ ] `status` = "unauthorized"
- [ ] `severity` = "CRITICAL"
- [ ] `alert_channel` = "gmail"
- [ ] User/phone/email match Step 6 log

---

#### Step 7: Verify Firebase Authentication Logs

**Navigate:** Firebase Console → Authentication → Users

**Search for phone number from email:**
- Phone: `+1` + [Phone from email] (e.g., +15555559999)

**Check:**
1. **User exists?**
   - YES → Credentials are in Firebase (compromised?)
   - NO → Test user not in production Firebase (expected)

2. **Last sign-in timestamp:**
   - Does it match incident timestamp?
   - If YES → Confirm login actually occurred
   - If NO → Test execution only (no real login)

3. **Sign-in method:**
   - Phone authentication
   - Any suspicious providers?

**Firebase Console URL:**
```
https://console.firebase.google.com/project/[PROJECT_ID]/authentication/users
```

---

### Phase 3: Impact Assessment (10-20 minutes)

#### Step 8: Determine Threat Level

**Threat Matrix:**

| Scenario | User | Hour | Firebase Record | Threat Level |
|----------|------|------|-----------------|--------------|
| Test execution (dev) | intruder_* | Any | No record | 🟢 LOW |
| Test execution (prod) | intruder_* | Any | Record exists | 🟡 MEDIUM |
| Unexpected user | Unknown name | != 9 | No record | 🟠 HIGH |
| Unexpected user | Unknown name | != 9 | Record exists | 🔴 CRITICAL |
| Known user wrong time | Real name | != 9 | Record exists | 🟠 HIGH |

**Classification Guide:**

**🟢 LOW (Test Artifact):**
- User identifier contains "test", "intruder", "hacker"
- No Firebase record found
- Execution during business hours
- **Action:** Document and close

**🟡 MEDIUM (Test in Production):**
- Test user but Firebase record exists
- Possible test data in production environment
- **Action:** Review environment isolation

**🟠 HIGH (Suspicious Activity):**
- Unknown user identifier
- No Firebase record (attempted but failed)
- Off-hours execution
- **Action:** Full investigation + IP tracking

**🔴 CRITICAL (Confirmed Breach):**
- Unknown user with Firebase record
- Successful login to production
- Off-hours + unusual location
- **Action:** IMMEDIATE LOCKDOWN + Legal/Compliance notification

---

#### Step 9: Check for Additional Indicators

**Additional Data Sources:**

**A. Cerberus Execution Pattern:**
```sql
-- Query MySQL to find similar attempts
SELECT 
    exe.Start AS Time,
    exe.ControlStatus AS Result,
    prop.Value AS Identity
FROM testcaseexecution exe
JOIN testcasestepexecution step ON exe.ID = step.ID
JOIN testcasestepexecutionproperty prop ON step.ID = prop.ID AND step.Step = prop.Step
WHERE exe.Test = 'LoginTests'
  AND exe.TestCase = 'TC001_SecureLogin'
  AND step.Step = 6
  AND prop.Property = 'TEST_IDENTITY_LOG'
  AND exe.Start >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
ORDER BY exe.Start DESC;
```

**Look for:**
- Multiple attempts in short timeframe (brute force?)
- Same phone number across multiple executions (targeted?)
- Pattern of failures then success (credential stuffing?)

---

**B. Discord Alert History:**

1. Open Discord channel
2. Search: `Unauthorized` (last 24 hours)
3. Count: How many red alerts in past day?

**Frequency Analysis:**
- 1-2 alerts/day → Normal test activity
- 5+ alerts/day → Investigation required
- 20+ alerts/day → Possible automated attack

---

**C. Network/IP Analysis (If Available):**

Check application logs for:
- Source IP address of login attempts
- Geolocation (unexpected countries?)
- User-Agent strings (automated tools?)

**Red Flags:**
- Multiple IPs in short time (distributed attack)
- TOR exit nodes
- Known malicious IP ranges
- Unusual user-agents (bots, scrapers)

---

### Phase 4: Response Actions (20-60 minutes)

#### Step 10: Execute Response Based on Threat Level

**🟢 LOW THREAT (Test Artifact):**

1. **Document:**
   - Add note to incident tracking sheet
   - Format: `[Date] [Time] Test execution alert - User: [name] - Status: False positive`

2. **Close:**
   - No further action required
   - Archive email

3. **Optional:**
   - Review test schedule to reduce off-hours tests
   - Consider whitelisting test user identifiers

---

**🟡 MEDIUM THREAT (Test in Production):**

1. **Verify Environment:**
   - Check which Firebase project was used
   - Confirm test data isolation
   - Review environment variables (DEV vs PROD)

2. **Remediate:**
   - Remove test user from production Firebase
   - Update test configuration to use DEV environment only
   - Add environment validation to test setup

3. **Document:**
   - Incident report: "Test data in production environment"
   - Corrective actions taken
   - Prevention measures implemented

---

**🟠 HIGH THREAT (Suspicious Activity):**

1. **Immediate Actions:**
   - Screenshot all evidence (Step 6 log, Firebase, Discord, Gmail)
   - Export Cerberus execution history (PDF/JSON)
   - Save Shuffle workflow execution logs

2. **Investigation:**
   - Contact user (if known) to verify legitimacy
   - Check for other compromised accounts
   - Review recent Firebase authentication logs (past 7 days)
   - Analyze IP address geolocation

3. **Containment:**
   - Enable additional monitoring alerts
   - Consider temporary rate limiting on phone auth
   - Add suspicious phone number to watchlist

4. **Documentation:**
   - Full incident report (see template below)
   - Timeline reconstruction
   - Root cause analysis

5. **Notification:**
   - Inform security team
   - Alert development team lead
   - Update incident tracking system

---

**🔴 CRITICAL THREAT (Confirmed Breach):**

1. **IMMEDIATE CONTAINMENT (within 5 minutes):**
   - **Disable compromised account** in Firebase
   - **Revoke all active sessions** for affected user
   - **Enable enhanced logging** for all authentication events
   - **Notify incident response team** via phone/SMS (not email)

2. **EVIDENCE PRESERVATION:**
   - Export complete Firebase user record
   - Export all Cerberus executions (past 30 days)
   - Export Shuffle workflow logs
   - Screenshot all Step 6 forensic logs
   - Capture Discord message history
   - Save all Gmail incident emails
   - **DO NOT DELETE ANYTHING** - preservation for legal/forensic

3. **EXPANDED INVESTIGATION:**
   - Check for lateral movement (other accounts accessed?)
   - Review application server logs (unusual API calls?)
   - Check for data exfiltration attempts
   - Analyze authentication patterns (timing, frequency)
   - Investigate source: social engineering? credential theft? brute force?

4. **STAKEHOLDER NOTIFICATION (within 30 minutes):**
   - **CTO/CISO:** Verbal briefing + written summary
   - **Legal:** Potential data breach notification
   - **Compliance:** Regulatory requirements (GDPR, etc.)
   - **PR/Communications:** If customer data affected

5. **REMEDIATION:**
   - Force password reset for all users (if email/password auth)
   - Implement MFA (Multi-Factor Authentication) immediately
   - Review and update phone authentication security
   - Audit Firebase security rules
   - Check for backdoors or persistent access

6. **POST-INCIDENT:**
   - Full forensic report (external security firm if needed)
   - Root cause analysis
   - Security architecture review
   - Implement additional controls
   - Staff training on security awareness

---

### Phase 5: Post-Incident Activities (1-7 days)

#### Step 11: Incident Documentation

**Complete Incident Report Template:**

```markdown
# Security Incident Report: [INCIDENT-ID]

## Executive Summary
- **Date:** [Date]
- **Time:** [Time]
- **Severity:** [LOW/MEDIUM/HIGH/CRITICAL]
- **Status:** [OPEN/INVESTIGATING/RESOLVED/CLOSED]
- **Reporter:** [Name]
- **Investigator:** [Name]

## Incident Details

### Alert Information
- **Alert Source:** Gmail CRITICAL + Discord Red
- **Timestamp:** [ISO 8601]
- **User Identifier:** [Username]
- **Phone Number:** [Phone]
- **Email Address:** [Email]
- **Hour of Attempt:** [Hour]

### Forensic Evidence

#### Cerberus Execution Log
- **Execution ID:** [ID]
- **Test Case:** TC001_SecureLogin
- **Status:** [PASS/FAIL]
- **Step 6 Property (TEST_IDENTITY_LOG):**
  ```
  [Paste complete log entry]
  ```

#### Shuffle Workflow Log
- **Execution ID:** [ID]
- **FinalLogic Output:**
  ```json
  [Paste JSON output]
  ```

#### Firebase Record
- **User UID:** [UID or "Not found"]
- **Last Sign-In:** [Timestamp or "N/A"]
- **Creation Date:** [Date or "N/A"]

### Impact Assessment
- **Threat Level:** [LOW/MEDIUM/HIGH/CRITICAL]
- **Data Accessed:** [Yes/No - Details]
- **Users Affected:** [Count]
- **Monetary Impact:** [$Amount or "None"]

### Response Actions Taken
1. [Action 1 - Timestamp]
2. [Action 2 - Timestamp]
3. [Action 3 - Timestamp]

### Root Cause Analysis
- **Cause:** [Description]
- **Contributing Factors:** [List]
- **How was it possible:** [Explanation]

### Preventive Measures
1. [Measure 1]
2. [Measure 2]
3. [Measure 3]

### Lessons Learned
- [Lesson 1]
- [Lesson 2]

### Attachments
- Screenshot: Cerberus Step 6 log
- Screenshot: Gmail CRITICAL email
- Screenshot: Discord red alert
- Export: Firebase user record (if applicable)
- Export: Cerberus execution history (JSON)

## Signatures
- **Investigator:** [Name] - [Date]
- **Reviewed By:** [Manager Name] - [Date]
- **Approved By:** [CISO/CTO Name] - [Date]
```

---

#### Step 12: Trend Analysis

**Monthly Security Review:**

Track incidents in spreadsheet:

| Date | Time | User | Phone | Threat Level | Response Time | Outcome |
|------|------|------|-------|--------------|---------------|---------|
| 2026-02-01 | 15:45 | intruder_hacker | 5555559999 | LOW | 3 min | False positive |
| 2026-02-05 | 03:15 | unknown_user | 5555558888 | HIGH | 12 min | Investigating |

**Metrics to Track:**
- Total alerts per month
- False positive rate (%)
- Average response time (minutes)
- Threat level distribution
- Time-of-day patterns
- Phone number reuse patterns

**Quarterly Report:**
- Alert trends (increasing/decreasing?)
- Response effectiveness (time to resolution)
- Recommendations for tuning FinalLogic logic
- Proposed enhancements to monitoring

---

#### Step 13: System Tuning

**If FALSE POSITIVE RATE > 20%:**

**Option A: Expand Authorized Users**
```python
# Modify FinalLogic Python node
authorized_users = ["wipedclean", "test_user", "qa_team"]

if username in authorized_users or current_hour == 9:
    status = "verified"
    alert_channel = "discord"
```

**Option B: Extend Authorized Hours**
```python
# Allow testing during business hours
business_hours = range(9, 18)  # 9 AM - 6 PM

if username == "wipedclean" or current_hour in business_hours:
    status = "verified"
    alert_channel = "discord"
```

**Option C: Add Environment Detection**
```python
# Only alert in production
environment = $exec.text.environment  # Pass from Cerberus

if environment == "DEV" or username == "wipedclean":
    status = "verified"
    alert_channel = "discord"
elif environment == "PROD":
    status = "unauthorized"
    alert_channel = "gmail"
```

---

### Phase 6: Knowledge Base Updates

#### Step 14: Update Playbook

**After Each Incident:**
- Document new attack patterns discovered
- Add new indicators of compromise (IOCs)
- Update response procedures based on lessons learned
- Refine threat level matrix

**Playbook Versioning:**
- Version: 1.0 → 1.1 (minor update)
- Version: 1.1 → 2.0 (major overhaul)
- Change log maintained in Git

---

#### Step 15: Team Training

**Quarterly Security Drills:**

1. **Scenario-Based Training:**
   - Run `./test_intrusion.sh` (Scenario 1: Unauthorized)
   - Execute full incident response workflow
   - Time the team from alert to resolution
   - Goal: < 15 minutes for HIGH threat

2. **Tabletop Exercises:**
   - Present hypothetical breach scenarios
   - Walk through playbook steps
   - Identify gaps or confusion
   - Update playbook based on feedback

3. **Tool Familiarization:**
   - Practice accessing Cerberus execution history
   - Practice querying Firebase users
   - Practice checking Shuffle workflow logs
   - Practice running forensic SQL queries

---

## 🎯 Quick Reference Card

### When Gmail CRITICAL Alert Arrives:

**First 2 Minutes:**
1. ✅ Acknowledge alert via email reply
2. ✅ Check Discord for red notification (confirm authenticity)
3. ✅ Record incident details from 8-field table

**Next 10 Minutes:**
4. ✅ Access Cerberus → Execution History → Find matching execution
5. ✅ Verify Step 6 forensic log (TEST_IDENTITY_LOG property)
6. ✅ Check Shuffle workflow logs (FinalLogic output)
7. ✅ Check Firebase Authentication (search phone number)
8. ✅ Determine threat level (LOW/MEDIUM/HIGH/CRITICAL)

**Next 20 Minutes:**
9. ✅ Execute response actions (based on threat level)
10. ✅ Document incident (screenshot evidence)
11. ✅ Notify stakeholders (if HIGH or CRITICAL)

**Within 24 Hours:**
12. ✅ Complete incident report
13. ✅ Implement preventive measures
14. ✅ Update playbook if needed

---

## 📞 Emergency Contacts

| Role | Name | Email | Phone | Escalation |
|------|------|-------|-------|------------|
| **Security Lead** | [Name] | security@lessimp.com | [Phone] | Primary |
| **CTO** | [Name] | [Email] | [Phone] | HIGH/CRITICAL |
| **CISO** | [Name] | [Email] | [Phone] | CRITICAL only |
| **Legal** | [Name] | legal@lessimp.com | [Phone] | CRITICAL + Data breach |
| **DevOps On-Call** | [Rotation] | devops@lessimp.com | [PagerDuty] | Infrastructure issues |

---

## 🔗 Key Resources

| Resource | URL | Purpose |
|----------|-----|---------|
| **Cerberus UI** | http://localhost:8888/ | Test execution logs |
| **Shuffle Workflow** | https://shuffler.io/workflows/... | Security workflow monitoring |
| **Firebase Console** | https://console.firebase.google.com/... | User authentication records |
| **Discord Channel** | https://discord.com/channels/... | Real-time alerts |
| **Gmail Inbox** | info@lessimp.com | CRITICAL incident emails |
| **Incident Tracking** | [Jira/ServiceNow URL] | Incident management |

---

## 📊 Success Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| **Mean Time to Acknowledge (MTTA)** | < 5 min | ___ min | [ ] |
| **Mean Time to Investigate (MTTI)** | < 15 min | ___ min | [ ] |
| **Mean Time to Resolve (MTTR)** | < 60 min | ___ min | [ ] |
| **False Positive Rate** | < 10% | ___% | [ ] |
| **Incident Report Completion** | Within 24h | ___ | [ ] |

---

## 🔐 Playbook Maintenance

**Version:** 1.0  
**Last Updated:** February 1, 2026  
**Next Review:** March 1, 2026  
**Owner:** Security Operations Team  

**Change Log:**
- **v1.0 (2026-02-01):** Initial playbook creation for Project Lessimp-Secure

---

## ✅ Playbook Validation

**Test Scenarios:**

1. **Low Threat Test:** Run `./test_intrusion.sh` → Scenario 1 → Verify can complete investigation in < 10 minutes
2. **High Threat Drill:** Simulate unauthorized user with Firebase record → Execute full response in < 30 minutes
3. **Critical Threat Exercise:** Tabletop exercise with CTO/CISO → Verify escalation procedures

**Sign-Off:**

- [ ] Security Team trained on playbook
- [ ] CTO/CISO reviewed and approved
- [ ] Emergency contacts verified
- [ ] Resource URLs tested
- [ ] Test scenarios executed successfully

---

**STATUS: OPERATIONAL**  
**PROJECT: Lessimp-Secure**  
**CLASSIFICATION: INTERNAL - SECURITY OPERATIONS**

🚨 **THIS PLAYBOOK IS YOUR MASTER KEY TO SECURITY INCIDENT RESPONSE** 🚨
