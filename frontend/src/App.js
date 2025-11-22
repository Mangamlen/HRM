import React, {useState} from 'react';
import Login from './pages/Login';
import Employees from './pages/Employees';
import Attendance from './pages/Attendance';
import Reports from './pages/Reports';

export default function App(){
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [view, setView] = useState('employees');
  if(!token){
    return <Login onLogin={(t)=>{setToken(t); localStorage.setItem('token', t);}} />;
  }
  return (
    <div style={{padding:20,fontFamily:'Arial'}}>
      <header><h1>HRM Agriculture</h1></header>
      <nav style={{marginBottom:12}}>
        <button onClick={()=>setView('employees')}>Employees</button>
        <button onClick={()=>setView('attendance')}>Attendance</button>
        <button onClick={()=>setView('reports')}>Reports</button>
        <button style={{float:'right'}} onClick={()=>{localStorage.removeItem('token'); setToken(null);}}>Logout</button>
      </nav>
      <main>
        {view==='employees' && <Employees token={token} />}
        {view==='attendance' && <Attendance token={token} />}
        {view==='reports' && <Reports token={token} />}
      </main>
    </div>
  );
}
