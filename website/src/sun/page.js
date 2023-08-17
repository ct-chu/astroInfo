"use client";

import * as React from "react"
import { Grid, ImageList, ImageListItem, Typography } from "@mui/material";

export default function Sun() {

    const sunSdoLink = "https://services.swpc.noaa.gov/images/animations//latest.jpg" 

    return (
        <Grid container
        direction="column"
        alignItems="center"
        >
            <Grid item sx={{ width: 0.85}}>
                <Typography variant="sectionTitle">太陽影像 Solar image<br /></Typography>
                <Typography variant="small">Lastest image from HMI, Solar Dynamics Observatory<br /></Typography>
        <ImageList sx={{width: 1}} cols={1} gap={8}>
            <ImageListItem>
              <img
              src={sunSdoLink}
              />
            </ImageListItem>
        </ImageList>
        </Grid>
        </Grid>
    )
}
