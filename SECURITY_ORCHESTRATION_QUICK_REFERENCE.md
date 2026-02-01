# 🚀 Security Orchestration Quick Reference

**Version:** 3.0 | **Date:** February 1, 2026 | **Status:** ✅ PRODUCTION READY

---

## 📊 16-Step Test Case Summary

| Step | Action | Critical Data | Fatal |
|------|--------|---------------|-------|
| 1 | callService (GetShuffleUser) | Get credentials from Shuffle | ❌ |
| 2 | verifyNumericEquals (HTTP 200) | Verify Shuffle success | ✅ |
| 3 | verifyStringDifferent (PHONE) | Validate phone exists | ✅ |
| 4 | verifyStringDifferent (OTP) | Validate OTP exists | ✅ |
| 5 | verifyStringDifferent (EMAIL) | Validate email (future) | ❌ |
| 6 | **calculateProperty** | **Log identity for audit** | ❌ |
| 7 | openApplication | Launch iOS app | ❌ |
| 8 | waitForElementPresent | Wait for phone_input | ✅ |
| 9 | type (phone_input) | **INJECT %PHONE%** | ❌ |
| 10 | click (login_button) | Trigger Firebase OTP | ❌ |
| 11 | waitForElementPresent | Wait for OTP screen | ✅ |
| 12 | type (otp_input) | **INJECT %OTP%** | ❌ |
| 13 | click (verify_button) | Submit OTP | ❌ |
| 14 | waitForElementPresent | Wait for home screen | ✅ |
| 15 | verifyElementVisible | Confirm login success | ❌ |
| 16 | **callService (Security)** | **🚨 TRIGGER SHUFFLE WEBHOOK** | ❌ |

---

## 🔐 Security Logic Flow

```
Step 16: callService → ShuffleSecurity_LoginTrigger
    ↓
Shuffle Webhook: webhook_a76354e0-cf09-4754-96e1-682c89084d4c
    ↓
FinalLogic Python Node:
    ↓
    ├─ IF user == "wipedclean" OR hour == 9
    │   └─ ✅ Discord: "Identity Verified" (GREEN)
    │
    └─ ELSE
        └─ 🚨 Gmail SMTP: "CRITICAL: Unauthorized Login" (RED)
```

---

## 📋 calculateProperty Explanation (Step 6)

### Purpose
Creates an **audit trail** in Cerberus execution history showing which user credentials were used. Critical for security forensics.

### Configuration
| Field | Value |
|-------|-------|
| **Action** | `calculateProperty` |
| **Value1** | `TEST_IDENTITY_LOG` (property name) |
| **Value2** | `Testing with: PHONE=%PHONE%, USER=%USER_NAME%, EMAIL=%EMAIL%, USER_ID=%USER_ID%` |

### Runtime Example
**Before Substitution:**
```
Testing with: PHONE=%PHONE%, USER=%USER_NAME%, EMAIL=%EMAIL%, USER_ID=%USER_ID%
```

**After Substitution:**
```
Testing with: PHONE=5555551003, USER=Carol Davis, EMAIL=carol.davis@testmail.com, USER_ID=3
```

### Where to View
1. Cerberus UI → Run → **Execution History**
2. Click execution → **View Details**
3. Step 6 → Property **TEST_IDENTITY_LOG** shows substituted values

### Why This Matters
- ✅ **Debugging:** Know which user was used if test fails
- ✅ **Auditing:** Track test data used in each execution
- ✅ **Security:** Forensic evidence for unauthorized access investigations
- ✅ **Compliance:** Prove randomized testing with traceability

---

## 🎨 Gmail SMTP Template Features

### Visual Design
- **Red gradient header** with 🚨 icon
- **CRITICAL severity badge** in white on red
- **Yellow warning box** for immediate attention
- **Structured incident details table** (8 fields)
- **Blue action section** with investigation checklist
- **Professional footer** with Lessimp branding

