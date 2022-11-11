/**
 * API - the class to work with API methods
 */

import axios from 'axios'
import { Service } from 'axios-middleware'

class API {
    constructor(baseUrl) {
        this.baseUrl = baseUrl
        this.service = new Service(axios)
        this.axiosInstance = axios.create({
            baseURL: baseUrl,
            headers: {"Content-Type": "application/json"}
        })
    }

    jsHeaders() {
        return {
            headers: {
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
        }
    }

    login(username, password) {
        const body = {
            username: username,
            password: password
        };
        return fetch( this.baseUrl + `/api/users/token`, {
            method: "POST",
            ...this.jsHeaders(),
            body: JSON.stringify(body)
        })
        .then(response => {
            if (response.ok) {
                return response.json()
            }
            throw new Error("Invalid credentials")
        })
        .then(data => {API.setToken(data)})
    }

    register(username, email, password1, password2){
        const body = {
            username: username,
            email: email,
            password1: password1,
            password2: password2
        };
        return fetch( this.baseUrl + `/api/users/register`, {
            method: "POST",
            ...this.jsHeaders(),
            body: JSON.stringify(body)
        })
        .then(response => {
            if (response.ok) {
                return response.json()
            }
            throw new Error("Invalid credentials")
        })
        .then(() => {window.location.replace("/")})
    }

    static get authHeaders() {
        const token = window.localStorage.getItem("token")
        const tokenExpiration = window.localStorage.getItem("tokenExp")
        const tokenExpirationDate = new Date(parseInt(tokenExpiration)  * 1000)
        if (token && tokenExpiration && tokenExpirationDate > new Date()) {
            return {"token": `${token}`}
        }
        return {}
    };

    static setToken(data) {
        if (!data){
            window.localStorage.removeItem("token")
            window.localStorage.removeItem("tokenExp")
            return
        }
        const {token, tokenExp} = data

        window.localStorage.setItem("token", token)
        window.localStorage.setItem("tokenExp", tokenExp)
    };

    setUp() {
        const serviceConfig = {
            onRequest(config) {
                if (API.isAuthenticated){
                    config.headers = {
                        "Content-Type": "application/json",
                        ...API.authHeaders
                    }
                    return config;
                }
            },
            onSync(promise) {
                return promise;
            },
            onResponse(response) {
                return response;
            }
        };
        this.service.register(serviceConfig)
    }

    static get isAuthenticated() {
        const token = window.localStorage.getItem("token")
        const tokenExpiration = window.localStorage.getItem("tokenExp")
        const tokenExpirationDate = new Date(parseInt(tokenExpiration) * 1000)
        if (!(token && tokenExpiration && tokenExpirationDate > new Date())){
            API.setToken(null)
            return false
        }
        return true
    }

    logout() {
        ["token","tokenExp"].forEach(el => {
            window.localStorage.removeItem(el)
        })
        window.location.replace("/")
    }

    getBucketsList() {
        return this.axiosInstance.get('/api/storage/buckets')
    }

    getUser() {
        return this.axiosInstance.get(`/api/users/me`)
    }
}

export default API