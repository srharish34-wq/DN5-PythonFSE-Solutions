

export default function Header({ siteName, enrolledCount }) {
  return (
    <header style={{
      background: '#1a237e', color: '#fff',
      padding: '16px 32px',
      display: 'flex', justifyContent: 'space-between', alignItems: 'center',
      position: 'sticky', top: 0, zIndex: 100
    }}>
      <div style={{ fontSize: '1.4rem', fontWeight: 'bold' }}>
        🎓 {siteName}
      </div>
      <nav style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
        <a href="/" style={{ color: '#fff', textDecoration: 'none' }}>Home</a>
        <a href="/courses" style={{ color: '#fff', textDecoration: 'none' }}>Courses</a>
        <a href="/profile" style={{ color: '#fff', textDecoration: 'none' }}>Profile</a>
        {enrolledCount > 0 && (
          <span style={{
            background: '#ff5722', color: '#fff',
            borderRadius: '20px', padding: '2px 10px', fontSize: '0.85rem'
          }}>
            {enrolledCount} Enrolled
          </span>
        )}
      </nav>
    </header>
  );
}
