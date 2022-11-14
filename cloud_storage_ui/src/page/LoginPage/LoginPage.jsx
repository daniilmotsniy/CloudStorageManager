import {api} from "../../api"
import "../../router/styles.css"

function LoginPage() {
    const handleSubmit = (event) => {
        event.preventDefault()
        const data = new FormData(event.currentTarget)
        const submitData = {
            username: data.get('username'),
            password: data.get('password'),
        }
        api.login(submitData.username, submitData.password)
        .then(() => (window.location.replace("/")))
    }

    return (
        <div className="Anonymous">
            <h3>Log In</h3>
            <form onSubmit={handleSubmit}>
                <input id="username" name="username" required type="text" placeholder="Username"/>
                <input id="password" name="password" required type="password" placeholder="Password"/>
                <input type="submit" value="Log In" />
            </form>
        </div>
    )
}

export default LoginPage