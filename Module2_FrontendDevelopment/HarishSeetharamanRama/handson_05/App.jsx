

import { useState, useEffect } from 'react';

const localCourses = [
  { id:1, name:'Data Structures & Algorithms', code:'CS101', credits:4, grade:'A' },
  { id:2, name:'Database Management Systems',  code:'CS102', credits:3, grade:'B' },
  { id:3, name:'Object Oriented Programming',  code:'CS103', credits:4, grade:'A' },
  { id:4, name:'Web Development Fundamentals', code:'CS104', credits:3, grade:'B' },
  { id:5, name:'Python Backend Frameworks',    code:'CS105', credits:4, grade:'A' },
];

// ── Header Component ──────────────────────────────────────
function Header({ siteName, enrolledCount }) {
  return (
    <header style={{ background:'#1a237e', color:'#fff', padding:'16px 32px',
      display:'flex', justifyContent:'space-between', alignItems:'center' }}>
      <div style={{ fontSize:'1.4rem', fontWeight:'bold' }}>🎓 {siteName}</div>
      <nav style={{ display:'flex', gap:'20px', alignItems:'center' }}>
        <a href="#" style={{ color:'#fff', textDecoration:'none' }}>Home</a>
        <a href="#" style={{ color:'#fff', textDecoration:'none' }}>Courses</a>
        <a href="#" style={{ color:'#fff', textDecoration:'none' }}>Profile</a>
        {enrolledCount > 0 && (
          <span style={{ background:'#ff5722', padding:'2px 10px',
            borderRadius:'20px', fontSize:'0.85rem' }}>
            {enrolledCount} Enrolled
          </span>
        )}
      </nav>
    </header>
  );
}

// ── Footer Component ──────────────────────────────────────
function Footer() {
  return (
    <footer style={{ background:'#1a237e', color:'#fff',
      textAlign:'center', padding:'20px', marginTop:'40px' }}>
      <p>&copy; 2024 Student Portal — Cognizant DN5.0 | Harish Seetharaman Rama</p>
    </footer>
  );
}

// ── CourseCard Component ──────────────────────────────────
// Props: id, name, code, credits, grade, onEnroll, isEnrolled
function CourseCard({ id, name, code, credits, grade, onEnroll, isEnrolled }) {
  return (
    <article style={{ background:'#fff', padding:'20px',
      border:'1px solid #e0e0e0', borderRadius:'8px',
      boxShadow:'0 2px 8px rgba(0,0,0,0.08)',
      display:'flex', flexDirection:'column', gap:'8px' }}>
      <h3 style={{ color:'#1a237e', fontSize:'1rem' }}>{name}</h3>
      <p style={{ color:'#666', fontSize:'0.85rem' }}>Code: {code}</p>
      <div style={{ display:'flex', gap:'8px' }}>
        <span style={{ background:'#e8eaf6', color:'#1a237e',
          padding:'3px 10px', borderRadius:'20px', fontSize:'0.8rem', fontWeight:'bold' }}>
          {credits} Credits
        </span>
        <span style={{ background:'#e8f5e9', color:'#2e7d32',
          padding:'3px 10px', borderRadius:'20px', fontSize:'0.8rem', fontWeight:'bold' }}>
          Grade: {grade}
        </span>
      </div>
      {/* onEnroll prop — handler lifted up to App.jsx */}
      <button
        onClick={() => onEnroll({ id, name, code, credits, grade })}
        disabled={isEnrolled}
        style={{ marginTop:'8px', padding:'8px 16px',
          background: isEnrolled ? '#ccc' : '#1a237e',
          color:'#fff', border:'none', borderRadius:'6px',
          cursor: isEnrolled ? 'not-allowed' : 'pointer' }}>
        {isEnrolled ? '✅ Enrolled' : 'Enroll'}
      </button>
    </article>
  );
}

// ── Main App Component ────────────────────────────────────
export default function App() {
  const [courses,          setCourses]         = useState([]);
  const [enrolledCourses,  setEnrolledCourses] = useState([]);
  const [searchTerm,       setSearchTerm]      = useState('');
  const [loading,          setLoading]         = useState(true);
  const [error,            setError]           = useState(null);

  // useEffect [] = runs once after mount (like componentDidMount)
  useEffect(() => {
    async function loadCourses() {
      try {
        const res   = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5');
        const posts = await res.json();
        const mapped = posts.map((post, i) => ({
          id     : post.id,
          name   : localCourses[i]?.name   || post.title,
          code   : localCourses[i]?.code   || `C${post.id}`,
          credits: localCourses[i]?.credits || 3,
          grade  : localCourses[i]?.grade   || 'N/A',
        }));
        setCourses(mapped);
      } catch(err) {
        setError('Failed to load. Using local data.');
        setCourses(localCourses);
      } finally {
        setLoading(false);
      }
    }
    loadCourses();
  }, []);

  // Log when courses update — dependency array matters!
  // Without [], this runs after EVERY render → infinite loop risk
  useEffect(() => {
    if (courses.length > 0) console.log('Courses updated:', courses.length);
  }, [courses]);

  function handleEnroll(course) {
    if (!enrolledCourses.find(c => c.id === course.id)) {
      setEnrolledCourses(prev => [...prev, course]);
    }
  }

  const filteredCourses = courses.filter(c =>
    c.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <Header siteName="Student Portal" enrolledCount={enrolledCourses.length} />
      <main style={{ maxWidth:'1200px', margin:'0 auto', padding:'32px' }}>
        <h2 style={{ color:'#1a237e', marginBottom:'24px' }}>Available Courses</h2>
        <input
          type="text"
          placeholder="🔍 Search courses..."
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
          style={{ padding:'10px 16px', width:'100%', maxWidth:'400px',
            border:'1px solid #ccc', borderRadius:'6px', fontSize:'1rem',
            marginBottom:'24px', display:'block' }}
        />
        {loading && <p style={{ color:'#1a237e' }}>Loading courses...</p>}
        {error   && <p style={{ color:'orange' }}>{error}</p>}
        <div style={{ display:'grid',
          gridTemplateColumns:'repeat(auto-fit, minmax(260px, 1fr))', gap:'20px' }}>
          {/* key must use stable ID — never array index */}
          {filteredCourses.map(course => (
            <CourseCard
              key={course.id}
              {...course}
              onEnroll={handleEnroll}
              isEnrolled={!!enrolledCourses.find(c => c.id === course.id)}
            />
          ))}
        </div>
        {filteredCourses.length === 0 && !loading && (
          <p style={{ textAlign:'center', color:'#999', marginTop:'32px' }}>No courses found.</p>
        )}
        {enrolledCourses.length > 0 && (
          <div style={{ marginTop:'40px' }}>
            <h3 style={{ color:'#1a237e', marginBottom:'16px' }}>
              ✅ Enrolled Courses ({enrolledCourses.length})
            </h3>
            <ul style={{ listStyle:'none', padding:0 }}>
              {enrolledCourses.map(c => (
                <li key={c.id} style={{ background:'#e8eaf6', padding:'10px 16px',
                  borderRadius:'6px', marginBottom:'8px', color:'#1a237e' }}>
                  {c.name} — {c.credits} Credits
                </li>
              ))}
            </ul>
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}
