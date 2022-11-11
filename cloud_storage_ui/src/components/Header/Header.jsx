import {NavLink} from "react-router-dom";
import {api} from "../../api";

function Header() {
    const handleLogOut = () => {
        api.logout();
    }
    return (
        <div className="Header" >
            <NavLink to="/buckets">Buckets</NavLink>
            <NavLink to="/account">Account</NavLink>
            <a onClick={handleLogOut}>Log out</a>
        </div>
    )
}

export default Header