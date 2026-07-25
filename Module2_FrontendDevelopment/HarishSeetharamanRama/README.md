# Module 2 — Frontend Development
## Cognizant DN5.0 | Harish Seetharaman Rama

---

## 📁 Folder Structure

```
Module2_FrontendDev/
└── HarishSeetharamanRama/
    ├── handson_01/          ← HTML5 Semantic + CSS3
    │   ├── index.html
    │   └── styles.css
    ├── handson_02/          ← Flexbox + Grid + Responsive
    │   └── index.html
    ├── handson_03/          ← JavaScript ES6 + DOM
    │   ├── index.html
    │   ├── app.js
    │   └── data.js
    ├── handson_04/          ← Async JS + Fetch + Axios
    │   └── index.html
    ├── handson_05/          ← React Components + Hooks
    │   ├── App.jsx
    │   └── components/
    │       ├── Header.jsx
    │       ├── Footer.jsx
    │       └── CourseCard.jsx
    ├── handson_06/          ← React Router + Redux Toolkit
    │   └── App.jsx
    ├── handson_07/          ← Angular Components + Services
    │   └── angular_notes.js
    ├── handson_08/          ← Vue.js Composition API + Pinia
    │   ├── CourseCard.vue
    │   ├── CoursesView.vue
    │   ├── enrollment.js
    │   └── router.js
    ├── handson_09/          ← Accessibility (a11y) + ARIA
    │   └── index.html
    └── handson_10/          ← API Layer + Redux Thunks
        └── apiClient.js
```

---

## 🚀 How to Run Each Hands-On

### Hands-On 1, 2, 3, 4 — Plain HTML/CSS/JS
Just open the `index.html` file directly in your browser!
```
Double-click index.html → Opens in Chrome/Firefox
```
For handson_03 (uses ES6 modules), run a local server:
```bash
cd handson_03
npx serve .
# Open http://localhost:3000
```

### Hands-On 5 — React
```bash
npm create vite@latest student-portal-react -- --template react
cd student-portal-react
npm install
# Copy App.jsx and components/ folder into src/
npm run dev
# Open http://localhost:5173
```

### Hands-On 6 — React + Router + Redux
```bash
# Inside the same React project from handson_05
npm install react-router-dom @reduxjs/toolkit react-redux
# Replace App.jsx with handson_06/App.jsx
npm run dev
```

### Hands-On 7 — Angular
```bash
npm install -g @angular/cli
ng new student-portal-angular --routing --style=css
cd student-portal-angular
# Follow comments in angular_notes.js
ng serve
# Open http://localhost:4200
```

### Hands-On 8 — Vue.js + Pinia
```bash
npm create vue@latest student-portal-vue
# Select: Vue Router YES, Pinia YES
cd student-portal-vue
npm install
# Copy Vue files into src/ folders
npm run dev
# Open http://localhost:5173
```

### Hands-On 9 — Accessibility
```bash
# Open index.html in Chrome
# Open DevTools → Lighthouse → Accessibility → Generate Report
```

### Hands-On 10 — API Layer + Redux Thunks
```bash
npm install axios @reduxjs/toolkit react-redux
# See comments in apiClient.js for full implementation
```

---

## 📚 Key Concepts Summary

| Hands-On | Topic | Key Takeaway |
|----------|-------|-------------|
| 1 | HTML5 + CSS3 | Semantic elements, box model, flexbox header |
| 2 | Responsive Design | CSS Grid auto-fit, media queries, mobile-first |
| 3 | JavaScript ES6 | map/filter/reduce, DOM manipulation, event delegation |
| 4 | Async JS | async/await, Promise.all, Fetch vs Axios |
| 5 | React Basics | Components, props, useState, useEffect |
| 6 | React Advanced | React Router, Context API, Redux Toolkit |
| 7 | Angular | DI, Services, Reactive Forms, *ngFor/*ngIf |
| 8 | Vue.js | Composition API, ref/computed, Pinia store |
| 9 | Accessibility | ARIA, tabindex, aria-live, contrast ratio |
| 10 | State + API | Axios interceptors, createAsyncThunk, Error Boundary |
