import React from 'react'
import HeaderAnonymous from "../HeaderAnonymous"
import Footer from "../Footer"

function AnonymousTemplate(props) {
    return (
        <div>
            <HeaderAnonymous />
            {props.children}
            <Footer />
        </div>
    )
}

export default AnonymousTemplate