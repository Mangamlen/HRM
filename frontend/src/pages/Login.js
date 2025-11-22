import React, {useState} from 'react';
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
  return (<form onSubmit={submit} style={{maxWidth:420}}>
    <h2>Login</h2>
    {err && <div style={{color:'red'}}>{err}</div>}
    <label>Username<br/><input value={u} onChange={e=>setU(e.target.value)} /></label><br/>
    <label>Password<br/><input type="password" value={p} onChange={e=>setP(e.target.value)} /></label><br/>
    <button type="submit">Login</button>
  </form>)
}
