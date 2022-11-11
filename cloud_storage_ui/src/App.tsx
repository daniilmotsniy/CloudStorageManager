import React from 'react'
import './App.css'
import {AnonymousRouter, AuthenticatedRouter} from "./router"
import {API} from "./api"

function App() {
    const authenticated: boolean = API.isAuthenticated
    const Router = authenticated ? AuthenticatedRouter : AnonymousRouter

     return (
         <div className="App">
              <div>
                  <Router />
              </div>
         </div>
     )
}

export default App
