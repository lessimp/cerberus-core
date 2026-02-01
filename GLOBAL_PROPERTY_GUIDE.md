# 🔀 Cerberus Global Property Guide: Hybrid Shuffle Environment Switching

**Purpose:** Toggle between Local Shuffle Engine and Cloud Shuffle Portal without modifying test cases.

---

## 📋 Overview

The **Global Property** feature in Cerberus allows you to define variables that are accessible across ALL test cases, test steps, and services. This is perfect for environment-specific configurations like API base URLs.

**Use Case:** Switch between Local Shuffle (http://localhost:3001) and Cloud Shuffle (https://shuffler.io) by changing a single property value.

---

## 🎯 Configuration Steps

### Step 1: Navigate to Global Properties

1. Log in to Cerberus: http://localhost:8888/
2. Click: **Administration** (top menu)
3. Click: **Global Property** (left sidebar)

**Direct URL:**
```
http://localhost:8888/PropertyList.jsp
```

---

### Step 2: Create SHUFFLE_BASE_URL Property

Click: **[+ Create Property]**

| Field | Value |
|-------|-------|
| **Property** | `SHUFFLE_BASE_URL` |
| **Type** | `text` |
| **Database** | (leave empty) |
| **Value** | `http://localhost:3001` ← **START WITH LOCAL** |
| **Length** | `0` (unlimited) |
| **Nature** | `STATIC` |
| **Description** | `Shuffle workflow execution base URL - Switch between Local (localhost:3001) and Cloud (shuffler.io)` |
| **Country** | `ALL` (or specific if needed) |

**Click:** [Save]

---

### Step 3: Create SHUFFLE_API_TOKEN Property (For Cloud)

Click: **[+ Create Property]**

| Field | Value |
|-------|-------|
| **Property** | `SHUFFLE_API_TOKEN` |
| **Type** | `text` |
| **Database** | (leave empty) |
| **Value** | `<your_shuffler_io_api_token>` ← **REPLACE WITH REAL TOKEN** |
| **Length** | `0` (unlimited) |
| **Nature** | `STATIC` |
| **Description** | `Shuffle Cloud authentication token - Required for shuffler.io API calls` |
| **Country** | `ALL` |

**Click:** [Save]

**⚠️ Security Note:** In production, use Cerberus's encrypted property feature or environment-specific properties.

---

### Step 4: Update GetShuffleUser Service to Use Global Property

Navigate to: **Service Library** → **GetShuffleUser**

**Original Service Path (hardcoded):**
```
http://localhost:3001/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute
```

**Updated Service Path (dynamic):**
```
%SHUFFLE_BASE_URL%/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute
```

**Service Headers:**

| Header Name | Header Value | Condition |
|-------------|--------------|-----------|
| `Content-Type` | `application/json` | Always |
| `Accept` | `application/json` | Always |
| `Authorization` | `Bearer %SHUFFLE_API_TOKEN%` | **Only for Cloud** (optional for Local) |

**Click:** [Save]

---

## 🔄 Environment Switching

### Switch to Local Shuffle Engine

1. Navigate to: Administration → Global Property
2. Find: `SHUFFLE_BASE_URL`
3. Click: [Edit]
4. **Value:** `http://localhost:3001`
5. Click: [Save]

**Result:** All test cases now call Local Shuffle Engine (no authentication required)

**Verify:**
```bash
curl -X POST http://localhost:3001/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

### Switch to Cloud Shuffle Portal

1. Navigate to: Administration → Global Property
2. Find: `SHUFFLE_BASE_URL`
3. Click: [Edit]
4. **Value:** `https://shuffler.io`
5. Click: [Save]
6. **ALSO:** Ensure `SHUFFLE_API_TOKEN` is set with valid token

**Result:** All test cases now call Cloud Shuffle Portal (authentication required)

**Verify:**
```bash
curl -X POST https://shuffler.io/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{}'
```

---

## 📊 Variable Substitution Flow

### Runtime Substitution Example

**Global Property Value:**
```
SHUFFLE_BASE_URL = http://localhost:3001
```

**Service Configuration:**
```
Service Path: %SHUFFLE_BASE_URL%/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute
```

**Runtime Execution:**
```
Actual URL Called: http://localhost:3001/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute
```

### Nested Variable Substitution

Cerberus supports chaining variables:

**Example:**
```
SHUFFLE_WORKFLOW_ID = 5e611ec1-350b-4395-9794-c0b08a098649
SHUFFLE_ENDPOINT = %SHUFFLE_BASE_URL%/api/v1/workflows/%SHUFFLE_WORKFLOW_ID%/execute
```

**Service Path:**
```
%SHUFFLE_ENDPOINT%
```

**Runtime:**
```
http://localhost:3001/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute
```

---

## 🎯 Advanced: Environment-Specific Properties

### Scenario: Different URLs per Country

| Property Name | Country | Value | Use Case |
|---------------|---------|-------|----------|
| `SHUFFLE_BASE_URL` | `US` | `http://localhost:3001` | US testing (local) |
| `SHUFFLE_BASE_URL` | `EU` | `https://eu.shuffler.io` | EU testing (cloud Europe) |
| `SHUFFLE_BASE_URL` | `GLOBAL` | `https://shuffler.io` | Global testing (cloud US) |

**Test Case Execution:**
- Run test with Country=US → Uses local endpoint
- Run test with Country=EU → Uses EU cloud endpoint
- Run test with Country=GLOBAL → Uses US cloud endpoint

---

## 🔐 Conditional Headers Based on Environment

### Problem: Authorization header only needed for Cloud

**Solution: Use Conditional Property**

**Create Property:**
```
Property: SHUFFLE_AUTH_REQUIRED
Type: text
Value: false (for local) or true (for cloud)
```

**Service Header Configuration:**

| Header Name | Header Value | Condition |
|-------------|--------------|-----------|
| `Authorization` | `Bearer %SHUFFLE_API_TOKEN%` | `%SHUFFLE_AUTH_REQUIRED% == true` |

**Note:** Cerberus v4.20 may not support conditional headers directly. Alternative: Use two services:
- `GetShuffleUser_Local` (no auth header)
- `GetShuffleUser_Cloud` (with auth header)

Then use a conditional step to call the correct service.

---

## 📝 Best Practices

### 1. Use Descriptive Property Names

✅ **Good:**
```
SHUFFLE_BASE_URL
SHUFFLE_API_TOKEN
SHUFFLE_WORKFLOW_ID
```

❌ **Bad:**
```
URL
TOKEN
ID
```

### 2. Document Property Values

Always include description explaining:
- What the property controls
- Valid values
- Impact of changing it

### 3. Version Control Property Configurations

Create a documentation file listing all global properties:

```markdown
# Cerberus Global Properties

## SHUFFLE_BASE_URL
- **Local:** http://localhost:3001
- **Cloud:** https://shuffler.io
- **Purpose:** Base URL for Shuffle workflow execution

## SHUFFLE_API_TOKEN
- **Value:** (stored in password manager)
- **Purpose:** Authentication for shuffler.io API
```

### 4. Test Both Environments

Before production deployment:
1. Run test with `SHUFFLE_BASE_URL=http://localhost:3001`
2. Verify: Test passes
3. Switch: `SHUFFLE_BASE_URL=https://shuffler.io`
4. Verify: Test passes with cloud endpoint

### 5. Use Environment-Specific Test Data

**Example:**

| Property | Local Value | Cloud Value |
|----------|-------------|-------------|
| `SHUFFLE_BASE_URL` | `http://localhost:3001` | `https://shuffler.io` |
| `EXPECTED_LATENCY_MS` | `100` | `500` |
| `RETRY_COUNT` | `1` | `3` |

---

## 🛠️ Troubleshooting

### Issue: Variable not substituted (shows as %SHUFFLE_BASE_URL%)

**Causes:**
1. Property name typo
2. Property not created in Cerberus
3. Property scope mismatch (Country-specific vs ALL)

**Solution:**
1. Verify property exists: Administration → Global Property
2. Check spelling: `SHUFFLE_BASE_URL` (case-sensitive)
3. Ensure Country is `ALL` or matches test execution country

---

### Issue: 401 Unauthorized when calling Cloud Shuffle

**Causes:**
1. `SHUFFLE_API_TOKEN` not set
2. Token expired
3. Authorization header missing from service

**Solution:**
1. Verify token: Administration → Global Property → `SHUFFLE_API_TOKEN`
2. Regenerate token in shuffler.io console
3. Add header to GetShuffleUser service: `Authorization: Bearer %SHUFFLE_API_TOKEN%`

---

### Issue: Service call timeout (Local Shuffle)

**Causes:**
1. Shuffle local engine not running
2. Wrong port (3001 vs 3000)
3. Docker container stopped

**Solution:**
```bash
# Check if Shuffle is running
curl http://localhost:3001/api/v1/workflows

# Start Shuffle
cd ~/shuffle
docker-compose up -d

# Check logs
docker-compose logs -f backend
```

---

### Issue: Service call timeout (Cloud Shuffle)

**Causes:**
1. Network connectivity issue
2. Firewall blocking outbound HTTPS
3. Shuffler.io service down

**Solution:**
```bash
# Test connectivity
curl -I https://shuffler.io

# Test API endpoint
curl -X POST https://shuffler.io/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'

# Check shuffler.io status
open https://status.shuffler.io
```

---

## 📊 Verification Checklist

### Pre-Execution Checks

- [ ] `SHUFFLE_BASE_URL` global property exists
- [ ] Value is either `http://localhost:3001` or `https://shuffler.io`
- [ ] `SHUFFLE_API_TOKEN` global property exists (for cloud)
- [ ] GetShuffleUser service uses `%SHUFFLE_BASE_URL%` in Service Path
- [ ] Authorization header configured (for cloud)

### Local Environment Verification

```bash
# 1. Check Shuffle local engine
curl http://localhost:3001/api/v1/workflows

# 2. Test workflow execution
curl -X POST http://localhost:3001/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute \
  -H "Content-Type: application/json" \
  -d '{}' | jq '.'

# 3. Verify response structure
# Expected: {"success": true, "shuffled_user": {...}}
```

### Cloud Environment Verification

```bash
# 1. Check shuffler.io connectivity
curl -I https://shuffler.io

# 2. Test workflow execution
curl -X POST https://shuffler.io/api/v1/workflows/5e611ec1-350b-4395-9794-c0b08a098649/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{}' | jq '.'

# 3. Verify authentication
# Expected: HTTP 200 if token valid, HTTP 401 if invalid
```

---

## 🚀 Quick Reference Card

| Task | Command |
|------|---------|
| **View all properties** | http://localhost:8888/PropertyList.jsp |
| **Switch to Local** | Set `SHUFFLE_BASE_URL` = `http://localhost:3001` |
| **Switch to Cloud** | Set `SHUFFLE_BASE_URL` = `https://shuffler.io` |
| **Test Local endpoint** | `curl http://localhost:3001/api/v1/workflows` |
| **Test Cloud endpoint** | `curl https://shuffler.io/api/v1/workflows` |
| **Use in service** | `%SHUFFLE_BASE_URL%/api/v1/...` |
| **Use in test step** | Value1: `%SHUFFLE_BASE_URL%` |

---

## 📦 Export/Import Properties

### Export Properties (Manual)

1. Navigate to: Administration → Global Property
2. For each property, note:
   - Property name
   - Value
   - Description
3. Save to text file: `cerberus_global_properties.txt`

### Import Properties (Manual)

1. Navigate to: Administration → Global Property
2. For each property in export file:
   - Click: [+ Create Property]
   - Fill in fields
   - Click: [Save]

**Note:** Cerberus v4.20 may not have automated import/export. Use database backup for bulk operations.

---

## 🔒 Security Considerations

### Sensitive Properties (API Tokens)

**Do NOT store in plain text if:**
- Running in production
- Multiple team members have access
- Property contains credentials/tokens

**Alternatives:**
1. Use Cerberus encrypted properties (if available)
2. Store token in environment variable, reference in property
3. Use external secret management (HashiCorp Vault, AWS Secrets Manager)

### Property Audit Trail

**Track property changes:**
1. Note: Cerberus logs property modifications
2. Check: testcaseproperty table in MySQL
3. Query: `SELECT * FROM testcaseproperty WHERE property='SHUFFLE_BASE_URL' ORDER BY DateModif DESC;`

---

**Status:** ✅ Complete Configuration Guide  
**Last Updated:** February 1, 2026  
**Cerberus Version:** v4.20  
**Author:** GitHub Copilot AI Agent
