export default function Stats({props}) {
    if(!props) { return null; }
    return (
        <>
        <div className="flex flex-col">
            <h1>Number of reviews: {props.num_reviews}</h1>
            <h1>Correctly predicted labels: {props.correct}</h1>
            <h1>Accuracy: {props.accuracy.toPrecision(5)}</h1>
        </div>
        </>
    );
}