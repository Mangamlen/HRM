import React, {useState} from 'react';
import Login from './pages/Login';
import Employees from './pages/Employees';
import Attendance from './pages/Attendance';
import Reports from './pages/Reports';
import './App.css';

export default function App(){
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [view, setView] = useState('employees');
  if(!token){
    return <Login onLogin={(t)=>{setToken(t); localStorage.setItem('token', t);}} />;
  }
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>HRM Agriculture</h1>
        <nav className="app-nav">
          <button onClick={()=>setView('employees')}>Employees</button>
          <button onClick={()=>setView('attendance')}>Attendance</button>
          <button onClick={()=>setView('reports')}>Reports</button>
          <button className="logout-button" onClick={()=>{localStorage.removeItem('token'); setToken(null);}}>Logout</button>
        </nav>
      </header>
      <main className="app-main">
        {view==='employees' && <Employees token={token} />}
        {view==='attendance' && <Attendance token={token} />}
        {view==='reports' && <Reports token={token} />}
      </main>
    </div>
  );
}
