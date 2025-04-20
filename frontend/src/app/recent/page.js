"use client";
import axios from "axios";
import { useState, useEffect } from "react";
import { API_LINK } from "../enums";
export default function RecentPage() {
    const [reviews, setReviews] = useState([]);
    const [sort, setSort]       = useState(false);

    useEffect(() => {
        axios.get(API_LINK + 'all-reviews')
        .then((res) => {setReviews(res.data.reviews);})
        .catch((err) => console.log(err));
    }, []);

    const sortedReviews = [...reviews].sort((a, b) => {
        if (a.media_name < b.media_name) return sort ? -1 : 1;
        if (a.media_name > b.media_name) return sort ? 1 : -1;
        return 0;
    });

    const toggleSort = () => setSort((prev) => !prev);
    return (
        <div className="recent">
            <h1 className='bullet2'>Recent Reviews</h1>
            <div className="max-h-[700px] mx-auto overflow-y-auto max-w-6xl">
            <table className="table w-full text-left border-separate border-spacing-y-2">
                <thead className="sticky top-0 z-10 bg-secondary text-black">
                    <tr>  
                        <th>IMDB username</th>
                        <th className="cursor-pointer" onClick={toggleSort}> media name {sort ? "↑" : "↓"}</th>
                        <th>episode name</th>
                        <th>rating score</th>
                        <th>model prediction</th>
                        <th>review</th>
                    </tr>
                </thead>
                <tbody>
                    {sortedReviews.map((row, i) => (
                        <tr className="bg-base-200 hover:bg-base-600 border-b-4 border-base-200" key={i}>
                            <td><a className="underline text-info" href={row.link} target="_blank">{row.user}</a></td>
                            <td>{row.media_name}</td>
                            <td>{row.episode_name || "N/A"}</td>
                            {row.score === "positive" ? <td className="text-success font-bold">positive</td> : <td className="text-error font-bold">negative</td>} 
                            {row.prediction === "positive" ? <td className="text-success font-bold">positive</td> : <td className="text-error font-bold">negative</td>} 
                            <td>{row.review}</td>
                        </tr>
                    ))
                    }
                </tbody>
            </table>
            </div>
        </div>
    );
}