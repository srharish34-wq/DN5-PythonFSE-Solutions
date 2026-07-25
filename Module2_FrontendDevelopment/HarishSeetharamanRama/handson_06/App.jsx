

import { BrowserRouter, Routes, Route, Link, useParams, useNavigate } from 'react-router-dom';
import { createContext, useContext, useState } from 'react';
import { configureStore, createSlice } from '@reduxjs/toolkit';
import { Provider, useSelector, useDispatch } from 'react-redux';

// ── Sample Data ───────────────────────────────────────────
const coursesData = [
  { id: 1, name: 'Data Structures & Algorithms', code: 'CS101', credits: 4, grade: 'A' },
  { id: 2, name: 'Database Management Systems',  code: 'CS102', credits: 3, grade: 'B' },
  { id: 3, name: 'Object Oriented Programming',  code: 'CS103', credits: 4, grade: 'A' },
  { id: 4, name: 'Web Development Fundamentals', code: 'CS104', credits: 3, grade: 'B' },
  { id: 5, name: 'Python Backend Frameworks',    code: 'CS105', credits: 4, grade: 'A' },
];

// ============================================================
// TASK 2: Context API for Global State
// ============================================================
export const EnrollmentContext = createContext();

export function EnrollmentProvider({ children }) {
  const [enrolledCourses, setEnrolledCourses] = useState([]);

  function enroll(course) {
    setEnrolledCourses(prev =>
      prev.find(c => c.id === course.id) ? prev : [...prev, course]
    );
  }

  function unenroll(courseId) {
    setEnrolledCourses(prev => prev.filter(c => c.id !== courseId));
  }

  return (
    <EnrollmentContext.Provider value={{ enrolledCourses, enroll, unenroll }}>
      {children}
    </EnrollmentContext.Provider>
  );
}

// ============================================================
// TASK 3: Redux Toolkit
// ============================================================
const enrollmentSlice = createSlice({
  name: 'enrollment',
  initialState: { enrolledCourses: [] },
  reducers: {
    enroll(state, action) {
      if (!state.enrolledCourses.find(c => c.id === action.payload.id)) {
        state.enrolledCourses.push(action.payload);
      }
    },
    unenroll(state, action) {
      state.enrolledCourses = state.enrolledCourses.filter(c => c.id !== action.payload);
    },
  },
});

export const { enroll, unenroll } = enrollmentSlice.actions;

export const store = configureStore({
  reducer: { enrollment: enrollmentSlice.reducer }
});

// Selectors
export const selectCourses   = state => state.enrollment.enrolledCourses;
export const selectCount     = state => state.enrollment.enrolledCourses.length;


// ============================================================
// COMPONENTS
// ============================================================

function NavBar() {
  const count = useSelector(selectCount);
  return (
    <header style={{
      background: '#1a237e', color: '#fff',
      padding: '16px 32px',
      display: 'flex', justifyContent: 'space-between', alignItems: 'center'
    }}>
      <div style={{ fontSize: '1.4rem', fontWeight: 'bold' }}>🎓 Student Portal</div>
      <nav style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
        {/* Link prevents full page reload */}
        <Link to="/"        style={{ color: '#fff', textDecoration: 'none' }}>Home</Link>
        <Link to="/courses" style={{ color: '#fff', textDecoration: 'none' }}>Courses</Link>
        <Link to="/profile" style={{ color: '#fff', textDecoration: 'none' }}>Profile</Link>
        {count > 0 && (
          <span style={{
            background: '#ff5722', padding: '2px 10px',
            borderRadius: '20px', fontSize: '0.85rem'
          }}>
            {count} Enrolled
          </span>
        )}
      </nav>
    </header>
  );
}

// Home Page
function HomePage() {
  return (
    <div style={{ textAlign: 'center', padding: '80px 32px', background: 'linear-gradient(135deg,#1a237e,#283593)', color: '#fff' }}>
      <h1 style={{ fontSize: '2.5rem', marginBottom: '16px' }}>Welcome to Student Portal</h1>
      <p style={{ marginBottom: '24px', opacity: 0.9 }}>Manage your courses, grades and profile.</p>
      <Link to="/courses" style={{
        padding: '12px 32px', border: '2px solid #fff', borderRadius: '6px',
        color: '#fff', textDecoration: 'none', fontSize: '1rem'
      }}>Explore Courses</Link>
    </div>
  );
}

