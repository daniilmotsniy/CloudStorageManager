import { BrowserRouter, Route, Routes } from "react-router-dom"

import AuthenticatedTemplate from "../components/AuthenticatedTemplate"
import BucketsPage from "../page/BucketsPage"
import AddNewBucketPage from "../page/AddNewBucketPage"
import AccountPage from "../page/AccountPage"

function AuthenticatedRouter() {
    return (
        <BrowserRouter>
            <AuthenticatedTemplate>
                <div className="ParentAuthenticated">
                    <Routes>
                        <Route path="/" element={<BucketsPage />} />
                        <Route path="/buckets" element={<BucketsPage />} />
                        <Route path="/add_new_bucket" element={<AddNewBucketPage />} />
                        <Route path="/account" element={<AccountPage />} />
                    </Routes>
                </div>
             </AuthenticatedTemplate>
        </BrowserRouter>
    )
}

export default AuthenticatedRouter