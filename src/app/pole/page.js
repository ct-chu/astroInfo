"use client";

import * as React from "react";
import { useState, useEffect } from "react";
import {Grid, Typography, Box, Switch } from "@mui/material";
import { pink } from "@mui/material/colors";
import { alpha, styled } from '@mui/material/styles';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import "yet-another-react-lightbox/styles.css";
import { Stage, Layer, Star, Text, Circle, Line } from 'react-konva';

function calculateLST() {
    const date = new Date();
    let longitude = 114.108075;
    let iyear = date.getUTCFullYear(); 
    let im = date.getUTCMonth() + 1;
    let iday = date.getUTCDate();
    let ihour = date.getUTCHours();
    let iminute = date.getUTCMinutes();
    let isecond = date.getUTCSeconds();
    let timezone = 8;

    let r = 1296000.0; 
    let longitudeH = longitude/15;
    
    let month = [31,28,31,30,31,30,31,31,30,31,30,31];    

    if (im != 1) {
        let i = Math.round(4*Math.floor(iyear/4));
        if (iyear == i) {
            month[1] = 29
        }
        for (i = 1; i <= im-1; i++)  {
            iday = Math.round(iday) + month[i-1]
        }
    }
    
    let iy = iyear - 1900;    
    iday = Math.floor((iday-1)+(iy-1)/4);
    let t = iday + iy*365.0;
    t = (t+0.5)/36525.0 - 1;
    let t2 = t**2;
    let t3 = t**3;

    let sm = 24110.548410 + 8640184.8128660*t + 0.093104*t2- 0.00000620*t3;
    while (sm <= 0) {
        sm += 86400.0;
    }
    while (sm > 86400) {
        sm -= 86400.0;
    }

    let p = Math.PI/180.0/3600.0;
    let e = p*(84381.448 - 46.8150*t - 0.00059*t2 + 0.0018130*t3);
    let q = p*(450160.280 -   5.0*r*t - 482890.539*t+ 7.455*t2 + 0.0080*t3);
    let d = p*(1072261.3070 + 1236.0*r*t + 1105601.328*t - 6.891*t2+ 0.0190*t3);
    let f = p*(335778.8770 + 1342.0*r*t + 295263.1370*t - 13.2570*t2+ 0.0110*t3);
    let m = p*(1287099.804 +  99.0*r*t+1292581.2240*t -  0.5770*t2 - 0.0120*t3);
    let l = p*(485866.7330+1325.0*r*t + 715922.633*t + 31.3100*t2+ 0.0640*t3);
    
    
    let pl =  -(17.19960 + 0.017420*t) * Math.sin(q);    
    pl += (0.20620 + 0.000020*t)   * Math.sin(2.0*q);
    pl += 0.00460              * Math.sin(q+2.0*f-2.0*l);
    pl += 0.00110              * Math.sin(2.0*(l-f));
    pl -= 0.00030              * Math.sin(2.0*(q+f-l));
    pl -= 0.00030              * Math.sin (l-m-d);
    pl -= 0.00020              * Math.sin (q-2.0*d+2.0*f-2.0*m);
    pl += 0.00010              * Math.sin (q-2.0*f+2.0*l);
    pl -= (1.31870+0.000160*t) * Math.sin (2.0*(q-d+f));
    pl += (0.14260-0.000340*t) * Math.sin (m);
    pl -= (0.05170-0.000120*t) * Math.sin (2.0*q-2.0*d+2.0*f+m);
    pl += (0.02170-0.000050*t) * Math.sin (2.0*q-2.0*d+2.0*f-m);
    pl += (0.01290+0.000010*t) * Math.sin (q-2.0*d+2.0*f);
    pl += 0.00480              * Math.sin (2.0*(l-d));
    pl -= 0.00220              * Math.sin (2.0*(f-d));
    pl += (0.00170-0.000010*t) * Math.sin (2.0*m);
    pl -= 0.00150              * Math.sin (q+m);
    pl -= (0.00160-0.000010*t) * Math.sin (2.0*(q-d+f+m));
    pl -= 0.00120              * Math.sin (q-m);
    pl -= 0.00060              * Math.sin (q+2.0*d-2.0*l);
    pl -= 0.00050              * Math.sin (q-2.0*d+2.0*f-m);
    pl += 0.00040              * Math.sin (q-2.0*d+2.0*l);
    pl += 0.00040              * Math.sin (q-2.0*d+2.0*f+m);
    pl -= 0.00040              * Math.sin (l-d);
    pl += 0.00010              * Math.sin (2.0*l+m-2.0*d);
    pl += 0.00010              * Math.sin (q+2.0*d-2.0*f);
    pl -= 0.00010              * Math.sin (2.0*d-2.0*f+m);
    pl += 0.00010              * Math.sin (2.0*q+m);
    pl += 0.00010              * Math.sin (q+d-l);
    pl -= 0.00010              * Math.sin (m+2.0*f-2.0*d);

    let ps  = -(  0.22740+0.000020*t) * Math.sin (2.0*(q+f));
    ps += (  0.07120+0.000010*t)  * Math.sin (l);
    ps -= (  0.03860+0.000040*t)  * Math.sin (q+2.0*f);
    ps -= 0.03010            * Math.sin (2.0*q+2.0*f+l);
    ps -= 0.01580            * Math.sin (l-2.0*d);
    ps += 0.01230            * Math.sin (2.0*q+2.0*f-l);
    ps += 0.00630            * Math.sin (2.0*d);
    ps += (  0.00630+0.000010*t) * Math.sin (q+l);
    ps -= (  0.00580+0.000010*t) * Math.sin (q-l);
    ps -= 0.00590            * Math.sin (2.0*q+2.0*d+2.0*f-l);
    ps -= 0.00510            * Math.sin (q+2.0*f+l);
    ps -= 0.00380            * Math.sin (2.0*(q+d+f));
    ps += 0.00290            * Math.sin (2.0*l);
    ps += 0.00290            * Math.sin (2.0*q-2.0*d+2.0*f+l);
    ps -= 0.00310            * Math.sin (2.0*(q+f+l));
    ps += 0.00260            * Math.sin (2.0*f);
    ps += 0.00210            * Math.sin (q+2.0*f-l);
    ps += 0.00160            * Math.sin (q+2.0*d-l);
    ps -= 0.00130            * Math.sin (q-2.0*d+l);
    ps -= 0.00100            * Math.sin (q+2.0*d+2.0*f-l);
    ps -= 0.00070            * Math.sin (l+m-2.0*d);
    ps += 0.00070            * Math.sin (2.0*q+2.0*f+m);
    ps -= 0.00070            * Math.sin (2.0*q+2.0*f-m);
    ps -= 0.00080            * Math.sin (2.0*q+2.0*d+2.0*f+l);
    ps += 0.00060            * Math.sin (2.0*d+l);
    ps += 0.00060            * Math.sin (2.0*(q-d+f+l));
    ps -= 0.00060            * Math.sin (q+2.0*d);
    ps -= 0.00070            * Math.sin (q+2.0*d+2.0*f);
    ps += 0.00060            * Math.sin (q-2.0*d+2.0*f+l);
    ps -= 0.00050            * Math.sin (q-2.0*d);
    ps += 0.00050            * Math.sin (l-m);
    ps -= 0.00050            * Math.sin (q+2.0*f+2.0*l);
    ps -= 0.00040            * Math.sin (m-2.0*d);
    ps += 0.00040            * Math.sin (l-2.0*f);
    ps -= 0.00040            * Math.sin (d);
    ps -= 0.00030            * Math.sin (l+m);
    ps += 0.00030            * Math.sin (l+2.0*f);
    ps -= 0.00030            * Math.sin (2.0*q+2.0*f-m+l);
    ps -= 0.00030            * Math.sin (2.0*q+2.0*d+2.0*f-m-l);
    ps -= 0.00020            * Math.sin (q-2.0*l);
    ps -= 0.00030            * Math.sin (2.0*q+2.0*f+3.0*l);
    ps -= 0.00030            * Math.sin (2.0*q+2.0*d+2.0*f-m);
    ps += 0.00020            * Math.sin (2.0*q+2.0*f+m+l);
    ps -= 0.00020            * Math.sin (q-2.0*d+2.0*f-l);
    ps += 0.00020            * Math.sin (q+2.0*l);
    ps -= 0.00020            * Math.sin (2.0*q+l);
    ps += 0.00020            * Math.sin (3.0*l);
    ps += 0.00020            * Math.sin (2.0*q+d+2.0*f);
    ps += 0.00010            * Math.sin (2.0*q-l);
    ps -= 0.00010            * Math.sin (l-4.0*d);
    ps += 0.00010            * Math.sin (2.0*(q+d+f-l));
    ps -= 0.00020            * Math.sin (2.0*q+4.0*d+2.0*f-l);
    ps -= 0.00010            * Math.sin (2.0*l-4.0*d);
    ps += 0.00010            * Math.sin (2.0*q-2.0*d+2.0*f+m+l);
    ps -= 0.00010            * Math.sin (q+2.0*d+2.0*f+l);
    ps -= 0.00010            * Math.sin (2.0*q+4.0*d+2.0*f-2.0*l);
    ps += 0.00010            * Math.sin (2.0*q+4.0*f-l);
    ps += 0.00010            * Math.sin (l-m-2.0*d);
    ps += 0.00010            * Math.sin (q-2.0*d+2.0*f+2.0*l);
    ps -= 0.00010            * Math.sin (2.0*(q+d+f+l));
    ps -= 0.00010            * Math.sin (q+2.0*d+l);
    ps += 0.00010            * Math.sin (2.0*q-2.0*d+4.0*f);
    ps += 0.00010            * Math.sin (2.0*q-2.0*d+2.0*f+3.0*l);
    ps -= 0.00010            * Math.sin (l+2.0*f-2.0*d);
    ps += 0.00010            * Math.sin (q+2.0*f+m);
    ps += 0.00010            * Math.sin (q+2.0*d-m-l);
    ps -= 0.00010            * Math.sin (q-2.0*f);
    ps -= 0.00010            * Math.sin (2.0*q-d+2.0*f);
    ps -= 0.00010            * Math.sin (2.0*d+m);
    ps -= 0.00010            * Math.sin (l-2.0*f-2.0*d);
    ps -= 0.00010            * Math.sin (q+2.0*f-m);
    ps -= 0.00010            * Math.sin (q-2.0*d+m+l);
    ps -= 0.00010            * Math.sin (l-2.0*f+2.0*d);
    ps += 0.00010            * Math.sin (2.0*(l+d));
    ps -= 0.00010            * Math.sin (2.0*q+4.0*d+2.0*f);
    ps += 0.00010            * Math.sin (d+m);

    let sa = sm + (pl+ps)/15.0 * Math.cos(e);

    let toTime = function(lst) {
        let s = (lst/3600) + longitudeH + 1.002737909350795*
          (ihour + iminute/60 + isecond/3600);
    
        if ( s < 0  ) s += 24;
        if ( s >=24 ) s -= 24;
        
        let hour = Math.floor(s);
        let min = (s - hour)*60;
        let sec = (min - Math.floor(min)) * 60;

        return {
            hour: hour,
            minute: Math.floor(min),
            second: sec
        };
    };
    
    return toTime(sa)
  };
  
