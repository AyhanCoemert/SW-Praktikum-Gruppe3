import BusinessObject from "./BusinessObject.js"



export default class Modul extends BusinessObject{
    /**
   * @param {*} sws - SWS des Moduls
   * @param {*} ects- ECTS des Moduls
   * @param {*} literatur - Literatur für Modul
   * @param {*} verantwortlicher - Verantwortlicher des Moduls
   * @param {*} edv_nummer - Nummer des Moduls
   */

    constructor(sws, ects, literatur, verantwortlicher, edv_nummer) {
        super();
        this.sws = sws
        this.ects = ects
        this.literatur = literatur
        this.verantwortlicher = verantwortlicher
        this.edv_nummer = edv_nummer

    }

    setSws(sws) {
        this.sws = sws;
    }
    getSws() {
        return this.sws;
    }

    setEcts(ects) {
        this.ects = ects;
    }
    getEcts() {
        return this.ects;
    }

    setLiteratur(literatur) {
        this.literatur = literatur;
    }
    getLiteratur() {
        return this.literatur;
    }

    setVerantwortlicher(verantwortlicher) {
        this.verantwortlicher = verantwortlicher;
    }
    getVerantwortlicher() {
        return this.verantwortlicher;
    }

    setEdvNummer(edv_nummer) {
        this.edv_nummer = edv_nummer;
    }
    getEdvNummer() {
        return this.edv_nummer;
    }

    static fromJSON(module) {
        let result = [];

        if (Array.isArray(module)) {
            user.forEach((c) => {
                Object.setPrototypeOf(c, Module.prototype);
                result.push(c);
            })
        } else {
            let c = module;
            Object.setPrototypeOf(c, Moduel.prototype);
            result.push(c);
        }

        return result;
    }
}