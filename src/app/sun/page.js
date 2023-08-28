"use client";

import * as React from "react";
import { Grid, ImageList, ImageListItem, Typography, Box } from "@mui/material";

export default function Sun() {
  const sunHmi =
    "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg";
  const sunAia =
    "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0304.jpg";
  const sunActive =
    "http://jsoc.stanford.edu/doc/data/hmi/harp/harp_nrt/latest_nrt.png";

  return (
    <Grid
      container
      direction="column"
      alignItems="center"
      spacing={2}
      xs={12}
      sm={10}
      md={8}
      lg={6}
    >
      <Grid item sx={{ width: 0.85 }}>
        <Box sx={{ height: "2rem" }} />
        <Typography variant="sectionTitle">
          太陽影像 Solar image
          <br />
        </Typography>
        <Typography align="center" variant="small">
          Lastest images from Solar Dynamics Observatory
          <br />
          <br />
        </Typography>
        <Typography variant="content">
          HMI<br />
        </Typography>
        <ImageList sx={{ width: 1 }} cols={1} gap={8}>
          <ImageListItem>
            <img src={sunHmi} />
          </ImageListItem>
        </ImageList>
        <Box sx={{ height: "2rem" }} />
        <Typography align="center" variant="content">
          AIA 304 Å <br />
        </Typography>
        <ImageList sx={{ width: 1 }} cols={1} gap={8}>
          <ImageListItem>
            <img src={sunAia} />
          </ImageListItem>
        </ImageList>
        <Box sx={{ height: "2rem" }} />
        <Typography align="center" variant="content">
          HMI Active Region Patch<br /><br />
        </Typography>
        <ImageList sx={{ width: 1 }} cols={1} gap={8}>
          <ImageListItem>
            <img src={sunActive} />
          </ImageListItem>
        </ImageList>
      </Grid>
      <Box sx={{ height: "2rem" }} />
    </Grid>
  );
}
