export default function Logo() {
    return (
        <div>
            <h1 style={headerStyle}>
                <span style={redStyle}>G</span>
                <span style={blueStyle}>o</span>
                <span style={yellowStyle}>o</span>
                <span style={greenStyle}>g</span>
                <span style={redStyle}>l</span>
                <span style={blueStyle}>e </span>

                <span style={yellowStyle}>A</span>
                <span style={blueStyle}>t </span>

                <span style={greenStyle}>H</span>
                <span style={redStyle}>o</span>
                <span style={yellowStyle}>m</span>
                <span style={greenStyle}>e</span>
            </h1>
        </div>
    );
}

const headerStyle = {
    fontSize: "3rem",
    fontWeight: "bold",
};

const redStyle = {
    color: "#DB4437",
};

const blueStyle = {
    color: "#4285F4",
};

const greenStyle = {
    color: "#0F9D58",
};

const yellowStyle = {
    color: "#F4B400",
};
