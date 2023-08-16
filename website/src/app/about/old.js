"use client";

import * as React from "react"
import { useState, useEffect} from "react";
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Card, CardMedia, CardContent, Typography, Box } from "@mui/material";
import Lightbox from "yet-another-react-lightbox";
import "yet-another-react-lightbox/styles.css";
import Zoom from "yet-another-react-lightbox/plugins/zoom";
import axios from "axios";

import Weather from "./pages/weather";
import Planets from "./pages/planets";
import Skymap from "./pages/skymap";
import About from "./pages/about"
import NotFoundPage from "./pages/404"

export default function Index() {

    return (
        <Typography>index</Typography>
    //     <Container>
    //     <BrowserRouter>
    //       <Routes>
    //         <Route exact path="/" element={<Index />} />
    //         <Route path="/weather" element={<Index />} />
    //         <Route path="/index" element={<Index />} />
    //         <Route path="/planets" element={<Planets />} />
    //         <Route path="/skymap" element={<Skymap />} />
    //         <Route path="/about" element={<About />} />
    //         <Route path="*" element={<NotFoundPage />} />
    //       </Routes>
    //     </BrowserRouter>
    //   </Container>
    )
}