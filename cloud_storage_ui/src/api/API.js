/**
 * API - the class to work with API methods
 */

import axios from 'axios';
import { Service } from 'axios-middleware';



class API {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
        this.service = new Service(axios);
        this.axiosInstance = axios.create({
            baseURL: baseUrl,
            headers: {"Content-Type": "application/json"}
        });
    };

    //
    // static get authHeaders() {
    //     const token = window.localStorage.getItem("token");
    //     const tokenExpiration = window.localStorage.getItem("tokenExp");
    //     const tokenExpirateionDate = new Date(parseInt(tokenExpiration) * 1000);
    //     console.warn("Getting auth headers");
    //     if (token && tokenExpiration && tokenExpirateionDate > new Date()) {
    //         return {"X-Auth-Token": `${token}`};
    //     }
    //     // If the access token is invalid
    //     API.setToken(null);
    //     return {};
    // };
    //
    //
    // static setRefresh(data) {
    //     if (!data) {
    //         window.localStorage.removeItem("refresh");
    //         window.localStorage.removeItem("refreshExp");
    //         return;
    //     }
    //     const {refresh, exp} = data;
    //     console.warn("API :: setRefresh :: refresh, exp == ", refresh, exp);
    //     window.localStorage.setItem("refresh", refresh);
    //     window.localStorage.setItem("refreshExp", exp);
    // };
    //
    // // Set X-Auth-Token
    // static setToken(data) {
    //     if (!data){
    //         window.localStorage.removeItem("token");
    //         window.localStorage.removeItem("tokenExp");
    //         return;
    //     }
    //     const {token, exp} = data;
    //     window.localStorage.setItem("token", token);
    //     window.localStorage.setItem("tokenExp", exp);
    // };
    //
    // setUp() {
    //     const self = this;
    //     const serviceConfig = {
    //         onRequest(config) {
    //             // console.log('onRequest');
    //
    //             if (API.isAuthenticated){
    //                 config.headers = {
    //                     "Content-Type": "application/json",
    //                     ...API.authHeaders
    //                 }
    //                 return config;
    //             }
    //             return self.refreshToken()
    //                 .then(() => {
    //                     config.headers = {
    //                         "Content-Type": "application/json",
    //                         ...API.authHeaders
    //                     };
    //                     return config;
    //                 });
    //         },
    //         onSync(promise) {
    //             // console.log('onSync');
    //             return promise;
    //         },
    //         onResponse(response) {
    //             // console.log('onResponse');
    //             return response;
    //         }
    //     };
    //     this.service.register(serviceConfig);
    // }
    //
    // static isTokenPresent(tokenName) {
    //     const anyToken = window.localStorage.getItem(tokenName);
    //     return typeof(anyToken) === "string";
    // }
    //
    //
    // static isTokenRelevant(tokenName) {
    //     try {
    //         const anyToken = window.localStorage.getItem(tokenName);
    //         const anyTokenExpiration = window.localStorage.getItem(`${tokenName}Exp`);
    //         const anyTokenExpirateionDate = new Date(parseInt(anyTokenExpiration) * 1000);
    //         return (typeof(anyToken) === "string" && anyTokenExpirateionDate > new Date());
    //     }
    //     catch(error){
    //         return false;
    //     }
    // };
    //
    // static isTokenPresentAndRelevant(tokenName) {
    //     const relevant = API.isTokenRelevant(tokenName);
    //     const present = API.isTokenPresent(tokenName);
    //     return (present && relevant);
    // };
    //
    // jsHeaders() {
    //     return {
    //         headers: {
    //             'Content-Type': 'application/json'
    //         }
    //     }
    // }
    //
    // /**
    //  * Check if the user is authenticated
    //  * @returns {Boolean} User is authenticated: Access token is valid
    //  */
    // static get isAuthenticated() {
    //     const token = window.localStorage.getItem("token");
    //     const tokenExpiration = window.localStorage.getItem("tokenExp");
    //     const tokenExpirateionDate = new Date(parseInt(tokenExpiration) * 1000);
    //     if (!(token && tokenExpiration && tokenExpirateionDate > new Date())){
    //         API.setToken(null);
    //         return false;
    //     }
    //     return true;
    // };
    //
    //
    // /**
    //  *
    //  * @param {String} email the User's email
    //  * @param {String} password the User's pass
    //  * @returns {Promise}
    //  */
    // login(email, password) {
    //     const body = {
    //         email: email,
    //         password: password
    //     };
    //     return fetch( this.baseUrl + `/api/auth/login/`, {
    //         method: "POST",
    //         ...this.jsHeaders(),
    //         body: JSON.stringify(body)
    //     })
    //         .then(response => {
    //             if (response.ok) {
    //                 return response.json();
    //             }
    //             throw new Error("Invalid credentials");
    //         })
    //         .then(data => {API.setRefresh(data);})
    //         .then(this.refreshToken())
    // }
    //
    // logout() {
    //     ["refresh","refreshExp","token","tokenExp"].forEach(el => {
    //         window.localStorage.removeItem(el);
    //     });
    //     window.location.replace("/");
    // };
    //
    // /**
    //  * Obtain a new access token
    //  * @returns void
    //  */
    // refreshToken() {
    //     const refresh = window.localStorage.getItem("refresh");
    //     return fetch( this.baseUrl + `/api/auth/refresh/${refresh}`, {
    //         method: "POST",
    //         ...this.jsHeaders(),
    //     })
    //         .then(response => {
    //             if (response.ok) {
    //                 return response.json();
    //             }
    //             throw new Error("Invalid refresh token");
    //         })
    //         .then(data => {
    //             const {token, exp} = data;
    //             API.setToken(data);
    //         });
    // };

    getBucketsList(status = 2) {
        return this.axiosInstance.get(`/api/coordinator?status=${status}`);
    }

    getUser(id = "self") {
        return this.axiosInstance.get(`/api/user/${id}`);
    };
}

export default API;