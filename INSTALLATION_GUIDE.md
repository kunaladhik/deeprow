# 🎯 INSTALLATION GUIDE - Step by Step

## ⚠️ Current Status

**Node.js:** ❌ NOT INSTALLED  
**npm:** ❌ NOT INSTALLED  
**Project:** ✅ Ready (created and configured)

---

## 📋 What You Need to Do

### STEP 1: Install Node.js (5 minutes)

#### Option A: Automatic (Easiest)
1. Go to: https://nodejs.org/
2. Click the big green **"LTS"** button
3. Run the installer file
4. Click "Next" through all screens
5. Click "Install"
6. **Restart your computer**

#### Option B: Manual Download
1. Visit: https://nodejs.org/en/download/
2. Select: **Windows Installer (.msi)**
3. Select: **LTS version** (recommended)
4. Select: **64-bit** (if your computer is 64-bit)
5. Run the installer
6. **Restart your computer**

---

### STEP 2: Verify Installation (1 minute)

After restarting, open **PowerShell** and run:

```bash
node --version
npm --version
```

You should see version numbers like:
```
v18.18.0
9.6.7
```

If you see version numbers, you're good! ✅

---

### STEP 3: Install Dependencies (5-10 minutes)

Navigate to your project and install:

```bash
cd "C:\Users\kunal\OneDrive\Desktop\DeepRow UI"
npm install
```

**What happens:**
- npm downloads all required packages
- Creates a `node_modules` folder (~400MB)
- This takes 5-10 minutes on first install
- You'll see lots of output (normal!)

**When it's done**, you'll see:
```
added XXX packages in XXs
```

---

### STEP 4: Start Development Server (30 seconds)

```bash
npm run dev
```

**What happens:**
- Vite starts a development server
- Your browser opens automatically
- You'll see: `Local: http://localhost:3000`
- The app is now running!

**Expected output:**
```
  VITE v5.0.0  ready in XXX ms

  ➜  Local:   http://localhost:3000/
  ➜  press h to show help
```

---

### STEP 5: View Your Application

1. Your browser should open automatically
2. If not, visit: **http://localhost:3000**
3. You should see your React application!

---

## 🎯 Using the Automated Script

If you want to automate steps 3-4:

### Double-Click Method
1. Navigate to: `C:\Users\kunal\OneDrive\Desktop\DeepRow UI\`
2. Double-click: `start.bat`
3. The script will:
   - Check for Node.js
   - Install dependencies
   - Start the development server
   - Open your browser

### PowerShell Method
```bash
cd "C:\Users\kunal\OneDrive\Desktop\DeepRow UI"
.\start.bat
```

---

## ✅ Complete Checklist

- [ ] Downloaded Node.js LTS from nodejs.org
- [ ] Ran the Node.js installer
- [ ] Restarted computer
- [ ] Verified: `node --version` (shows version)
- [ ] Verified: `npm --version` (shows version)
- [ ] Ran: `npm install` (completed successfully)
- [ ] Ran: `npm run dev` (server started)
- [ ] Opened: http://localhost:3000 (saw the app)

---

## 🚨 Troubleshooting

### Problem: "npm: The term 'npm' is not recognized"

**Cause:** Node.js not installed or restart needed

**Solution:**
1. Install Node.js from https://nodejs.org/
2. **Restart your computer**
3. Open a **new PowerShell window**
4. Try again: `npm --version`

---

### Problem: "npm install is very slow"

**Cause:** This is normal! Large download

**Solution:**
1. Wait patiently (takes 5-10 minutes)
2. Don't close the terminal
3. First install is always slowest
4. Next installs will be faster

**If it times out after 30+ minutes:**
```bash
npm install --no-audit --prefer-offline
```

---

### Problem: "Port 3000 already in use"

**Cause:** Another app is using port 3000

**Solution - Option 1:** Use different port
```bash
npm run dev -- --port 3001
```

**Solution - Option 2:** Find and close the app using port 3000
```bash
netstat -ano | findstr :3000
```

---

### Problem: "EACCES: permission denied"

**Cause:** Windows permissions issue

**Solution:**
1. Right-click PowerShell
2. Select "Run as Administrator"
3. Try again: `npm install`

---

### Problem: "Command 'npm install' fails"

**Solution 1:** Clear npm cache
```bash
npm cache clean --force
npm install
```

**Solution 2:** Reinstall Node.js
1. Uninstall Node.js
2. Download again from nodejs.org
3. Install fresh
4. Restart computer
5. Try `npm install` again

---

## 💾 File Locations

```
Project Folder:
C:\Users\kunal\OneDrive\Desktop\DeepRow UI\

