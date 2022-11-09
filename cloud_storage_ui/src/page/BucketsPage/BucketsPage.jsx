import BucketInfo from "../../components/BucketInfo";

function BucketsPage() {
    return (
        <div>
            <BucketInfo bucketName={'Test AWS Bucket 1'} bucketDesc={'Lorem ipsum ...'}/>
            <BucketInfo bucketName={'Test AWS Bucket 2'} bucketDesc={'Lorem ipsum ...'}/>
            <BucketInfo bucketName={'Test GCP Bucket 1'} bucketDesc={'Lorem ipsum ...'}/>
        </div>
    )
}

export default BucketsPage