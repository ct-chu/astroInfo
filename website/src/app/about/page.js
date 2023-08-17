"use client";

import * as React from "react"
import { Box, Card, Grid, Typography } from "@mui/material";
import { AddToHomeScreen } from 'react-pwa-add-to-homescreen';

export default function About() {

    return (
        <Grid container
            direction="row"
            justifyContent="center"
            alignItems="center"
            sx={{position: "fixed", top: 0, bottom: 0}}
        >
            <Grid item sx={{width: 0.9}}>
            <Box sx={{ height:"2rem" }} />
                <Grid item sx={{width: 0.9}}>
                <Typography variant="sectionTitle">可觀天文資訊  </Typography>
                <Typography variant="small">v0.1<br /></Typography>
                <Typography variant="small"><br />by CT Chu (HKNEAC)<br />Original python scripts by Thomas K. T. Fok (HKNEAC)<br /><br /></Typography>
                <Typography variant="small">All-sky images from Ho Koon Nature Education cum Astronomical Centre (Sponsored by Sik Sik Yuen), Hong Kong Observatory, and Hong Kong Space Muesum<br /></Typography>
                <Typography variant="small">Emphemeris by Skyfield (ascl:1907.024)<br /></Typography>
                <Typography variant="small">Solar image from Solar Dynamics Observatory, NASA<br /></Typography>
                </Grid>
                <Box sx={{ height:"2rem" }} />
            </Grid>
            
            <AddToHomeScreen />
        
        </Grid>
    )
}
