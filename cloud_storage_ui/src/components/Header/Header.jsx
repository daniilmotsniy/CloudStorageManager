import {NavLink} from "react-router-dom";

function Header() {
    return (
        <div className="Header" >
            <NavLink to="/buckets">Buckets</NavLink>
            <NavLink to="/account">Account</NavLink>
            <a href="/logout">Log out</a>
        </div>
    )
}

export default Header