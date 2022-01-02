import React,{useState} from 'react';
import './App.css';
import MaterialTable from 'material-table'



function SPO(){
    const [tableData, setTableData] = useState ([
     {Semester:"1", EDV_Nummer:"335000", Modul:"Einstufungstest Englisch", SWS:"0", ECTS:"0", Prüfungsform:"LÜ"},
     {Semester:"", EDV_Nummer:"", Modul:"", SWS:"", ECTS:"", Prüfungsform:""},
     {Semester:"", EDV_Nummer:"", Modul:"", SWS:"", ECTS:"", Prüfungsform:""},
     {Semester:"", EDV_Nummer:"", Modul:"", SWS:"", ECTS:"", Prüfungsform:""},
     {Semester:"", EDV_Nummer:"", Modul:"", SWS:"", ECTS:"", Prüfungsform:""},
     {Semester:"", EDV_Nummer:"", Modul:"", SWS:"", ECTS:"", Prüfungsform:""},
     {Semester:"", EDV_Nummer:"", Modul:"", SWS:"", ECTS:"", Prüfungsform:""},
     {Semester:"", EDV_Nummer:"", Modul:"", SWS:"", ECTS:"", Prüfungsform:""},
     {Semester:"", EDV_Nummer:"", Modul:"", SWS:"", ECTS:"", Prüfungsform:""},
     {Semester:"", EDV_Nummer:"", Modul:"", SWS:"", ECTS:"", Prüfungsform:""},
     {Semester:"", EDV_Nummer:"", Modul:"", SWS:"", ECTS:"", Prüfungsform:""},
     {Semester:"", EDV_Nummer:"", Modul:"", SWS:"", ECTS:"", Prüfungsform:""},
     {Semester:"", EDV_Nummer:"", Modul:"", SWS:"", ECTS:"", Prüfungsform:""},
     {Semester:"", EDV_Nummer:"", Modul:"", SWS:"", ECTS:"", Prüfungsform:""},
     {Semester:"", EDV_Nummer:"", Modul:"", SWS:"", ECTS:"", Prüfungsform:""},
    ])
    const columns=[
        {title:"Semester", field:"Semester"},
        {title:"EDV_Nummer", field:"EDV_Nummer"},
        {title:"Modul", field:"Modul"},
        {title:"SWS", field:"SWS"},
        {title:"ECTS", field:"ECTS"},
        {title:"Prüfungsform", field:"Prüfungsform"},
    ]
    return(
        <div className="SPO">
          <h1 align="center">SPOtch</h1>
          <h4 align="center"></h4>

          <MaterialTable columns = {columns} data={tableData}/>
       
        </div>
      );
}

export default SPO;
