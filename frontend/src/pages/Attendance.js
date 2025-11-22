import React, {useEffect, useState} from 'react';
import './Attendance.css';

export default function Attendance({token}){
  const [emps,setEmps]=useState([]);
  const [date,setDate]=useState(new Date().toISOString().slice(0,10));
  const [emp,setEmp]=useState(null);
  useEffect(()=>{fetch('/api/employees',{headers:{Authorization:'Bearer '+token}}).then(r=>r.json()).then(d=>{setEmps(d); if(d[0]) setEmp(d[0].id)})},[]);
  const checkin=async ()=>{ await fetch('/api/attendance',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+token},body:JSON.stringify({employee_id:emp,date})}); alert('checked in'); }
  const checkout=async ()=>{ await fetch('/api/attendance/checkout',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+token},body:JSON.stringify({employee_id:emp,date})}); alert('checked out'); }
  return (
    <div className="attendance-container">
      <h2>Attendance</h2>
      <div className="attendance-form">
        <div className="form-group">
          <label htmlFor="date">Date:</label>
          <input id="date" type='date' value={date} onChange={e=>setDate(e.target.value)} />
        </div>
        <div className="form-group">
          <label htmlFor="employee">Employee:</label>
          <select id="employee" value={emp||''} onChange={e=>setEmp(parseInt(e.target.value))}>
            {emps.map(x=>(<option key={x.id} value={x.id}>{x.id} - {x.first_name} {x.last_name}</option>))}
          </select>
        </div>
        <div className="action-buttons">
          <button className="check-in-button" onClick={checkin}>Check-in</button>
          <button className="check-out-button" onClick={checkout}>Check-out</button>
        </div>
      </div>
    </div>
  )
}
