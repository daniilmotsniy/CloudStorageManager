import "./styles.css"

function BucketInfo(props) {
    return (
        <div className="BucketsInfo">
            <h3>{props.bucketName}</h3>
            <p>
                Provider: {props.bucketDesc}
            </p>
            <button id="files"> Files </button>
            <button id="delete"> Delete </button>
        </div>
    )
}

export default BucketInfo