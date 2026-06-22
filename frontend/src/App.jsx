import React, { useEffect, useState } from 'react'

const API = 'http://localhost:5000'

export default function App(){
  const [pets, setPets] = useState([])
  const [name, setName] = useState('')
  const [selected, setSelected] = useState(null)
  const [memory, setMemory] = useState('')

  useEffect(()=>{ fetchPets() }, [])

  async function fetchPets(){
    const res = await fetch(`${API}/pets`)
    const data = await res.json()
    setPets(data)
  }

  async function createPet(e){
    e.preventDefault()
    if(!name) return
    await fetch(`${API}/pets`, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({name})})
    setName('')
    fetchPets()
  }

  async function addMemory(e){
    e.preventDefault()
    if(!selected || !memory) return
    await fetch(`${API}/pets/${selected}/memories`, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({memory})})
    setMemory('')
    fetchPets()
  }

  return (
    <div className="container">
      <h1>Bichinhos da Memória</h1>
      <div className="row">
        <div className="col">
          <h2>Criar bichinho</h2>
          <form onSubmit={createPet}>
            <input value={name} onChange={e=>setName(e.target.value)} placeholder="Nome" />
            <button type="submit">Criar</button>
          </form>

          <h2>Lista</h2>
          <ul>
            {pets.map(p=> (
              <li key={p.id} onClick={()=>setSelected(p.id)} className={selected===p.id? 'selected':''}>
                {p.name} ({p.memory?.length || 0})
              </li>
            ))}
          </ul>
        </div>
        <div className="col">
          <h2>Detalhes</h2>
          {selected ? (
            <div>
              <h3>Memórias</h3>
              <ul>
                {(pets.find(p=>p.id===selected)?.memory||[]).map((m,i)=> <li key={i}>{m}</li>)}
              </ul>
              <form onSubmit={addMemory}>
                <input value={memory} onChange={e=>setMemory(e.target.value)} placeholder="Nova memória" />
                <button type="submit">Adicionar</button>
              </form>
            </div>
          ) : (
            <div>Selecione um bichinho à esquerda</div>
          )}
        </div>
      </div>
    </div>
  )
}
