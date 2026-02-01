# 🔧 Cerberus Testing - Apple Silicon Setup & Fixes

## 📋 Overview

This document captures all the fixes applied to successfully run **Cerberus Testing v4.20** on **Apple Silicon (M-series) Macs** using Docker Compose with **AMD64 emulation via Rosetta 2**.

---

## 🎯 Issues Resolved

### 1. ✅ ROOT.war Context Path Issue
**Problem:** Application deployed as `ROOT.war` but accessed incorrectly at `/Cerberus/`  
**Solution:** Access at root context `/` instead  
**Correct URL:** `http://localhost:8888/`  
**Incorrect URL:** ~~`http://localhost:8888/Cerberus/`~~ (404 error)

### 2. ✅ M1/M3 Mac Database Compatibility
**Problem:** MySQL container needs `platform: linux/amd64` for Apple Silicon  
**Solution:** Added platform specification in `docker-compose.yml`  
**Result:** Database runs successfully via Rosetta 2 emulation

### 3. ✅ Database Initialization
**Problem:** Application started before database tables were imported  
**Solution:** Database now fully populated with 72 tables including `myversion`  
**Status:** ✅ HEALTHY & POPULATED

### 4. ✅ API Endpoint Compatibility
**Problem:** Modern REST API endpoints (`/api/public/*`) don't exist in v4.20  
**Solution:** Use UI-based test case creation instead  
**Version Note:** API endpoints require Cerberus v4.15+

### 5. ✅ System/Application Hierarchy Requirement
**Problem:** "Verify rights on object's system" error  
**Solution:** Must create System → Application → Test → Test Case hierarchy  
**Documentation:** See `CERBERUS_PERMISSION_FIX.md`

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop for Mac with Rosetta 2 enabled
- Apple Silicon Mac (M1, M2, M3, etc.)
- Port 8888 available

### Start Cerberus

```bash
cd ~/Documents/GitHub/cerberus-core/docker/compositions/cerberus-tomcat-mysql
docker-compose up -d
```

### Access Cerberus

**URL:** http://localhost:8888/  
**Credentials:**
- Username: `admin`
- Password: `admin`

### Initial Setup (Required)

Follow these steps in order:

1. **Create System**
   - Go to: Administration → System
   - Create: `MySystem` or `PROD_SYSTEM`
   - Mark as Active

2. **Create Application**
   - Go to: Administration → Application
   - Create: `MyWebApp` or `MyFlutterApp`
   - Link to the System you created
   - Type: `WEB`

3. **Verify User Permissions**
   - Go to: Administration → User
   - Ensure `admin` user has access to your System

4. **Create Test Cases**
   - Go to: Test → Test Cases
   - Follow guides in documentation files

**Detailed Instructions:** See `CERBERUS_QUICK_SETUP.md`

---

## 📚 Documentation Files

All guides are in this directory:

### Setup Guides
- **`CERBERUS_QUICK_SETUP.md`** - 📍 START HERE - Visual quick start (10 min)
- **`CERBERUS_MANUAL_SETUP.md`** - Complete manual test creation guide
- **`CERBERUS_PERMISSION_FIX.md`** - Fixing system/permission errors
- **`CERBERUS_QUICKSTART.md`** - General quickstart reference

### Reference Documentation
- **`cerberus_test_examples.md`** - Test case examples and action reference
- **`YOUR_TEST_CASE_GUIDE.md`** - Step-by-step test case guide
- **`ERROR_EXPLANATION.md`** - Understanding the API compatibility issue

### Scripts (Reference Only - v4.20 incompatible)
- **`cerberus_helper.py`** - Python API helper (needs v4.15+)
- **`create_simple_test.sh`** - Bash API script (needs v4.15+)
- **`create_cerberus_test.sh`** - Alternative API script (needs v4.15+)

**Note:** Scripts require Cerberus v4.15+ with REST API support. Use UI-based creation for v4.20.

---

## 🛠️ Docker Compose Configuration

### Key Settings

**Location:** `docker/compositions/cerberus-tomcat-mysql/docker-compose.yml`

```yaml
services:
  database:
    platform: linux/amd64  # ← Critical for Apple Silicon
    image: cerberustesting/cerberus-db-mysql:latest
    command: --authentication_policy=mysql_native_password
    ports:
      - "13306:3306"
    volumes:
      - ./localdata/mysql-db:/var/lib/mysql
      
  cerberus:
    platform: linux/amd64  # ← Critical for Apple Silicon
    image: cerberustesting/cerberus-as-tomcat:latest
    environment:
      - DATABASE_HOST=database
      - DATABASE_PORT=3306
      - JDBC_OPTIONS=allowPublicKeyRetrieval=true&useSSL=false
    ports:
      - "8888:8080"  # ← Access at http://localhost:8888/
    volumes:
      - ./localdata/cerberusmedia:/opt/CerberusMedias/
```

---

## 🔍 Verification

### Check Services are Running

```bash
cd ~/Documents/GitHub/cerberus-core/docker/compositions/cerberus-tomcat-mysql
docker-compose ps
```

Expected output:
```
cerberus-tomcat-mysql-database-1   Up (healthy)
cerberus-tomcat-mysql-cerberus-1   Up
```

### Check Database Health

```bash
docker exec cerberus-tomcat-mysql-database-1 mysql -ucerberus -pcerberus -e "SHOW TABLES;" cerberus | wc -l
```

Expected: `73` (72 tables + header line)

