import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {useState,useEffect} from 'react';

const TableComponent = ({ data }) => {
    const columns = data.columns
    const values = data.results

    if (!data || data.length === 0) {
        return <div>No data available.</div>;
    }
    return (
        <div className="flex flex-col items-center">
            <table className ="table table-bordered border-primary">
                <thead>
                    <tr>
                        {columns.map(key=> (
                            <th key={key}>{key}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {values.map((row,index)=> (
                    <tr key = {index}>
                        {row.map((value,index) => (
                            <td key={index}>{value}</td>
                        ))}
                    </tr>
                    ))}  
                </tbody>
            </table>
        </div>
    );
};

export default TableComponent;