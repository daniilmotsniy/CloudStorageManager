function BucketInfo(props) {
    return (
        <div>
            <h3>{props.bucketName}</h3>
            <p>
                {props.bucketDesc}
            </p>
        </div>
    )
}

export default BucketInfo