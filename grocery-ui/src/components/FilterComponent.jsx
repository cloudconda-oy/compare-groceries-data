import React, { useState,useEffect } from 'react';
import TableComponent from './TableComponent.jsx'

const FilterComponent = () => {
  const [data,setData] = useState([])
  const [query, setQuery] = useState('');
  const [showData, setShowData] =  useState(false);

  const handleClick = () => {
    setShowData(true);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch('http://127.0.0.1:5000/query',{
      method : 'POST',
      headers : {
        'Content-Type' : 'application/json'
      },
      body : JSON.stringify({query})
    })
    .then(response => response.json())
    .then(apiData => {
      setData(apiData);
    })
    .catch(error => {
      console.error(error);
    });
  };
  
  
  return (
    <>
      <div className="flex flex-col items-center justify-center h-screen bg-success">
        <h2 className="text-4xl text-center text-white font-bold mb-4">Compare prices for the grocery products in one tap.</h2>
        <form onSubmit={handleSubmit}>
          <input type = "text" value = {query} placeholder=" Enter query" onChange={e => setQuery(e.target.value)}></input>
          <br/>
          <br/>

          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" type = "submit" onClick={handleClick}>Get Data</button>
        </form>
      </div>
      <div>
        {showData && <TableComponent data={data} />}
      </div>
    </>
  )};

export default FilterComponent;