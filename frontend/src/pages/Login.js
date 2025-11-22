import React, {useState} from 'react';
import './Login.css';

export default function Login({onLogin}){
  const [u,setU]=useState('admin');
  const [p,setP]=useState('admin123');
  const [err,setErr]=useState(null);
  const submit=async e=>{
    e.preventDefault();
    const res = await fetch('/api/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})});
    const data = await res.json();
    if(res.ok){ onLogin(data.access_token); } else { setErr(data.msg || 'login failed'); }
  }
  return (<div className="login-container">
    <form onSubmit={submit} className="login-form">
      <h2>Login</h2>
      {err && <div className="error-message">{err}</div>}
      <div className="input-group">
        <label htmlFor="username">Username</label>
        <input id="username" value={u} onChange={e=>setU(e.target.value)} />
      </div>
      <div className="input-group">
        <label htmlFor="password">Password</label>
        <input id="password" type="password" value={p} onChange={e=>setP(e.target.value)} />
      </div>
      <button type="submit" className="login-button">Login</button>
    </form>
  </div>)
}
