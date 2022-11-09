import React from 'react'
import './App.css'
import {AuthenticatedRouter} from "./router"

function App() {
    const Router = AuthenticatedRouter

     return (
         <div className="App">
              <div>
                  <Router />
              </div>
         </div>
     )
}

export default App
