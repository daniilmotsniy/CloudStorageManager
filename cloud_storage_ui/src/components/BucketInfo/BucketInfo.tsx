import "./styles.css"
import {NavLink} from "react-router-dom";
import { ReactElement, JSXElementConstructor, ReactFragment, ReactPortal } from "react";

function BucketInfo(props: { id: string; bucketName: string | number | boolean | ReactElement<any, string | JSXElementConstructor<any>> | ReactFragment | ReactPortal | null | undefined; bucketDesc: string | number | boolean | ReactElement<any, string | JSXElementConstructor<any>> | ReactFragment | ReactPortal | null | undefined; }) {
    return (
        <div className="BucketsInfo">
            <NavLink to={"/bucket/" + props.id}>
                <h3>{props.bucketName}</h3>
                <p>
                    Provider: {props.bucketDesc}
                </p>
            </NavLink>
        </div>
    )
}

export default BucketInfo