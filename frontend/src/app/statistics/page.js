"use client";

import axios from "axios";
import { API_LINK } from "../enums";
import { useState, useEffect } from "react";
export default function Statistics() {
    const [image, setImage] = useState(null);

    useEffect(() => {

        axios.get(API_LINK + 'statistics')
        .then((res) => {console.log(res); setImage(res.data.image);})
        .catch((err) => console.log(err));
    },[])
    return (
        <div>
            <h1 className="bullet1">Statistics</h1>
            <div className="flex justify-center items-center my-4">
            {image ? <img className="text-center items-center justify-center " src={`data:image/png;base64,${image}`} alt="Confusion Matrix" /> : null }
            </div>
            
        </div>
    )
}