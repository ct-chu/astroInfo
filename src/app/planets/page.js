import * as React from "react";
import { ImageList, ImageListItem, Grid } from "@mui/material";

export default function Planets() {
  const planetImgLink =
    "https://live.staticflickr.com/65535/53121429242_f313301d18_o_d.png"; //for testing

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
      <Grid item>
        <ImageList sx={{ width: 1 }} cols={1} gap={8}>
          <ImageListItem>
            <img src={planetImgLink} />
          </ImageListItem>
        </ImageList>
      </Grid>
    </Grid>
  );
}
