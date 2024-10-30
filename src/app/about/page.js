"use client";

import * as React from "react";
import { Box, CardMedia, Grid, Typography } from "@mui/material";
import { prefix } from '../prefix.js';
// import { AddToHomeScreen } from "react-pwa-add-to-homescreen";

const versionInfo = "v1.1.0 (20241030)"

export default function About() {
  return (
    <Grid
      container
      direction="row"
      justifyContent="center"
      alignItems="center"
    >
      <Grid item sx={{ width: 0.9 }}>
        <Box sx={{ height: "4rem" }} />
        <CardMedia
          component={"img"}
          sx={{ width: { xs: 0.2, lg: 0.1 } }}
          src={`${prefix}/icons/icon-192x192.png`}
        />
        <Box sx={{ height: "2rem" }} />
        <Grid sx={{ width: 0.9 }}>
          <Typography variant="sectionTitle">
            可觀天文助理
            <br />
          </Typography>
          <Typography variant="sectionTitle">Ho Koon Astro-info </Typography>
          <Typography variant="small">
            {versionInfo}
            <br />
          </Typography>
          <Typography variant="small">
            <br />
            by CT Chu (HKNEAC)
            <br />
            Original python scripts by Thomas K. T. Fok (HKNEAC)
            <br />
            <br />
          </Typography>
          <Typography variant="small">
            Unless specified otherwise, emphemeris, skymaps, polarscope, and other information are all calculated for the geographical location of Ho Koon Natural Education cum Astronomical Centre, HONG KONG.
            <br />
            <br />
            All-sky images from Ho Koon Nature Education cum Astronomical Centre
            (Sponsored by Sik Sik Yuen), Hong Kong Observatory, and Hong Kong
            Space Muesum
            <br />
            Emphemeris by Skyfield (ascl:1907.024, DE421)
            <br />
            Solar images courtesy of NASA/SDO and the AIA, EVE, and HMI science teams.
            <br />
            Sidereal time, which is used to calculate the location of Polaris, is calculated using a modified version of Samuel Etver&apos;s Sidereal time calculater (https://github.com/samuel-etver/sidereal-time).
          </Typography>
        </Grid>
        <Box sx={{ height: "2rem" }} />
        <Grid
          container
          sx={{ width: { xs: "170%", sm: 0.9 } }}
          direction="row"
          justifyContent="space-between"
          alignItems="center"
        >
          <Grid item xs={1}>
            <CardMedia
              component={"img"}
              src={`${prefix}/icons/SSY_white.png`}
            />
          </Grid>
          <Grid item xs={1}>
            <CardMedia
              component={"img"}
              sx={{ width: { xs: "90%", sm: 0.8 } }}
              src={`${prefix}/icons/HK_white.png`}
            />
          </Grid>
          <Grid item xs={9}></Grid>
        </Grid>
        <Box sx={{ height: "8rem" }} />
      </Grid>

      {/* <AddToHomeScreen /> */}
    </Grid>
  );
}
