import React, {useEffect, useState} from 'react';
export default function Employees({token}){
  const [emps,setEmps]=useState([]);
  const [form,setForm]=useState({first_name:'',last_name:'',phone:'',role:'field_worker',wage_type:'daily',wage_amount:0,farm_location:''});
  const load=async ()=>{
    const r=await fetch('/api/employees',{headers:{Authorization:'Bearer '+token}});
    setEmps(await r.json());
  }
  useEffect(()=>{load();},[]);
  const add=async e=>{e.preventDefault(); await fetch('/api/employees',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+token},body:JSON.stringify(form)}); setForm({first_name:'',last_name:'',phone:'',role:'field_worker',wage_type:'daily',wage_amount:0,farm_location:''}); load();}
  const del=async id=>{ if(!confirm('Delete?')) return; await fetch('/api/employees/'+id,{method:'DELETE',headers:{Authorization:'Bearer '+token}}); load(); }
  return (<div>
    <h2>Employees</h2>
    <form onSubmit={add} style={{marginBottom:12}}>
      <input placeholder='First name' value={form.first_name} onChange={e=>setForm({...form,first_name:e.target.value})} required />
      <input placeholder='Last name' value={form.last_name} onChange={e=>setForm({...form,last_name:e.target.value})} />
      <input placeholder='Phone' value={form.phone} onChange={e=>setForm({...form,phone:e.target.value})} />
      <select value={form.role} onChange={e=>setForm({...form,role:e.target.value})}><option>field_worker</option><option>supervisor</option><option>admin</option></select>
      <select value={form.wage_type} onChange={e=>setForm({...form,wage_type:e.target.value})}><option value='daily'>daily</option><option value='monthly'>monthly</option></select>
      <input type='number' step='0.01' value={form.wage_amount} onChange={e=>setForm({...form,wage_amount:parseFloat(e.target.value)})} />
      <input placeholder='Farm location' value={form.farm_location} onChange={e=>setForm({...form,farm_location:e.target.value})} />
      <button type='submit'>Add</button>
    </form>
    <table border='1' cellPadding='6'><thead><tr><th>ID</th><th>Name</th><th>Role</th><th>Wage</th><th>Location</th><th>Action</th></tr></thead>
    <tbody>{emps.map(e=>(<tr key={e.id}><td>{e.id}</td><td>{e.first_name} {e.last_name}</td><td>{e.role}</td><td>{e.wage_type} - {e.wage_amount}</td><td>{e.farm_location}</td><td><button onClick={()=>del(e.id)}>Delete</button></td></tr>))}</tbody></table>
  </div>)
}
