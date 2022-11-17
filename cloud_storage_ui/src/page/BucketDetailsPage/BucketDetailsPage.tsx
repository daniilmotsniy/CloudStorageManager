import "./styles.css"
import {useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import {api} from "../../api";

function BucketDetailsPage() {
    const params = useParams();
    const bucketId = params.id;

    type BucketType = {
        id: string
        name: string
        provider: string
        files: Array<string>
        folders: Array<string>
    }

    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")
    const [bucket, setBucket] = useState<BucketType| undefined>(undefined)

    useEffect(() => {
        loadBucket()
    }, []);

    function loadBucket() {
        setLoading(true);
        setError("");
        api.getBucketDetails(bucketId)
            .then(({data}) => {
                setLoading(false);
                setError("");
                setBucket(data);
            })
            .catch(err => {
                setError("Unknown error occurred " + err);
            })
    }

    return (
        error || !bucket ? <div>{error}</div> :
            <div>
                {
                    loading  ? <div>Loading ...</div> :
                        <>
                            <div className="BucketDetails">
                                <h3>Bucket name: {bucket.name}</h3>
                                <h3>Provider: {bucket.provider}</h3>
                                <p>
                                    Files: {bucket.files}
                                </p>
                                <p>
                                    Folders: {bucket.folders}
                                </p>
                            </div>
                        </>
                }
            </div>
    )
}

export default BucketDetailsPage