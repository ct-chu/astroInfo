"use client";

import * as React from "react";
import { Box, CardMedia, Grid, Typography } from "@mui/material";
import { AddToHomeScreen } from "react-pwa-add-to-homescreen";

export default function About() {
  return (
    <Grid
      container
      direction="row"
      justifyContent="center"
      alignItems="center"
      sx={{ position: "fixed", top: "7%", bottom: 0 }}
    >
      <Grid item sx={{ width: 0.9 }}>
        <Box sx={{ height: "4rem" }} />
        <CardMedia
              component={"img"}
              sx={{ width: {xs: 0.2, lg: 0.1} }}
              src={"/apple-icon.png"}
            />
        <Box sx={{ height: "2rem" }} />
        <Grid sx={{ width: 0.9 }}>
          <Typography variant="sectionTitle">可觀天文資訊 </Typography>
          <Typography variant="small">
            v0.1
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
            All-sky images from Ho Koon Nature Education cum Astronomical Centre
            (Sponsored by Sik Sik Yuen), Hong Kong Observatory, and Hong Kong
            Space Muesum
            <br />
          </Typography>
          <Typography variant="small">
            Emphemeris by Skyfield (ascl:1907.024)
            <br />
          </Typography>
          <Typography variant="small">
            Solar images from Solar Dynamics Observatory, NASA
            <br />
          </Typography>
        </Grid>
        <Box sx={{ height: "2rem" }} />
        <Grid
          container
          sx={{ width: {xs: "150%" , sm:0.9} }}
          direction="row"
          justifyContent="space-between"
          alignItems="center"
        >
          <Grid item xs={1}>
            <CardMedia component={"img"} src={"/SSY_white.png"} />
          </Grid>
          <Grid item xs={1}>
            <CardMedia
              component={"img"}
              sx={{ width: {xs: "140%" , sm:0.8}}}
              src={"/HK_white.png"}
            />
          </Grid>
          <Grid item xs={9}></Grid>
        </Grid>
        <Box sx={{ height: "20rem" }} />
      </Grid>

      {/* <AddToHomeScreen /> */}
    </Grid>
  );
}