const polarisAngle = (last) => {
    const polaris = {
        hour: 3,
        minute: 1,
        second: 30.27
    }; //RA of polaris =3h1m30.27s (J2023.6)

    let hourAngleDeg = (last.hour*3600 + last.minute*60 + last.second - polaris.hour*3600 - polaris.minute*60 - polaris.second)/86164.0905*360;
    
    let angle = 360 - hourAngleDeg;

    (angle > 360) ? (angle = angle%360) : (angle = angle)

    return angle
}

const DrawPole = () => {
  const last = calculateLST()
  const angle = polarisAngle(last) *0.0174533
  const graphTime = new Date().toLocaleString()
  const [inversion, setInversion] = useState(false)
  const [lateralInversion, setLateralInversion] = useState(false)

  // useEffect(() => {
    
  // })
  // const changeInversion = useState(!inversion)
  // const changeLateralInversion = useState(!lateralInversion)

  let polX = lateralInversion === false ? (150 + 110*Math.sin(angle)) : (-1 * (150 + 110*Math.sin(angle)))
  let polY = inversion === false ? (150 - 110*Math.cos(angle)) : (-1 * (150 - 110*Math.cos(angle)))

  const PinkSwitch = styled(Switch)(({ theme }) => ({
    '& .MuiSwitch-switchBase.Mui-checked': {
      color: pink[600],
      '&:hover': {
        backgroundColor: alpha(pink[600], theme.palette.action.hoverOpacity),
      },
    },
    '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
      backgroundColor: pink[600],
    },
  }));
  

  return (
  <Grid item>
  <Stage width={300} height={300}>
    <Layer>
      {/* Graph time */}
      <Text x={40} y={15} fontSize={13} fill='#555' align="center" text={"Generated at: " + graphTime}/>
      {/* outer circle */}
      <Circle x={150} y={150} radius={110} stroke="#555"/>
      {/* marking on outer circle */}
      <Line stroke="#555" points={[150, 40, 150, 60]} />
      <Line stroke="#555" points={[150, 240, 150, 260]} />
      <Line stroke="#555" points={[40, 150,60, 150]} />
      <Line stroke="#555" points={[240, 150,260, 150]} />
      <Line stroke="#555" points={[72.22, 72.22, 86.36, 86.36]} />
      <Line stroke="#555" points={[213.64, 213.64, 227.78, 227.78]} />
      <Line stroke="#555" points={[72.22, 227.78, 86.36, 213.64]} />
      <Line stroke="#555" points={[227.78, 72.22, 213.64, 86.36]} />
      {/* cross in centre */}
      <Line stroke="#555" points={[150, 140, 150, 160]} />
      <Line stroke="#555" points={[140, 150, 160, 150]} />
      <Text x={130} y={165} fontSize={20} fill='#FFF' align="center" text="NCP"/>
      {/* polaris */}
      <Star numPoints={5} innerRadius={4} outerRadius={8} x={polX} y={polY} fill="#FFF"/>
      {/* Inversion */}
      <Text x={110} y={275} fontSize={13} fill='#555' align="center" text={"Correct Image"} />
    </Layer>
  </Stage>
  <Box sx={{ height: "1rem" }} />
  <FormGroup>
    {/* <FormControlLabel control={<PinkSwitch onChange={() => changeLateralInversion}/>} label="Laterally inverted (LR)?"/>
    <FormControlLabel control={<PinkSwitch onChange={() => changeInversion}/>} label="Inverte (UD)?"/> */}
    <FormControlLabel disabled control={<PinkSwitch />} label="Laterally inverted (LR)?"/>
    <FormControlLabel disabled control={<PinkSwitch />} label="Inverted (UD)?"/>
  </FormGroup>
  </Grid>
)}

export default function Pole() {

  return (
    <Grid
      container
      direction="column"
      alignItems="center"
      xs={12}
      sm={10}
      md={8}
      lg={6}
    >
      <Box sx={{ height: "2rem" }} />

      <Grid item>

          <Typography variant="sectionTitle">
            北極星位置 Polaris location
            <br />
          </Typography>
          
        
        </Grid>
      <DrawPole />
      <Box sx={{ height: "2rem" }} />

    </Grid>
  );
}
