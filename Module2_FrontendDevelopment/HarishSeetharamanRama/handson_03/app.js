
import { courses } from './data.js';

// ── TASK 1: ES6+ Syntax ──────────────────────────────────

// map() → formatted strings using template literals
const formattedCourses = courses.map(({ name, code, credits }) =>
  `${code} — ${name} (${credits} credits)`
);
console.log('Formatted:', formattedCourses);

// filter() → courses with 4+ credits
const highCredit = courses.filter(({ credits }) => credits >= 4);
console.log('High credit count:', highCredit.length);

// reduce() → total credits
const totalCredits = courses.reduce((sum, { credits }) => sum + credits, 0);
console.log('Total credits:', totalCredits);

// ── TASK 2: DOM Rendering ────────────────────────────────

const courseGrid   = document.querySelector('.course-grid');
const totalCreditP = document.getElementById('total-credits');
const selectedDiv  = document.getElementById('selected-course');

function renderCourses(list) {
  courseGrid.innerHTML = '';

  if (list.length === 0) {
    courseGrid.innerHTML = '<p style="text-align:center;color:#999;grid-column:1/-1">No courses found.</p>';
    return;
  }

  const fragment = document.createDocumentFragment();
  list.forEach(course => {
    const article = document.createElement('article');
    article.className = 'course-card';
    article.dataset.id = course.id;
    article.tabIndex = 0;
    article.innerHTML = `
      <h3>${course.name}</h3>
      <p>Code: <strong>${course.code}</strong></p>
      <span class="credits">${course.credits} Credits</span>
      <span class="grade">Grade: ${course.grade}</span>
    `;
    fragment.appendChild(article);
  });
  courseGrid.appendChild(fragment);

  const shown = list.reduce((sum, c) => sum + c.credits, 0);
  totalCreditP.textContent = `Total Credits Shown: ${shown}`;
}

renderCourses(courses);
totalCreditP.textContent = `Total Credits: ${totalCredits}`;

// ── TASK 3: Event Listeners ──────────────────────────────

// Search input — filter on every keystroke
document.getElementById('search-courses').addEventListener('input', e => {
  const term     = e.target.value.toLowerCase();
  const filtered = courses.filter(c => c.name.toLowerCase().includes(term));
  renderCourses(filtered);
});

// Sort by Credits button
document.getElementById('sort-btn').addEventListener('click', () => {
  const sorted = [...courses].sort((a, b) => b.credits - a.credits);
  renderCourses(sorted);
});

// Event Delegation — single listener on grid for all card clicks
courseGrid.addEventListener('click', e => {
  const card = e.target.closest('.course-card');
  if (!card) return;
  const course = courses.find(c => c.id === parseInt(card.dataset.id));
  if (course && selectedDiv) {
    selectedDiv.textContent = `Selected: ${course.name} | Grade: ${course.grade} | ${course.credits} Credits`;
    selectedDiv.style.display = 'block';
  }
});

// Also handle keyboard Enter on cards
courseGrid.addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    const card = e.target.closest('.course-card');
    if (card) card.click();
  }
});
