import {api} from "../../api";

import "./styles.css"

function AddNewBucketPage() {
    const handleSubmit = (event: { preventDefault: () => void; currentTarget: HTMLFormElement | undefined; }) => {
        event.preventDefault()
        const data = new FormData(event.currentTarget)
        const submitData = {
            name: data.get('name'),
            provider: data.get('provider'),
        }
        api.addNewBucket(submitData.name, submitData.provider)
            .then(() => (window.location.replace("/buckets")))
    }

    return (
        <div className="AddBucket">
            <form onSubmit={handleSubmit}>
                <h4>Bucket name</h4>
                <input id="name" name="name" required type="text" placeholder="Enter name here"/>
                <div className="wrapper">
                    <h4>Bucket cloud provider</h4>
                    <label className="container">
                        AWS
                        <input type="radio" checked={true} name="provider" value="aws"/>
                        <span className="checkmark"></span>
                    </label>
                    <label className="container">
                        GCP
                        <input type="radio" name="provider" value="gcp"/>
                        <span className="checkmark"></span>
                    </label>
                </div>
                <input type="submit" value="Add new bucket" />
            </form>
        </div>
    )
}

export default AddNewBucketPage