Important Files:
├── package.json          (Dependencies list)
├── src/                  (Your code)
├── node_modules/         (Downloaded packages)
├── start.bat             (Easy start script)
└── INSTALL_NODEJS.md     (This file)
```

---

## 📊 What Gets Installed

### When you run `npm install`:

- **react** - UI framework
- **typescript** - Type safety
- **vite** - Build tool
- **react-router** - Navigation
- **axios** - API calls
- **zustand** - State management
- **chart.js** - Charts
- Plus 20+ other packages

### Total Size: ~400MB (node_modules folder)

### Time: 5-10 minutes (first time)

---

## 🎓 Understanding the Process

### npm install
- Reads `package.json`
- Downloads all dependencies
- Installs them in `node_modules/`
- Creates `package-lock.json` (lock file)

### npm run dev
- Starts Vite development server
- Watches for file changes
- Auto-reloads in browser
- Opens http://localhost:3000

### Hot Module Replacement (HMR)
- When you edit code, changes appear instantly
- No need to refresh browser
- Very fast development experience

---

## 🎯 Quick Reference

```bash
# Check if Node.js is installed
node --version

# Check if npm is installed
npm --version

# Navigate to project
cd "C:\Users\kunal\OneDrive\Desktop\DeepRow UI"

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Stop development server
# Press: Ctrl + C
```

---

## 🌐 Ports & URLs

| Service | URL | Port |
|---------|-----|------|
| Dev Server | http://localhost:3000 | 3000 |
| Alternate | http://localhost:3001 | 3001 |
| Local IP | http://192.168.x.x:3000 | 3000 |

---

## 💡 Pro Tips

1. **Keep it running:** Leave `npm run dev` running while coding
2. **Auto-reload:** Edits auto-save to browser
3. **Console logs:** Check browser console (F12) for errors
4. **Errors:** Read error messages - they're usually clear
5. **Speed:** First `npm install` is slowest

---

## ⏱️ Time Estimate

| Step | Time |
|------|------|
| Download Node.js | 2 min |
| Install Node.js | 3 min |
| Restart computer | 2 min |
| npm install | 5-10 min |
| npm run dev | 30 sec |
| **Total** | **~15 minutes** |

---

## ✨ Success Indicators

✅ You'll know it's working when:
- `npm install` completes without errors
- `npm run dev` shows "Local: http://localhost:3000"
- Browser opens your application
- You can see the login page
- Sidebar navigation visible
- Clicking links changes the page

---

## 🆘 Need Help?

### Check These Files:
1. **INSTALL_NODEJS.md** - Node.js installation
2. **START_HERE.md** - Quick start
3. **README.md** - Features overview
4. **QUICK_REFERENCE.md** - Common commands

### Online Resources:
- Node.js Docs: https://nodejs.org/
- npm Docs: https://docs.npmjs.com/
- Vite Docs: https://vitejs.dev/
- React Docs: https://react.dev/

---

## ✅ Ready to Go?

Once Node.js is installed:

```bash
cd "C:\Users\kunal\OneDrive\Desktop\DeepRow UI"
npm install
npm run dev
```

**Then visit: http://localhost:3000** 🎉

---

**Everything will work perfectly once Node.js is installed!**

It's just a one-time setup, then you're good to go! 🚀
