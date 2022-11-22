interface SearchButtonProps {
    children: string;
    onClick: () => void;
}

export default function SearchButton({ children, onClick }: SearchButtonProps) {
    return (
        <button style={buttonStyle} onClick={onClick}>
            {children}
        </button>
    );
}

const buttonStyle = {
    borderRadius: "6px",
    padding: "8px",
    marginRight: "8px",
    backgroundColor: "#f8f9fa",
    borderColor: "#f8f9fa",
    cursor: "pointer",
    boxShadow: "none",
};
