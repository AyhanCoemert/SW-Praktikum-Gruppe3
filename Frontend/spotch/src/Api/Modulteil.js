/* /import React, { Component, useState, useEffect } from 'react';
import PropTypes from 'prop-types';


function App() {
    const [modul, setModul] = useState([])

    useEffect(() => {
        
    }

    )
}


 */
import BusinessObject from "./BusinessObject.js"



export default class Modulteil extends BusinessObject{
    /**
   * @param {*} ID - ID des Modulteils
   */

    constructor(ID) {
        super();
        this.ID = ID

    }
    

    setID(ID) {
       this.ID = ID; 
    }

    getID() {
       return this.ID; 
    }

    static fromJSON(modulteil) {
        let result = [];

        if (Array.isArray(modulteil)) {
            user.forEach((c) => {
                Object.setPrototypeOf(c, Modulteil.prototype);
                result.push(c);
            })
        } else {
            let c = modulteil;
            Object.setPrototypeOf(c, Modulteil.prototype);
            result.push(c);
        }

        return result;
    }
}