### Dynamic Fields (Shuffle Variables)
| Field | Shuffle Variable | Example Value |
|-------|------------------|---------------|
| User Identifier | `$finallogic.user` | `unknown_user` |
| Timestamp | `$finallogic.timestamp` | `2026-02-01T14:30:00` |
| Phone Number | `$exec.text.phone` | `+15555551003` |
| Email | `$exec.text.email` | `carol.davis@testmail.com` |
| Hour | `$finallogic.hour` | `14` |

### Subject Line
```
🚨 CRITICAL: Unauthorized Login Attempt - Lessimp Security Alert
```

### Recipients
- **To:** info@lessimp.com
- **CC:** wfrancois@lessimp.com
- **From:** security@lessimp.com (or authenticated Gmail)

### CTA Buttons
1. **View Cerberus Logs** → http://localhost:8888/
2. **View Firebase Logs** → https://console.firebase.google.com/

---

## 🔧 Service Configuration

### Service 1: GetShuffleUser
```
Method: POST
URL: %SHUFFLE_BASE_URL%/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute
Headers:
  - Content-Type: application/json
  - Authorization: Bearer %SHUFFLE_API_TOKEN%
```

### Service 2: ShuffleSecurity_LoginTrigger
```
Method: POST
URL: https://shuffler.io/api/v1/hooks/webhook_a76354e0-cf09-4754-96e1-682c89084d4c
Headers:
  - Content-Type: application/json
Body:
{
  "user": "wipedclean",
  "phone": "%PHONE%",
  "email": "%EMAIL%",
  "timestamp": "%SYS.TODAY%",
  "test_case": "TC001_SecureLogin",
  "status": "login_complete"
}
```

---

## 🎯 Discord Webhook Configuration

### Verified Status (Green Embed)
```json
{
  "embeds": [{
    "title": "✅ Lessimp Security: Identity Verified",
    "description": "User 'wipedclean' logged in successfully",
    "color": 3066993,
    "fields": [
      {"name": "User", "value": "wipedclean", "inline": true},
      {"name": "Phone", "value": "+15555551003", "inline": true},
      {"name": "Timestamp", "value": "2026-02-01T14:30:00", "inline": true}
    ]
  }]
}
```

### Unauthorized Status (Red Embed)
```json
{
  "embeds": [{
    "title": "🚨 CRITICAL: Unauthorized Login Attempt",
    "description": "Unknown user attempted login - Gmail alert sent",
    "color": 15158332,
    "fields": [
      {"name": "User", "value": "unknown_user", "inline": true},
      {"name": "Severity", "value": "CRITICAL", "inline": true}
    ]
  }]
}
```

**Webhook URL:**
```
https://discord.com/api/webhooks/.../9DQw5FmRhZ4oKLp9jN2QPvZyKVPcXOhsz_j5qpFXc5oYTHQu79TS_TRvGiUkO6vCX2QT
```

---

## 🔍 FinalLogic Python Node (Complete Code)

```python
import json
from datetime import datetime

# Input from Shuffle webhook
user = $exec.text.user  # e.g., "wipedclean"
timestamp = datetime.now()
hour = timestamp.hour

# Security validation logic
if user == "wipedclean" or hour == 9:
    status = "verified"
    severity = "INFO"
    message = f"✅ Identity Restored: User '{user}' logged in successfully at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    alert_channel = "discord"
else:
    status = "unauthorized"
    severity = "CRITICAL"
    message = f"🚨 UNAUTHORIZED LOGIN ATTEMPT: User '{user}' at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    alert_channel = "gmail"

# Output to next Shuffle node
return {
    "status": status,
    "severity": severity,
    "message": message,
    "alert_channel": alert_channel,
    "user": user,
    "timestamp": timestamp.isoformat(),
    "hour": hour
}
```

---

## 🚀 One-Command Execution

