import BusinessObject from "./BusinessObject.js"



export default class User extends BusinessObject{
    /**
   * @param {*} name- Name des Users
   * @param {*} email - HdM Email des Users
   * @param {*} passwort- die User ID
   */

    constructor(name, email, passwort) {
        super();
        this.name = name
        this.email = email
        this.passwort = passwort

    }
    

    setName(name) {
        this.name = name;
    }

    getName() {
        return this.name;
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


    static fromJSON(user) {
        let result = [];

        if (Array.isArray(user)) {
            user.forEach((c) => {
                Object.setPrototypeOf(c, User.prototype);
                result.push(c);
            })
        } else {
            let c = user;
            Object.setPrototypeOf(c, User.prototype);
            result.push(c);
        }

        return result;
    }
}

