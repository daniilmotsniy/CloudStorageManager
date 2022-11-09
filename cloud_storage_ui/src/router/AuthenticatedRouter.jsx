import { BrowserRouter, Route, Routes } from "react-router-dom"

import AuthenticatedTemplate from "../components/AuthenticatedTemplate"
import BucketsPage from "../page/BucketsPage"
import AccountPage from "../page/AccountPage"

function AuthenticatedRouter() {
    return (
        <BrowserRouter>
            <AuthenticatedTemplate>
                <Routes>
                    <Route path="/" element={<BucketsPage />} />
                    <Route path="/buckets" element={<BucketsPage />} />
                    <Route path="/account" element={<AccountPage />} />
                </Routes>
             </AuthenticatedTemplate>
        </BrowserRouter>
    )
}

export default AuthenticatedRouter