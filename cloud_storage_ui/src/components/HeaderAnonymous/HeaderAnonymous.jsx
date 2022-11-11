import {NavLink} from "react-router-dom";

function HeaderAnonymous() {
    return (
        <div className="Header" >
            <NavLink to="/register">Register</NavLink>
            <NavLink to="/login">Log In</NavLink>
        </div>
    )
}

export default HeaderAnonymous