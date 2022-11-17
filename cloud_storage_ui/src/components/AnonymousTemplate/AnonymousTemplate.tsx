import React from 'react'
import HeaderAnonymous from "../HeaderAnonymous"
import Footer from "../Footer"

function AnonymousTemplate(props: { children: string | number | boolean |
        React.ReactElement<any, string | React.JSXElementConstructor<any>>
        | React.ReactFragment | React.ReactPortal | null | undefined }) {
    return (
        <div>
            <HeaderAnonymous />
            {props.children}
            <Footer />
        </div>
    )
}

export default AnonymousTemplate