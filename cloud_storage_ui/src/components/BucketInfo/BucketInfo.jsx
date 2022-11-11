function BucketInfo(props) {
    return (
        <div>
            <h3>{props.bucketName}</h3>
            <p>
                Provider: {props.bucketDesc}
            </p>
            <button> Read </button>
            <button> Delete </button>
        </div>
    )
}

export default BucketInfo