"use client";
import axios, { AxiosError } from "axios";
import { useState } from "react";
export default function Predictor() {
    const API_LINK = "http://localhost:8000/"
    const [model, setModel] = useState("nb");
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
            <input type="radio" name="selector" id="text-input" className="hidden peer/text" defaultChecked />
            <label htmlFor="text-input" className="text-input"> Text Input </label>
            <input type="radio" name="selector" id="imdb-link" className="hidden peer/imdb"/>
            <label htmlFor="imdb-link" className="imdb-link"> IMDB Link </label>
            </div>
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
            </form>
        </div>
    )
}