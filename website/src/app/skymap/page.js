"use client";

import * as React from "react";
import { useState } from "react";
import { ImageList, ImageListItem, Grid, Typography, Box } from "@mui/material";
import Lightbox from "yet-another-react-lightbox";
import "yet-another-react-lightbox/styles.css";
import Zoom from "yet-another-react-lightbox/plugins/zoom";

export default function Skymap() {
  const skymapLink =
    "https://live.staticflickr.com/65535/53121429232_5ed7d059c6_o_d.png"; //for testing
  const skymapChnLink =
    "https://live.staticflickr.com/65535/53122034701_eecb029601_o_d.png"; //for testing
  const [open, setOpen] = useState(false);
  const [lightboxURL, setLightboxURL] = useState(skymapLink);

  return (
    <Grid container direction="column" alignItems="center">
      <Box sx={{ height: "2rem" }} />

      <Grid item sx={{ width: 0.85 }}>
        <ImageList sx={{ width: 1 }} cols={1} gap={8}>
          <Typography variant="sectionTitle">
            即時星圖 Realtime Skymap
            <br />
          </Typography>
          <Typography variant="small">
            按圖放大 Press image to zoom <br />
          </Typography>

          <ImageListItem>
            <img
              src={skymapLink}
              onClick={() => {
                setOpen(true);
                setLightboxURL(skymapLink);
              }}
            />
          </ImageListItem>

          <Box sx={{ height: "2rem" }} />

          <Typography variant="sectionTitle">
            即時中國星圖 Realtime Chinese Skymap
            <br />
          </Typography>
          <Typography variant="small">
            按圖放大 Press image to zoom <br />
          </Typography>

          <ImageListItem>
            <img
              src={skymapChnLink}
              onClick={() => {
                setOpen(true);
                setLightboxURL(skymapChnLink);
              }}
            />
          </ImageListItem>
        </ImageList>
      </Grid>

      <Lightbox
        open={open}
        close={() => setOpen(false)}
        plugins={[Zoom]}
        slides={[
          {
            src: lightboxURL,
          },
        ]}
        render={{
          buttonPrev: () => null,
          buttonNext: () => null,
        }}
      />
    </Grid>
  );
}
