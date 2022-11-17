import {api} from "../../api"

import {useEffect, useState} from "react"

function AccountPage() {
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")

    type UserData = {
        username: string
        email: string
        api_token: string
    }

    const [userdata, setUserdata] = useState<UserData | undefined>(undefined)

    useEffect(() => {
        userDetails()
    }, []);

    function userDetails() {
        setLoading(true);
        setError("");
        api.getUser()
        .then(({data}) => {
            setLoading(false);
            setError("");
            setUserdata(data);
        })
        .catch(err => {
            setError("Unknown error occured " + err);
        })
    }

    return (
        error || !userdata ? <div>{error}</div> :
            <div>
                {
                    loading ? <div>Loading ...</div> :
                        <>
                            <p>
                                Username: {userdata.username}
                            </p>
                            <p>
                                Email: {userdata.email}
                            </p>
                            <p>
                                API Token: {userdata.api_token}
                            </p>
                        </>
                }
            </div>
    )
}

export default AccountPage