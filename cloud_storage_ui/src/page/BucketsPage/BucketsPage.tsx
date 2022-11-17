import BucketInfo from "../../components/BucketInfo";
import {api} from "../../api";

import {useEffect, useState} from "react";

import "./styles.css"
import {NavLink} from "react-router-dom";

function BucketsPage() {
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    type BucketType = {
        id: string
        name: string
        provider: string
    }

    const [buckets, setBuckets] = useState(Array<BucketType>)

    useEffect(() => {
        loadBuckets()
    }, []);

    function loadBuckets() {
        setLoading(true);
        setError('');
        api.getBucketsList()
        .then(({data}) => {
            setLoading(false);
            setError('');
            setBuckets(data);
        })
        .catch(err => {
            return setError("Unknown error occurred " + err);
        })
    }

    return (
        error ? <div>{error}</div> :
        <div>
            {
                loading ? <div>Loading ...</div> :
                    <>
                        <div className="Buckets">
                            <div className="AddBucket">
                                <NavLink to="/add_new_bucket">
                                    <input type="submit" value="Add new bucket"/>
                                </NavLink>
                            </div>
                            {
                                buckets.map(el => (
                                    <BucketInfo id={el.id} bucketName={el.name} bucketDesc={el.provider}/>
                                ))
                            }
                        </div>
                    </>
            }
        </div>
    )
}

export default BucketsPage