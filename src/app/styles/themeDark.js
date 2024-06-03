"use client";

import { createTheme } from "@mui/material";

let theme = createTheme()

const themeDark = createTheme(theme, {
  palette: {
    mode: "dark",
    primary: {
      main: "#fff",
      contrastText: "#fff" //button text white instead of black
    },
    secondary: {
      main: "#222",
      contrastText: "#fff" //button text white instead of black
    },
    background: {
      default: "#000000",
      paper: "#000000",
    },
  },
  components: {
    MuiCssBaseline: {
      background: {
        default: "#000000",
      },
    },
  },
  text: {
    screenTitle: {
      fontSize: "20px",
    },
    sectionTitle: {
      fontSize: "18px",
    },
    content: {
      fontSize: "13px",
    },
    small: {
      fontSize: "8px",
      color: "grey",
    },
  },
  typography: {
    fontFamily: {
      display: "Noto Sans TC",
      body: "Noto Sans TC",
      color: "white",
    },
    button: {
      fontFamily: {
        display: "Noto Sans TC",
        body: "Noto Sans TC",
      },
      fontSize: "calc(14px + 0.5vw)",
      color: "white",
    },
    menu: {
      fontFamily: {
        display: "Noto Sans TC",
        body: "Noto Sans TC",
      },
      [theme.breakpoints.between("xs", "md")]: {
          fontSize: "13 px",
      },
      [theme.breakpoints.between("md", "lg")]: {
          fontSize: "calc(10px + 0.5vw)",
      },
      color: "white",
  },
    sectionTitle: {
      fontSize: "calc(19px + 0.5vw)",
      color: "white",
    },
    content: {
      fontSize: "calc(14px + 0.5vw)",
      color: "white",
    },
    small: {
      fontSize: "calc(12px + 0.5vw)",
      color: "grey",
    },
  },
});

export default themeDark;
