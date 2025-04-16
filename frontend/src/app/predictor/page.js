"use client";
import axios, { AxiosError } from "axios";
import { useState } from "react";
export default function Predictor() {
    const API_LINK = "http://localhost:8000/"
    const [model, setModel] = useState("nb");
    const [type, setType] = useState(0);
    // nb svm log_reg
    const handleSubmit = async (event) => {
        event.preventDefault();

        const payload = {
            url: event.currentTarget.url.value,
            model: model,
            input: event.currentTarget.input || null,
            label: event.currentTarget.label || null,
        };

        try {
            const { data } = await axios.post(API_LINK + "predict-review", payload);
            
            console.log(data);
        } catch(e) {
            const error = e;
            const { message, response } = error;
            const error_msg = response.data.detail.message[0];
            alert(`${error.message}: ${error_msg}`);
        }
    }
    return (
        <div>
            <h1 className="bullet1">Predict IMDB Reviews</h1>
            <div className="selector">
            <input type="radio" name="selector" id="text-input" className="hidden peer/text" onChange={() => setType(0)} defaultChecked />
            <label htmlFor="text-input" className="text-input"> Text Input </label>
            <input type="radio" name="selector" id="imdb-link" className="hidden peer/imdb" onChange={() => setType(1)} />
            <label htmlFor="imdb-link" className="imdb-link"> IMDB Link </label>
            </div>
            { type === 0 ? 
            (
                // text-input form
            <>
                <h1 className='form-heading'>Predict Rating via Text Input</h1>
                <form onSubmit={handleSubmit} className="text-form">
                    <div className="text-form">
                        <h2 className="heading2">Input</h2>
                        <textarea 
                            type="text"
                            id="input"
                            name="input"
                            placeholder="This movie is great!"
                            required
                            className="textarea textarea-border w-3xl min-h-32 items-center justify-center text-center"
                        />
                        <h2 className="heading2">Rating</h2>
                        <div className="rating-selector">
                        <input type="radio" name="label" id="positive-rating" className="hidden peer/positive" onChange={() => console.log(type)} defaultChecked />
                        <label htmlFor="positive-rating" className="positive-rating"> Positive </label>
                        <input type="radio" name="label" id="negative-rating" className="hidden peer/negative" onChange={() => console.log(type)} />
                        <label htmlFor="negative-rating" className="negative-rating"> Negative </label>
                        </div>
                    </div>
                    <button className="btn btn-warning justify-center">Submit Link</button>
                </form>
            </>
            ) :
            (
                // imdb-link form
            <>
                <h1 className='form-heading'>Predict IMDB Movie Review Rating</h1>
                <form onSubmit={handleSubmit} className="imdb-form">
                    <div className="imdb-form">
                        <label htmlFor="url">URL:</label>
                        <input 
                            type="text"
                            id="url"
                            name="url"
                            required
                            className="border rounded border-primary"
                        />
                    </div>
                    <button className="btn btn-warning">Submit Link</button>
                </form>
            </>
            )}
        </div>
    )
}