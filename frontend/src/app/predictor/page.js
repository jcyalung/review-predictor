"use client";
import axios, { AxiosError } from "axios";
import { useState } from "react";
import Result from "./result";
import { API_LINK } from "../enums";
export default function Predictor() {
    const [model, setModel] = useState("nb");
    const [type, setType] = useState(0);
    const [label, setLabel] = useState("positive");
    const [modal, setModal] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(false);
    // nb svm log_reg
    const handleSubmit = async (event) => {
        event.preventDefault();
        const payload = type === 0 ? {
            model: model,
            review: event.currentTarget.input.value,
            label: label,
        } :
        {
            model: model,
            url: event.currentTarget.url.value,

        }
        setModal(true);        
        try {
            const { data } = type === 0 ? await axios.post(API_LINK + "predict-input", payload) : await axios.post(API_LINK + "predict-review", payload);
            setResult(data);
        } catch(e) {
            const { message, response } = e;
            setError(true);
            if(message === "Network Error") {
                setResult(({'error' : 'Backend is down, please check if the backend is running!'}));
            }
            else {
                const error_msg = response.data.detail.message[0];
                setResult({'error' : error_msg});
            }
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
                    <div className="text-form w-full max-w-4xl mx-auto p-8 bg-gray-400 rounded-2xl shadow-lg">
                        <h2 className="heading2">Input</h2>
                        <div className="w-full flex justify-center">
                          <textarea 
                            id="input"
                            name="input"
                            placeholder="This movie is great!"
                            required
                            className="textarea textarea-bordered w-full max-w-3xl min-h-32 text-center resize-none rounded-2xl"
                          />
                        </div>
                        <h2 className="heading2">Rating</h2>
                        <div className="rating-selector">
                        <input type="radio" name="label" id="positive-rating" className="hidden peer/positive" onChange={() => setLabel("positive")} defaultChecked />
                        <label htmlFor="positive-rating" className="positive-rating"> Positive </label>
                        <input type="radio" name="label" id="negative-rating" className="hidden peer/negative" onChange={() => setLabel("negative")} />
                        <label htmlFor="negative-rating" className="negative-rating"> Negative </label>
                        </div>

                        <h2 className="heading2">Model</h2>
                        <div className="model-selector">
                        <input type="radio" name="model" id="nb" className="hidden peer/nb" onChange={() => setModel("nb")} defaultChecked />
                        <label htmlFor="nb" className="nb"> MNB </label>
                        <input type="radio" name="model" id="svm" className="hidden peer/svm" onChange={() => setModel("svm")} />
                        <label htmlFor="svm" className="svm"> SVM </label>
                        <input type="radio" name="model" id="lr" className="hidden peer/lr" onChange={() => setModel("log_reg")} />
                        <label htmlFor="lr" className="lr"> LogReg </label>
                        </div>
                    </div>
                    <button className="btn btn-accent mt-8">Submit</button>
                </form>
            </>
            ) :
            (
                // imdb-link form
            <>
                <h1 className='form-heading'>Predict IMDB Movie Review Rating</h1>
                <form onSubmit={handleSubmit} className="text-form">
                    <div className="text-form w-full max-w-4xl mx-auto p-8 bg-gray-400 rounded-2xl shadow-lg">
                        <h2 className="heading2">Link</h2>
                        <div className="w-full flex justify-center mt-3">
                          <input 
                            id="url"
                            name="url"
                            placeholder="https://imdb.com/"
                            required
                            className="bg-white w-1/2 text-center resize-none rounded-2xl"
                          />
                        </div>

                        <h2 className="heading2">Model</h2>
                        <div className="model-selector">
                        <input type="radio" name="model" id="nb" className="hidden peer/nb" onChange={() => setModel("nb")} defaultChecked />
                        <label htmlFor="nb" className="nb"> MNB </label>
                        <input type="radio" name="model" id="svm" className="hidden peer/svm" onChange={() => setModel("svm")} />
                        <label htmlFor="svm" className="svm"> SVM </label>
                        <input type="radio" name="model" id="lr" className="hidden peer/lr" onChange={() => setModel("log_reg")} />
                        <label htmlFor="lr" className="lr"> LogReg </label>
                        </div>
                    </div>
                    <button className="btn btn-accent mt-8">Submit</button>
                </form>
            </>
            )}
            {modal && (
                <div className="fixed inset-0 backdrop-blur-sm flex items-center justify-center z-50 transition-opacity duration-300">
                <div className="bg-white dark:bg-neutral p-6 rounded-2xl shadow-lg w-full max-w-md text-center transform scale-95 animate-fade-in-up">
                    {error ? 
                    <h2 className="text-xl font-bold mb-4 text-error">An error occurred!</h2>
                    : 
                    <h2 className="text-xl font-bold mb-4 text-secondary">Prediction</h2> }
                    {result ? 
                    <Result props={result}/>
                    : 
                    <p className="mb-6"> Predicting... </p>
                    }
                    <button 
                        className="btn btn-accent mt-6" 
                        onClick={() => { setModal(false); setResult(""); setError(false); }}
                        >Close
                    </button>
                </div>
                </div>
                )}
        </div>
    )
}