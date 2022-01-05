import React,{useState} from 'react';
import './App.css';
import MaterialTable from 'material-table'



function SPO(){
    const [tableData, setTableData] = useState ([
     {Semester:"1", EDV_Nummer:"335000", Modul:"Einstufungstest Englisch", SWS:"0", ECTS:"0", Prüfungsform:"LÜ"},
     {Semester:"1", EDV_Nummer:"335120", Modul:"Marketing & Organisation", SWS:"4", ECTS:"5", Prüfungsform:"KL"},
     {Semester:"1", EDV_Nummer:"335121", Modul:"Grundlagen Wirtschaftsinformatik", SWS:"4", ECTS:"5", Prüfungsform:"KMP"},
     {Semester:"1", EDV_Nummer:"335122", Modul:"Datenbanken Grundlagen", SWS:"4", ECTS:"5", Prüfungsform:"KMP"},
     {Semester:"1", EDV_Nummer:"335123", Modul:"Programmieren", SWS:"4", ECTS:"5", Prüfungsform:"KMP"},
     {Semester:"1", EDV_Nummer:"335126", Modul:"Propädeutik WI", SWS:"4", ECTS:"5", Prüfungsform:"KMP"},
     {Semester:"1", EDV_Nummer:"338048", Modul:"Data Literacy_1", SWS:"2", ECTS:"5", Prüfungsform:"KSP"},
     {Semester:"2", EDV_Nummer:" 338047", Modul:"Data Literacy_2", SWS:"2", ECTS:"5", Prüfungsform:"KMP"},
     {Semester:"2", EDV_Nummer:"335125", Modul:"Externes und Internes_Rechnungswesen", SWS:"4", ECTS:"5", Prüfungsform:"KL"},
     {Semester:"2", EDV_Nummer:"335127", Modul:"Algorithmen & Datenstrukturen", SWS:"4", ECTS:"5", Prüfungsform:"KMP"},
     {Semester:"2", EDV_Nummer:"335128", Modul:"Geschäftsprozesse", SWS:"4", ECTS:"5", Prüfungsform:"KL"},
     {Semester:"2", EDV_Nummer:"", Modul:"", SWS:"", ECTS:"", Prüfungsform:""},
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

          <MaterialTable columns = {columns} data={tableData} title="WI SPO"/>
       
        </div>
      );
}

export default SPO;
