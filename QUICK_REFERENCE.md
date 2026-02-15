# ⚡ Quick Reference Guide

## 🚀 Quick Start (Copy & Paste)

```bash
# 1. Navigate to project
cd "C:\Users\kunal\OneDrive\Desktop\DeepRow UI"

# 2. Install dependencies
npm install

# 3. Start development
npm run dev

# 4. Open browser
http://localhost:3000
```

---

## 📱 Pages & Routes

| Page | Route | File | Features |
|------|-------|------|----------|
| Login | `/login` | `Login.tsx` | Email/password form |
| Dashboard | `/dashboard` | `Dashboard.tsx` | Metrics, charts, insights |
| Upload | `/upload` | `FileUpload.tsx` | Drag-drop, CSV/Excel |
| Data Review | `/data-review` | `DataIssueReview.tsx` | Issues, quality score |
| Builder | `/builder` | `DashboardBuilder.tsx` | Widget selector, canvas |
| Transparency | `/transparency` | `LogicTransparency.tsx` | AI reasoning, confidence |

---

## 🎨 Colors & Branding

```
Primary:    #6366f1 (Indigo)
Secondary:  #8b5cf6 (Purple)
Success:    #10b981 (Green)
Warning:    #f59e0b (Amber)
Danger:     #ef4444 (Red)
Background: #f8fafc (Light Gray)
```

---

## 📁 Where to Edit

### Add New Page
1. Create file: `src/pages/YourPage.tsx`
2. Create style: `src/styles/yourpage.css`
3. Add route in `src/App.tsx`
4. Add nav link in `src/components/Layout.tsx`

### Change Navigation
Edit: `src/components/Layout.tsx`

### Change Colors/Styling
Edit: `src/styles/index.css` (CSS variables)

### Change Layout
Edit: `src/components/Layout.tsx` (sidebar)

### Add Dependencies
```bash
npm install package-name
```

---

## 🔧 Common Tasks

### View All Files
```powershell
# From project root:
dir /s
```

### Edit in VS Code
```powershell
code "C:\Users\kunal\OneDrive\Desktop\DeepRow UI"
```

### Clean Install
```bash
# Delete node_modules
rmdir /s node_modules

# Reinstall
npm install
```

### Check Dependencies
```bash
npm list
npm outdated
```

### Format Code
```bash
npm run lint
```

---

## 📚 File Locations

```
Project Root
├── 📄 package.json           (Dependencies)
├── 📄 tsconfig.json          (TypeScript)
├── 📄 vite.config.ts         (Build config)
├── 📄 index.html             (HTML template)
│
├── 📁 src/
│   ├── 📄 App.tsx            (Routes)
│   ├── 📄 main.tsx           (Entry point)
│   ├── 📁 pages/             (6 pages)
│   ├── 📁 components/        (Layout)
│   ├── 📁 styles/            (CSS)
│   ├── 📁 store/             (Zustand)
│   └── 📁 utils/             (Helpers)
│
├── 📁 dist/                  (Production build)
├── 📁 node_modules/          (Dependencies)
└── 📄 README.md              (Docs)
```

---

## 🎯 Component Structure

```typescript
// Basic page template
import '../styles/pagename.css'

export default function PageName() {
  return (
    <div className="page">
      <h1>Page Title</h1>
      {/* Content */}
    </div>
  )
}
```

---

## 🔌 Connect to API

```typescript
import axios from 'axios'

// In your component:
const fetchData = async () => {
  try {
    const res = await axios.get('/api/endpoint')
    console.log(res.data)
  } catch (error) {
    console.error(error)
  }
}

// Call it:
useEffect(() => {
  fetchData()
}, [])
```

---

## 📦 NPM Commands

```bash
npm install              # Install dependencies
npm run dev             # Start dev server (localhost:3000)
npm run build           # Production build
npm run preview         # Preview production
npm run lint            # Check code
npm update              # Update packages
npm list                # Show dependencies
npm outdated            # Show outdated packages
npm install --save pkg  # Add dependency
npm uninstall pkg       # Remove dependency
```

---

