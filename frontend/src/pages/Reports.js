import React, {useState} from 'react';
import './Reports.css';

export default function Reports({token}){
  const [start,setStart]=useState('2025-11-01');
  const [end,setEnd]=useState(new Date().toISOString().slice(0,10));
  const [att,setAtt]=useState(null);
  const [pay,setPay]=useState(null);
  const loadAtt=async ()=>{ const r=await fetch(`/api/report/attendance_summary?start=${start}&end=${end}`,{headers:{Authorization:'Bearer '+token}}); setAtt(await r.json()); }
  const loadPay=async ()=>{ const r=await fetch(`/api/report/payroll?start=${start}&end=${end}`,{headers:{Authorization:'Bearer '+token}}); setPay(await r.json()); }
  return (
    <div className="reports-container">
      <h2>Reports</h2>
      <div className="date-filters">
        <div className="date-filter">
          <label htmlFor="start-date">Start</label>
          <input id="start-date" type='date' value={start} onChange={e=>setStart(e.target.value)} />
        </div>
        <div className="date-filter">
          <label htmlFor="end-date">End</label>
          <input id="end-date" type='date' value={end} onChange={e=>setEnd(e.target.value)} />
        </div>
      </div>
      <div className="report-buttons">
        <button onClick={loadAtt}>Load Attendance Summary</button>
        <button onClick={loadPay}>Load Payroll</button>
      </div>
      <div className="report-output">
        {att && <div><h3>Attendance</h3><pre>{JSON.stringify(att,null,2)}</pre></div>}
        {pay && <div><h3>Payroll</h3><pre>{JSON.stringify(pay,null,2)}</pre></div>}
      </div>
    </div>
  )
}
