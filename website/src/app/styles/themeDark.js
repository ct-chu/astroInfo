"use client";

import { createTheme } from "@mui/material";

const themeDark = createTheme({
    palette: {
        mode: 'dark',
        background: {
            default: "#000000"
        },
    },
    text: {
        screenTitle: {
            fontSize: '20px',
            
        },
        sectionTitle: {
            fontSize: '18px',
        },
        content: {
            fontSize: '15px',
        },
    },
    typography: {
        fontFamily: "'Montserrat', 'Noto Sans TC', sans-serif", 
        button: {
            textTransform: "none",
        }
    },
});

export default themeDark;