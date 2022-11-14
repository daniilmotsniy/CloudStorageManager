import {api} from "../../api";
import "../../router/styles.css"

function RegisterPage() {
    const handleSubmit = (event) => {
        event.preventDefault()
        const data = new FormData(event.currentTarget)
        const submitData = {
            username: data.get('username'),
            email: data.get('email'),
            password1: data.get('password1'),
            password2: data.get('password2'),
        }
        api.register(submitData.username, submitData.email, submitData.password1, submitData.password2)
    }

    return (
        <div className="Anonymous">
            <h3>Register</h3>

            <form onSubmit={handleSubmit}>
                <input id="username" name="username" required type="text" placeholder="Username"/>
                <input id="email" name="email" required type="email" placeholder="Email"/>
                <input id="password1" name="password1" required type="password" placeholder="Password" />
                <input id="password2" name="password2" required type="password" placeholder="Repeat password" />
                <input type="submit" value="Register" />
            </form>
        </div>
    )
}

export default RegisterPage