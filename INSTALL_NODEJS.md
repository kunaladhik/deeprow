# ⚠️ IMPORTANT: Install Node.js First!

## Node.js is Not Installed

Your system doesn't have Node.js (which includes npm) installed yet. This is required to run the React application.

---

## 🚀 How to Install Node.js

### Step 1: Download Node.js

1. Go to: **https://nodejs.org/**
2. Download the **LTS (Long Term Support)** version
   - Look for the green "LTS" button
   - Choose the version for Windows

### Step 2: Install Node.js

1. Run the installer you just downloaded
2. Follow the installation wizard
3. Accept all default settings
4. Choose to install npm (should be selected by default)
5. Click "Install" and wait for completion

### Step 3: Verify Installation

Open PowerShell and run:
```bash
node --version
npm --version
```

You should see version numbers like:
```
v18.x.x
9.x.x
```

---

## ✅ Once Node.js is Installed

Then run these commands in PowerShell:

```bash
# Navigate to your project
cd "C:\Users\kunal\OneDrive\Desktop\DeepRow UI"

# Install dependencies
npm install

# Start development server
npm run dev
```

Your application will open at: **http://localhost:3000**

---

## 📥 Download Link

**Direct Download:** https://nodejs.org/en/download/

Choose:
- Windows Installer (.msi)
- LTS version (Recommended)
- 64-bit (if you have 64-bit Windows)

---

## 🔧 Installation Tips

- The installer is about 100MB
- Installation takes 2-3 minutes
- You may need to restart your computer
- Run PowerShell **as Administrator** if needed

---

## ❓ Still Having Issues?

### Issue: "npm: The term 'npm' is not recognized"
**Solution:** Node.js is not installed or needs a restart
1. Install Node.js from nodejs.org
2. Restart your computer
3. Open a fresh PowerShell window

### Issue: "npm install takes too long"
**Solution:** This is normal! 
- First install can take 5-10 minutes
- Dependencies are large (node_modules folder)
- Wait for it to complete

### Issue: "Port 3000 already in use"
**Solution:** Use a different port
```bash
npm run dev -- --port 3001
```

---

## 📋 Checklist

- [ ] Downloaded Node.js LTS from nodejs.org
- [ ] Installed Node.js
- [ ] Restarted computer
- [ ] Verified with: node --version
- [ ] Verified with: npm --version
- [ ] Ready to run: npm install && npm run dev

---

## 🎯 Next Steps

1. **Install Node.js** from https://nodejs.org/
2. **Verify installation** with the version commands above
3. **Run in your project folder:**
   ```bash
   npm install
   npm run dev
   ```
4. **Visit** http://localhost:3000 in your browser

---

**Once Node.js is installed, your React app will work perfectly!** ✨

Questions? Check the documentation in your project folder.
