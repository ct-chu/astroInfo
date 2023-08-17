import * as React from "react"
import { ImageList, ImageListItem } from "@mui/material";

export default function Planets() {

    const planetImgLink = "https://live.staticflickr.com/65535/53121429242_f313301d18_o_d.png" //for testing

    return (
        <ImageList sx={{width: 1}} cols={1} gap={8}>
            <ImageListItem>
              <img
              src={planetImgLink}
              />
            </ImageListItem>
        </ImageList>
    )
}
