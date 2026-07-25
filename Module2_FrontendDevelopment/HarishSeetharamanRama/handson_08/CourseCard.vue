<!-- ============================================================
Hands-On 8 — Vue.js: Composition API, Vue Router & Pinia
CourseCard.vue
Cognizant DN5.0 | Harish Seetharaman Rama

SETUP:
  npm create vue@latest student-portal-vue
  (select: Vue Router yes, Pinia yes)
  cd student-portal-vue && npm install && npm run dev
============================================================ -->

<template>
  <article class="course-card">
    <h3>{{ name }}</h3>
    <p>{{ code }} | {{ credits }} Credits</p>
    <div class="badges">
      <span class="badge credits-badge">{{ credits }} Credits</span>
      <span class="badge grade-badge">Grade: {{ grade }}</span>
    </div>
    <button
      @click="handleEnroll"
      :disabled="isEnrolled"
      :class="isEnrolled ? 'btn-enrolled' : 'btn-enroll'"
    >
      {{ isEnrolled ? '✅ Enrolled' : 'Enroll' }}
    </button>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { useEnrollmentStore } from '../stores/enrollment'

// defineProps — declare props with types
const props = defineProps({
  id     : Number,
  name   : String,
  code   : String,
  credits: Number,
  grade  : String,
})

const store     = useEnrollmentStore()
const isEnrolled = computed(() =>
  store.enrolledCourses.some(c => c.id === props.id)
)

function handleEnroll() {
  store.enroll({ id: props.id, name: props.name, code: props.code, credits: props.credits, grade: props.grade })
}
</script>

<style scoped>
.course-card {
  background: #fff;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  display: flex;
  flex-direction: column;
  gap: 10px;
}
h3 { color: #1a237e; font-size: 1rem; }
p  { color: #666; font-size: 0.85rem; }
.badges { display: flex; gap: 8px; flex-wrap: wrap; }
.badge {
  padding: 3px 10px; border-radius: 20px;
  font-size: 0.8rem; font-weight: bold;
}
.credits-badge { background: #e8eaf6; color: #1a237e; }
.grade-badge   { background: #e8f5e9; color: #2e7d32; }
.btn-enroll {
  padding: 8px 16px; background: #1a237e; color: #fff;
  border: none; border-radius: 6px; cursor: pointer; font-size: 0.9rem;
}
.btn-enrolled {
  padding: 8px 16px; background: #ccc; color: #fff;
  border: none; border-radius: 6px; cursor: not-allowed; font-size: 0.9rem;
}
</style>
