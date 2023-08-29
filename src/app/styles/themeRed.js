"use client";

import { createTheme } from "@mui/material";

let theme = createTheme()

const themeRed = createTheme(theme, {
  palette: {
    mode: "dark",
    background: {
      default: "#000000",
      paper: "#000000",
    },
    primary: {
        main: "#992222",
      },
      secondary: {
        main: "#200",
        contrastText: "#fff" //button text white instead of black
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
        fontFamily: {
            display: "Noto",
            body: "Noto",
          },
      fontSize: "calc(14px + 0.5vw)",
      color: "#cc3d3d",
    },
    menu: {
        fontFamily: {
            display: "Noto",
            body: "Noto",
          },
        [theme.breakpoints.between("xs", "md")]: {
            fontSize: "13 px",
        },
        [theme.breakpoints.between("md", "lg")]: {
            fontSize: "calc(10px + 0.5vw)",
        },
        color: "#cc3d3d",
    },
    sectionTitle: {
      fontSize: "calc(19px + 0.5vw)",
      color: "#cc3d3d",
    },
    content: {
      fontSize: "calc(14px + 0.5vw)",
      color: "#cc3d3d",
    },
    small: {
      fontSize: "calc(12px + 0.5vw)",
      color: "#882c2c",
    },
  },
});

export default themeRed;
