import React from "react";
import "./App.css";
import Logo from "./components/Logo";
import Searchbox from "./components/Searchbox";
import SearchButton from "./components/SearchButton";

function App() {
    const [results, setResults] = React.useState([]);

    async function search() {
        console.log("trykket på søk");
        const a = await fetch(
            "http://localhost:8000/search?query=%22leder%22&res=2"
        ).then((res) => {
            return res.json();
        });

        console.log("svar fra api", a);
    }

    return (
        <div className="App" style={containerStyle}>
            <Logo />
            <Searchbox />
            <div>
                <SearchButton onClick={() => search()}>Google-søk</SearchButton>
                <SearchButton onClick={() => search()}>
                    Jeg prøver lykken
                </SearchButton>
            </div>

            {results && (
                <div>
                    <h2>Resultater</h2>
                    {results}
                </div>
            )}
        </div>
    );
}

export default App;

const containerStyle = {
    paddingTop: "12rem",
};
