"use client";

import Header from "./header";

export default function ClientLayout({ children }) {
    return (
        <>
            <Header />
            {children}
        </>
    )
}