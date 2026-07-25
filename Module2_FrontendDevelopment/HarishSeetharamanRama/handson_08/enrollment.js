

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useEnrollmentStore = defineStore('enrollment', () => {
  // ── State ──────────────────────────────────────────────
  const enrolledCourses = ref([])

  // ── Computed (getter) ──────────────────────────────────
  const totalCredits = computed(() =>
    enrolledCourses.value.reduce((sum, c) => sum + c.credits, 0)
  )

  const enrolledCount = computed(() => enrolledCourses.value.length)

  // ── Actions ────────────────────────────────────────────
  function enroll(course) {
    if (!enrolledCourses.value.find(c => c.id === course.id)) {
      enrolledCourses.value.push(course)
    }
  }

  function unenroll(courseId) {
    enrolledCourses.value = enrolledCourses.value.filter(c => c.id !== courseId)
  }

  // Advanced: fetch from API then enroll
  async function fetchAndEnroll(courseId) {
    try {
      const res    = await fetch(`https://jsonplaceholder.typicode.com/posts/${courseId}`)
      const post   = await res.json()
      const course = {
        id     : post.id,
        name   : post.title.substring(0, 30),
        code   : `C${post.id}`,
        credits: 3,
        grade  : 'N/A'
      }
      enroll(course)
    } catch (err) {
      console.error('fetchAndEnroll error:', err)
    }
  }

  // Reset all enrollment state
  function $reset() {
    enrolledCourses.value = []
  }

  return {
    enrolledCourses,
    totalCredits,
    enrolledCount,
    enroll,
    unenroll,
    fetchAndEnroll,
    $reset
  }
})