### Check Application Logs

```bash
docker-compose logs --tail=50 cerberus
```

Should show: `Server startup in [XXXX] milliseconds`

### Test Web Access

```bash
curl -I http://localhost:8888/
```

Expected: `HTTP/1.1 200`

---

## 🎯 Test Case Creation Workflow

### Hierarchy Structure

```
System (e.g., "PROD_SYSTEM")
  └── Application (e.g., "MyFlutterApp")
        └── Test (e.g., "MyFirstTest")
              └── Test Case (e.g., "TC001_VerifyWebsiteText")
                    ├── Step 1: openUrl → https://example.com
                    ├── Step 2: verifyTextInPage → "Example Domain"
                    └── Step 3: verifyElementPresent → id=content
```

### Common Actions Reference

**Navigation:**
- `openUrl` - Open a URL
- `click` - Click an element
- `clickAndWait` - Click and wait for page load

**Verification:**
- `verifyTextInPage` - Verify text exists
- `verifyElementPresent` - Verify element exists
- `verifyTitle` - Verify page title

**Input:**
- `type` - Type text into field
- `select` - Select from dropdown
- `clearField` - Clear input field

**Waits:**
- `wait` - Simple wait (milliseconds)
- `waitForElementPresent` - Wait for element

**Element Locators:**
- `id=myId` - By ID
- `name=myName` - By name
- `xpath=//div[@class='x']` - By XPath
- `css=#myId` - By CSS selector
- `link=Click Here` - By link text

---

## 🔗 Important URLs

- **Homepage:** http://localhost:8888/
- **Test Case List:** http://localhost:8888/TestCaseList.jsp
- **Run Tests:** http://localhost:8888/RunTests.jsp
- **Execution Reports:** http://localhost:8888/ReportingExecutionList.jsp
- **System Management:** http://localhost:8888/SystemList.jsp
- **Application Management:** http://localhost:8888/ApplicationList.jsp
- **User Management:** http://localhost:8888/UserList.jsp
- **Database (MySQL):** localhost:13306

---

## 🐛 Troubleshooting

### Container Won't Start
```bash
cd ~/Documents/GitHub/cerberus-core/docker/compositions/cerberus-tomcat-mysql
docker-compose down
docker-compose up -d
docker-compose logs -f
```

### Database Connection Issues
```bash
# Check database is healthy
docker-compose ps database

# Connect to database manually
docker exec -it cerberus-tomcat-mysql-database-1 mysql -ucerberus -pcerberus cerberus
```

### "Verify Rights on Object's System" Error
**Cause:** No System/Application configured  
**Solution:** Follow `CERBERUS_PERMISSION_FIX.md`

### 404 Error on /Cerberus/ Path
**Cause:** Wrong URL - app is at root context  
**Solution:** Use `http://localhost:8888/` instead

### Port 8888 Already in Use
```bash
# Find process using port 8888
lsof -i :8888

# Stop Cerberus
docker-compose down

# Or change port in docker-compose.yml
ports:
  - "8889:8080"  # Use 8889 instead
```

---

## 📊 System Information

### Environment Details
- **Cerberus Version:** 4.20
- **Tomcat Version:** 9.0.109
- **MySQL Version:** 8.0.42
- **Docker Platform:** linux/amd64 (via Rosetta 2)
- **Architecture:** Apple Silicon (M1/M2/M3)

### Database Credentials
- **Database:** cerberus
- **User:** cerberus
- **Password:** cerberus
- **Root Password:** rootpassword

### Data Persistence
- **MySQL Data:** `./localdata/mysql-db`
- **Cerberus Media:** `./localdata/cerberusmedia`

---

## 🎉 Success Indicators

When everything is working correctly, you should see:

✅ Docker containers running and healthy  
✅ Login page accessible at http://localhost:8888/  
✅ Successful login with admin/admin  
✅ 72 tables in MySQL database  
✅ No errors in application logs  
✅ System and Application can be created  
✅ Test cases can be created and run  

---

## 🚀 Next Steps

1. ✅ Create your first System
2. ✅ Create your first Application
3. ✅ Create your first Test Case
4. ✅ Run the test and view results
5. ✅ Create more complex test scenarios
6. ✅ Set up test campaigns
7. ✅ Integrate with CI/CD (future)

---

## 📝 Notes

### Version Compatibility
- **Cerberus v4.20:** Uses Servlet-based architecture, no REST API
- **Cerberus v4.15+:** Has REST API at `/api/public/*` endpoints
- **For v4.20:** Use UI-based test creation
- **For v4.15+:** Can use scripts and API automation

### Upgrade Path
To use the API scripts in this repository:
1. Upgrade to Cerberus v4.15 or later
2. Check: https://github.com/cerberustesting/cerberus-docker
3. Update docker-compose.yml with newer image tags

---

## 🙏 Credits

This setup guide was created through collaborative troubleshooting to resolve:
- Apple Silicon compatibility issues
- Context path confusion
- Database initialization timing
- API version differences
- Permission hierarchy requirements

---

## 📧 Support

- **Cerberus Documentation:** http://localhost:8888/documentation/
- **GitHub Issues:** https://github.com/cerberustesting/cerberus-docker/issues
- **Community:** https://github.com/cerberustesting/cerberus-source

---

**Last Updated:** February 1, 2026  
**Environment:** Apple Silicon Mac, Docker Desktop, Rosetta 2  
**Status:** ✅ Fully Functional
