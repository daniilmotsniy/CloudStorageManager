import {api} from "../../api"

import {useEffect, useState} from "react"

function AccountPage() {
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [userdata, setUserdata] = useState({})

    useEffect(() => {
        userDetails()
    }, []);

    function userDetails() {
        setLoading(true);
        setError(null);
        api.getUser()
        .then(({data}) => {
            setLoading(false);
            setError(false);
            setUserdata(data);
        })
        .catch(err => {
            setError(`Unknown error occured ` + err);
        })
    }

    return (
        error ? <div>{error}</div> :
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