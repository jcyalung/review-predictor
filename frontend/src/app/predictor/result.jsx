export default function Result({props}) {
    if (props.error) {
        return (
            <p className='mt-6 mb-6'>{props.error}</p>
        );
    }
    else {
        const { result, label, input} = props;
        return (
            <>
            <p className="mt-6"> Model prediction: <b>{result}</b> </p>
            <p className="mt-2"> Actual rating: <b>{label}</b> </p>
            <p className="mt-2 text-info">Was model correct?</p>
            {result === label ? 
            <p className="text-success text-xl font-bold mt-2">{"Yes! :D"}</p>
            :
            <p className="text-error text-xl font-bold mt-2">{"No :("}</p>
            }
            { input ? null : <p className="text-accent mt-2 mb-6"><b>Review saved to database.</b></p>}
            </>
        )

    }
}