// Courses Page
function CoursesPage() {
  const dispatch = useDispatch();
  const enrolled = useSelector(selectCourses);

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '32px' }}>
      <h2 style={{ color: '#1a237e', marginBottom: '24px' }}>Available Courses</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(260px,1fr))', gap: '20px' }}>
        {coursesData.map(course => {
          const isEnrolled = enrolled.find(c => c.id === course.id);
          return (
            <article key={course.id} style={{
              background: '#fff', padding: '20px', borderRadius: '8px',
              border: '1px solid #e0e0e0', boxShadow: '0 2px 8px rgba(0,0,0,0.08)'
            }}>
              <h3 style={{ color: '#1a237e', marginBottom: '8px' }}>{course.name}</h3>
              <p style={{ color: '#666', fontSize: '0.9rem', marginBottom: '12px' }}>
                {course.code} | {course.credits} Credits
              </p>
              <div style={{ display: 'flex', gap: '8px' }}>
                {/* Link to course detail — useParams in detail page */}
                <Link to={`/courses/${course.id}`} style={{
                  padding: '6px 14px', background: '#e8eaf6', color: '#1a237e',
                  borderRadius: '4px', textDecoration: 'none', fontSize: '0.85rem'
                }}>View Details</Link>
                <button
                  onClick={() => dispatch(enroll(course))}
                  disabled={!!isEnrolled}
                  style={{
                    padding: '6px 14px',
                    background: isEnrolled ? '#ccc' : '#1a237e',
                    color: '#fff', border: 'none', borderRadius: '4px',
                    cursor: isEnrolled ? 'not-allowed' : 'pointer', fontSize: '0.85rem'
                  }}
                >
                  {isEnrolled ? '✅ Enrolled' : 'Enroll'}
                </button>
              </div>
            </article>
          );
        })}
      </div>
    </div>
  );
}

// Course Detail Page — useParams
function CourseDetailPage() {
  const { courseId } = useParams();   // reads :courseId from URL
  const navigate     = useNavigate();
  const dispatch     = useDispatch();
  const course       = coursesData.find(c => c.id === parseInt(courseId));

  if (!course) return <p style={{ padding: '32px', color: 'red' }}>Course not found.</p>;

  function handleEnroll() {
    dispatch(enroll(course));
    navigate('/profile');  // navigate to profile after enrolling
  }

  return (
    <div style={{ maxWidth: '600px', margin: '40px auto', padding: '32px',
      background: '#fff', borderRadius: '8px', boxShadow: '0 2px 16px rgba(0,0,0,0.1)' }}>
      <h2 style={{ color: '#1a237e', marginBottom: '16px' }}>{course.name}</h2>
      <p><strong>Code:</strong> {course.code}</p>
      <p><strong>Credits:</strong> {course.credits}</p>
      <p><strong>Grade:</strong> {course.grade}</p>
      <div style={{ marginTop: '24px', display: 'flex', gap: '12px' }}>
        <button onClick={handleEnroll} style={{
          padding: '10px 24px', background: '#1a237e', color: '#fff',
          border: 'none', borderRadius: '6px', cursor: 'pointer'
        }}>Enroll & Go to Profile</button>
        <button onClick={() => navigate(-1)} style={{
          padding: '10px 24px', background: '#e0e0e0', color: '#333',
          border: 'none', borderRadius: '6px', cursor: 'pointer'
        }}>← Back</button>
      </div>
    </div>
  );
}

// Profile Page
function ProfilePage() {
  const enrolled = useSelector(selectCourses);
  const dispatch = useDispatch();

  return (
    <div style={{ maxWidth: '700px', margin: '40px auto', padding: '32px' }}>
      <h2 style={{ color: '#1a237e', marginBottom: '24px' }}>My Profile</h2>
      <h3 style={{ marginBottom: '16px' }}>Enrolled Courses ({enrolled.length})</h3>
      {enrolled.length === 0
        ? <p style={{ color: '#999' }}>No courses enrolled yet.</p>
        : enrolled.map(c => (
          <div key={c.id} style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            background: '#e8eaf6', padding: '12px 16px', borderRadius: '6px', marginBottom: '8px'
          }}>
            <span style={{ color: '#1a237e', fontWeight: 'bold' }}>{c.name}</span>
            <button onClick={() => dispatch(unenroll(c.id))} style={{
              padding: '4px 12px', background: '#c62828', color: '#fff',
              border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '0.8rem'
            }}>Remove</button>
          </div>
        ))
      }
    </div>
  );
}

// ============================================================
// MAIN APP — Wrap with Provider and BrowserRouter
// ============================================================
export default function App() {
  return (
    <Provider store={store}>
      <BrowserRouter>
        <NavBar />
        <Routes>
          <Route path="/"                  element={<HomePage />} />
          <Route path="/courses"           element={<CoursesPage />} />
          <Route path="/courses/:courseId" element={<CourseDetailPage />} />
          <Route path="/profile"           element={<ProfilePage />} />
        </Routes>
        <footer style={{
          background: '#1a237e', color: '#fff',
          textAlign: 'center', padding: '20px', marginTop: '40px'
        }}>
          <p>&copy; 2024 Student Portal — Cognizant DN5.0 | Harish Seetharaman Rama</p>
        </footer>
      </BrowserRouter>
    </Provider>
  );
}
