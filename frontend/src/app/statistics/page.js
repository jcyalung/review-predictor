"use client";

import axios from "axios";
import { API_LINK } from "../enums";
import { useState, useEffect } from "react";
import Stats from "./stats";
export default function Statistics() {
    const [image, setImage] = useState(null);
    const [stats, setStats] = useState(null);
    
    useEffect(() => {
        axios.get(API_LINK + 'statistics')
        .then((res) => {console.log(res); setImage(res.data.image); setStats(res.data.statistics);})
        .catch((err) => console.log(err));
    },[])
    return (
        <div>
            <h1 className="bullet1">Statistics</h1>
            <div className="flex justify-center items-center gap-4 my-4 max-w-6xl">
            {image ? <img className="rounded-lg shadow-md h-auto" src={`data:image/png;base64,${image}`} alt="Confusion Matrix" /> : null }
            {stats ? <Stats props={stats}/> : null}
            </div>
        </div>
    )
}