import { BrowserRouter, Route, Routes } from "react-router-dom"

import AnonymousTemplate from "../components/AnonymousTemplate"
import LoginPage from "../page/LoginPage"
import RegisterPage from "../page/RegisterPage"

import "./styles.css"

function AuthenticatedRouter() {
    return (
        <BrowserRouter>
            <AnonymousTemplate>
                <div className="ParentAnonymous">
                    <Routes>
                        <Route path="/" element={<LoginPage />} />
                        <Route path="/register" element={<RegisterPage />} />
                        <Route path="/login" element={<LoginPage />} />
                    </Routes>
                </div>
             </AnonymousTemplate>
        </BrowserRouter>
    )
}

export default AuthenticatedRouter