## 🎨 CSS Variables Reference

```css
/* In any CSS file */
color: var(--primary-color);
background: var(--secondary-color);
background: var(--success-color);
background: var(--warning-color);
background: var(--danger-color);
background: var(--bg-color);
background: var(--card-bg);
color: var(--text-dark);
color: var(--text-light);
border-color: var(--border-color);
```

---

## 🖼️ UI Component Examples

### Button
```tsx
<button className="btn btn-primary">Click Me</button>
```

### Card
```tsx
<div className="metric-card">
  <div className="metric-icon">📊</div>
  <div className="metric-content">
    <p className="metric-title">Title</p>
    <p className="metric-value">Value</p>
  </div>
</div>
```

### Form
```tsx
<form onSubmit={handleSubmit}>
  <div className="form-group">
    <label>Label</label>
    <input type="text" />
  </div>
  <button type="submit">Submit</button>
</form>
```

### Table
```tsx
<table>
  <thead>
    <tr><th>Column</th></tr>
  </thead>
  <tbody>
    <tr><td>Data</td></tr>
  </tbody>
</table>
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use different port
npm run dev -- --port 3001
```

### Dependencies Error
```bash
# Clear and reinstall
npm install --force
```

### Build Error
```bash
# Clear cache
npm cache clean --force
npm install
npm run build
```

### Module Not Found
```bash
# Check file exists
dir src/pages/YourPage.tsx

# Check import path
import YourPage from './pages/YourPage'  // Correct path
```

---

## 🚀 Deploy Checklist

- [ ] `npm run build` completes without errors
- [ ] `dist/` folder created
- [ ] No TypeScript errors
- [ ] All pages load correctly
- [ ] No console errors
- [ ] Images & assets load
- [ ] Responsive on mobile
- [ ] Navigation works
- [ ] Forms functional
- [ ] API calls working

---

## 📋 Testing Commands

```bash
# Build test
npm run build
npm run preview

# Type check
npx tsc --noEmit

# Lint check
npm run lint

# Performance check
# Use Lighthouse in Chrome DevTools
```

---

## 💾 Project Info

**Project Name:** AI Analytics Dashboard  
**Framework:** React 18 + TypeScript  
**Build Tool:** Vite  
**Node Version:** 16+  
**Status:** ✅ Ready for Development  

---

## 🔗 Quick Links

- **React Docs:** https://react.dev
- **Vite Docs:** https://vitejs.dev
- **Router Docs:** https://reactrouter.com
- **TypeScript:** https://www.typescriptlang.org
- **Chart.js:** https://www.chartjs.org
- **Zustand:** https://github.com/pmndrs/zustand

---

## ✨ Pro Tips

1. **Hot Reload:** Changes auto-reload in dev mode
2. **TypeScript:** Hover over variables for type hints
3. **DevTools:** Use React DevTools extension
4. **Console:** Check browser console for errors
5. **Network:** Use DevTools Network tab to debug API calls
6. **Storage:** LocalStorage for user preferences
7. **Performance:** Use Lighthouse in Chrome DevTools

---

## 🎓 Learning Paths

### Beginner
- [ ] Understand React basics
- [ ] Learn about props & state
- [ ] Practice CSS styling
- [ ] Create simple components

### Intermediate
- [ ] Use React Router
- [ ] Handle forms
- [ ] Make API calls
- [ ] Implement state management

### Advanced
- [ ] Performance optimization
- [ ] Code splitting
- [ ] Error boundaries
- [ ] Custom hooks

---

## 📞 Getting Help

1. **Check Documentation:** README.md, SETUP.md, ARCHITECTURE.md
2. **Google the Error:** Copy error message to Google
3. **Stack Overflow:** Tag `reactjs` or `vite`
4. **GitHub Issues:** Search similar issues
5. **Community Discord:** React community channels

---

## ✅ You're Ready!

Everything is set up. Just run:

```bash
npm install && npm run dev
```

Then visit `http://localhost:3000` 🎉

---

**Last Updated:** 2026  
**Status:** ✅ Complete & Ready  
**Support:** See documentation files  
