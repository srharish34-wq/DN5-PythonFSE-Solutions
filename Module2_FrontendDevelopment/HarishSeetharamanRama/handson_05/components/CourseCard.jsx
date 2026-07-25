

export default function CourseCard({ id, name, code, credits, grade, onEnroll, isEnrolled }) {
  return (
    <article style={{
      background: '#fff',
      padding: '20px',
      border: '1px solid #e0e0e0',
      borderRadius: '8px',
      boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
      display: 'flex',
      flexDirection: 'column',
      gap: '8px'
    }}>
      <h3 style={{ color: '#1a237e', fontSize: '1rem' }}>{name}</h3>
      <p style={{ color: '#666', fontSize: '0.85rem' }}>Code: {code}</p>

      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
        <span style={{
          background: '#e8eaf6', color: '#1a237e',
          padding: '3px 10px', borderRadius: '20px', fontSize: '0.8rem', fontWeight: 'bold'
        }}>
          {credits} Credits
        </span>
        <span style={{
          background: '#e8f5e9', color: '#2e7d32',
          padding: '3px 10px', borderRadius: '20px', fontSize: '0.8rem', fontWeight: 'bold'
        }}>
          Grade: {grade}
        </span>
      </div>

      {/* Enroll button — handler passed as prop from App.jsx (lifting state up) */}
      <button
        onClick={() => onEnroll({ id, name, code, credits, grade })}
        disabled={isEnrolled}
        style={{
          marginTop: '8px',
          padding: '8px 16px',
          background: isEnrolled ? '#ccc' : '#1a237e',
          color: '#fff',
          border: 'none',
          borderRadius: '6px',
          cursor: isEnrolled ? 'not-allowed' : 'pointer',
          fontSize: '0.9rem',
          transition: 'background 0.2s'
        }}
      >
        {isEnrolled ? '✅ Enrolled' : 'Enroll'}
      </button>
    </article>
  );
}
