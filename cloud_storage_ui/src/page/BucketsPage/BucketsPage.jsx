import BucketInfo from "../../components/BucketInfo";
import {api} from "../../api";

import {useEffect, useState} from "react";

import "./styles.css"
import {NavLink} from "react-router-dom";

function BucketsPage() {
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [buckets, setBuckets] = useState([])

    useEffect(() => {
        loadBuckets()
    }, []);

    function loadBuckets() {
        setLoading(true);
        setError(null);
        api.getBucketsList()
        .then(({data}) => {
            setLoading(false);
            setError(false);
            setBuckets(data);
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
                        <div className="Buckets">
                            <div className="AddBucket">
                                <NavLink to="/add_new_bucket">
                                    <input type="submit" value="Add new bucket"/>
                                </NavLink>
                            </div>
                            {
                                buckets.map(el => (
                                    <BucketInfo bucketName={el.name} bucketDesc={el.provider}/>
                                ))
                            }
                        </div>
                    </>
            }
        </div>

    )
}

export default BucketsPage