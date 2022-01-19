import BusinessObject from "./BusinessObject.js"



export default class User extends BusinessObject{
    /**
   * @param {*} ID - ID der Verwaltungsmitarbeiter
   * @param {*} name - Name der Verwaltungsmitarbeiter
   * @param {*} vorname - Vorname der Verwaltungsmitarbeiter
   * @param {*} email - HdM Email der Verwaltungsmitarbeiter
   * @param {*} passwort- Die Passwort
   */

    constructor(ID, name, vorname, email, passwort) {
        super();
        this.ID = ID
        this.name = name
        this.vorname = vorname
        this.email = email
        this.passwort = passwort

    }

    setID(ID) {
        this.ID = ID;
    }
    getID() {
        this.ID = ID;
    }
    

    setName(name) {
        this.name = name;
    }

    getName() {
        return this.name;
    }

    setVorname(vorname) {
        this.vorname = vorname;
    }

    getVorname() {
        return this.vorname;
    }

    setEmail (email) {
        this.email = email;
    }

    getEmail() {
        return this.email;
    }

    setPasswort (passwort) {
        this.passwort = this.passwort;
    }

    getPasswort() {
        return this.passwort;
    }


    static fromJSON(verwaltungsmitarbeiter) {
        let result = [];

        if (Array.isArray(verwaltungsmitarbeiter)) {
            verwaltungsmitarbeiter.forEach((c) => {
                Object.setPrototypeOf(c, Verwaltungsmitarbeiter.prototype);
                result.push(c);
            })
        } else {
            let c = verwaltungsmitarbeiter;
            Object.setPrototypeOf(c, Verwaltungsmitarbeiter.prototype);
            result.push(c);
        }

        return result;
    }

}
