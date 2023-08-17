"use client";

import { createTheme } from "@mui/material";

const themeDark = createTheme({
  overrides: {
    MuiCssBaseline: {
      "#overlay": {
        position: "fixed",
        display: "none",
        width: 1,
        height: 1,
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: "rgba(120,0,0,0.5)",
        zIndex: 2,
      },
      background: {
        default: "#000000",
        paper: "#000000",
      },
    },
  },
  palette: {
    mode: "dark",
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
      display: "Noto",
      body: "Noto",
    },
    button: {
      fontSize: "16px",
    },
    sectionTitle: {
      fontSize: "19px",
    },
    content: {
      fontSize: "16px",
    },
    small: {
      fontSize: "14px",
      color: "grey",
    },
  },
});

export default themeDark;