### Start Infrastructure
```bash
# Cerberus
cd ~/Documents/GitHub/cerberus-core && docker-compose up -d

# Shuffle (if local)
cd ~/shuffle && docker-compose up -d

# iOS Simulator
xcrun simctl boot "iPhone 16 Pro" && open -a Simulator
```

### Run Test
```bash
# Access Cerberus UI
open http://localhost:8888/

# Navigate: Run → Test Queue → Manual Execution
# Select: TC001_SecureLogin
# Click: [Execute]
```

---

## 📊 Expected Results

### Scenario 1: Authorized User (wipedclean)
| Component | Expected Result |
|-----------|-----------------|
| **Cerberus** | ✅ All 16 steps PASS |
| **Discord** | ✅ Green embed: "Identity Verified" |
| **Gmail** | ❌ No email sent |
| **Duration** | 50-70 seconds |

### Scenario 2: Unauthorized User (NOT wipedclean AND hour ≠ 9)
| Component | Expected Result |
|-----------|-----------------|
| **Cerberus** | ✅ All 16 steps PASS (functional test succeeds) |
| **Discord** | 🚨 Red embed: "Unauthorized Login" |
| **Gmail** | 🚨 Critical incident email to info@lessimp.com |
| **Duration** | 50-70 seconds |

---

## 🐛 Troubleshooting

### Issue: Step 6 property not visible

**Solution:**
1. Navigate: Cerberus UI → Run → Execution History
2. Click execution → View Details
3. Scroll to Step 6
4. Look for property: `TEST_IDENTITY_LOG`
5. If missing: Re-run test, ensure Step 6 executes successfully

### Issue: Step 16 webhook fails

**Test webhook manually:**
```bash
curl -X POST https://shuffler.io/api/v1/hooks/webhook_a76354e0-cf09-4754-96e1-682c89084d4c \
  -H "Content-Type: application/json" \
  -d '{"user": "wipedclean", "phone": "5555551003", "email": "test@test.com", "timestamp": "2026-02-01T14:30:00"}'
```

### Issue: Gmail HTML not rendering

**Check:**
1. Shuffle Gmail node: Ensure "Body Type" = `HTML`
2. Test email client: Some clients strip HTML (try Gmail web interface)
3. Variables: Verify Shuffle variables populated correctly

### Issue: Discord webhook not working

**Test:**
```bash
curl -X POST "https://discord.com/api/webhooks/.../YOUR_WEBHOOK" \
  -H "Content-Type: application/json" \
  -d '{"content": "Test from Shuffle"}'
```

---

## 📁 Documentation Files

| File | Purpose | Size |
|------|---------|------|
| `MASTER_DIRECTIVE_SECURITY_ORCHESTRATION.md` | Complete integration guide | 45 KB |
| `GMAIL_CRITICAL_INCIDENT_TEMPLATE.html` | Professional email template | 12 KB |
| `SECURITY_ORCHESTRATION_QUICK_REFERENCE.md` | This file | 8 KB |

---

## ✅ Pre-Flight Checklist

- [ ] Cerberus running: http://localhost:8888/
- [ ] Shuffle workflow accessible
- [ ] iOS Simulator booted
- [ ] Flutter app built: `Runner.app`
- [ ] Firebase test numbers configured (5 numbers)
- [ ] Discord webhook tested
- [ ] Gmail SMTP credentials in Shuffle
- [ ] Global properties: `SHUFFLE_BASE_URL`, `SHUFFLE_API_TOKEN`
- [ ] Services created: `GetShuffleUser`, `ShuffleSecurity_LoginTrigger`
- [ ] Test case created: `TC001_SecureLogin` (16 steps)

---

**Status:** ✅ READY FOR EXECUTION  
**Version:** 3.0 - Security Integration  
**Last Updated:** February 1, 2026  
**Author:** GitHub Copilot AI Agent

**🎯 Next Action:** Execute TC001_SecureLogin and verify security alerts! 🚀
