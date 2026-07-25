<!-- ============================================================
Hands-On 8 — Vue.js CoursesView with Composition API
src/views/CoursesView.vue
Cognizant DN5.0 | Harish Seetharaman Rama
============================================================ -->

<template>
  <div class="courses-view">
    <h2>Available Courses</h2>

    <!-- v-model binds input to searchTerm ref -->
    <input
      v-model="searchTerm"
      placeholder="🔍 Search courses..."
      class="search-input"
    />

    <!-- v-for renders each course card -->
    <div class="course-grid">
      <CourseCard
        v-for="course in filteredCourses"
        :key="course.id"
        :id="course.id"
        :name="course.name"
        :code="course.code"
        :credits="course.credits"
        :grade="course.grade"
      />
    </div>

    <!-- Show when no results -->
    <p v-if="filteredCourses.length === 0" class="empty-msg">
      No courses found.
    </p>

    <!-- Total credits from Pinia store -->
    <p class="total">
      Total Enrolled Credits: <strong>{{ store.totalCredits }}</strong>
    </p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useEnrollmentStore } from '../stores/enrollment'
import CourseCard from '../components/CourseCard.vue'

const store      = useEnrollmentStore()
const searchTerm = ref('')

// Reactive courses array
const courses = ref([])

// onMounted — runs after component is mounted (like useEffect with [])
onMounted(() => {
  courses.value = [
    { id: 1, name: 'Data Structures & Algorithms', code: 'CS101', credits: 4, grade: 'A' },
    { id: 2, name: 'Database Management Systems',  code: 'CS102', credits: 3, grade: 'B' },
    { id: 3, name: 'Object Oriented Programming',  code: 'CS103', credits: 4, grade: 'A' },
    { id: 4, name: 'Web Development Fundamentals', code: 'CS104', credits: 3, grade: 'B' },
    { id: 5, name: 'Python Backend Frameworks',    code: 'CS105', credits: 4, grade: 'A' },
  ]
})

// computed() is cached — only re-runs when searchTerm or courses changes
// Unlike a method which runs on every render
const filteredCourses = computed(() =>
  courses.value.filter(c =>
    c.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
)
</script>

<style scoped>
.courses-view { max-width: 1200px; margin: 0 auto; padding: 32px; }
h2 { color: #1a237e; margin-bottom: 24px; }
.search-input {
  width: 100%; max-width: 360px;
  padding: 10px 16px; border: 1px solid #ccc;
  border-radius: 6px; font-size: 1rem; margin-bottom: 24px; display: block;
}
.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
}
.empty-msg { text-align: center; color: #999; margin-top: 32px; }
.total { margin-top: 24px; color: #1a237e; font-size: 1.1rem; }
</style>
