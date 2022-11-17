import React from 'react'
import Header from "../Header"
import Footer from "../Footer"

function AuthenticatedTemplate(props: any) {
    return (
        <div>
            <Header />
            {props.children}
            <Footer />
        </div>
    )
}

export default AuthenticatedTemplate