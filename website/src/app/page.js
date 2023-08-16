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


export default function Home() {
  
  const [open, setOpen] = useState(false);
    const [weatherData, setWeatherData] = useState("");
    const [error, setError] = useState(false);
    const [state, setState] = useState("");
    
    useEffect(() => {
        setState("loading");
        axios
          .get(
            "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en"
          )
          .then((res) => {
            setState("success");
            setWeatherData(
              [`https://www.hko.gov.hk/images/HKOWxIconOutline/pic${res.data.icon[0]}.png`, res.data.temperature.data[14].value, res.data.humidity.data[0].value, res.data.uvindex.data[0].desc]
            );
            console.log(weatherData);
          })
          .catch((err) => {
            console.error("Error:", err);
            setState("error");
            setError(err);
          });
      }, []);
      if (state === "error") return <h1>{error.toString()}</h1>;

      const WeatherCard = () => {
        return (
            <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                <CardContent sx={{ flex: '1 0 auto' }}>
                    <Typography component="div" variant="content">
                        Air temp: {weatherData[1]} °C
                    </Typography>
                    <Typography component="div" variant="content">
                        Humidity: {weatherData[2]} %
                    </Typography>
                    <Typography component="div" variant="content">
                        UV intensity: {weatherData[3]}
                    </Typography>
                </CardContent>
                <CardMedia
                    component="img"
                    sx={{ width: 0.2 }}
                    image={weatherData[0]}
                    alt="Current weather"
                />
            </Box>
        )
      }
  
  return(
    <>
      <Card sx={{ width: 1 }}>
        <CardContent>
            <Typography variant="content">即時全天影像</Typography>
        </CardContent>
        <CardMedia
            sx={{ width: 1 }}
            image="./temp/Hokoon_ASC.png"
            onClick={() => setOpen(true)}
        />
      </Card>
      <Card sx={{ width: 1 }}>
          <CardContent>
              <Typography variant="content">Weather Info</Typography>
          </CardContent>
          {state === "loading" ? <h1>Loading...</h1> : <WeatherCard />}
      </Card>
      <Lightbox
          open={open}
          close={() => setOpen(false)}
          plugins={[Zoom]}
          slides={[{ src: "./temp/Hokoon_ASC.png" }]}
          render={{
              buttonPrev: () => null,
              buttonNext: () => null
          }}
      />
  </>
  )
}
