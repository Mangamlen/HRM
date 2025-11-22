import React, {useEffect, useState} from 'react';
export default function Attendance({token}){
  const [emps,setEmps]=useState([]);
  const [date,setDate]=useState(new Date().toISOString().slice(0,10));
  const [emp,setEmp]=useState(null);
  useEffect(()=>{fetch('/api/employees',{headers:{Authorization:'Bearer '+token}}).then(r=>r.json()).then(d=>{setEmps(d); if(d[0]) setEmp(d[0].id)})},[]);
  const checkin=async ()=>{ await fetch('/api/attendance',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+token},body:JSON.stringify({employee_id:emp,date})}); alert('checked in'); }
  const checkout=async ()=>{ await fetch('/api/attendance/checkout',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+token},body:JSON.stringify({employee_id:emp,date})}); alert('checked out'); }
  return (<div><h2>Attendance</h2>
    <label>Date: <input type='date' value={date} onChange={e=>setDate(e.target.value)} /></label>
    <label>Employee: <select value={emp||''} onChange={e=>setEmp(parseInt(e.target.value))}>{emps.map(x=>(<option key={x.id} value={x.id}>{x.id} - {x.first_name} {x.last_name}</option>))}</select></label>
    <div><button onClick={checkin}>Check-in</button><button onClick={checkout}>Check-out</button></div>
  </div>)
}
