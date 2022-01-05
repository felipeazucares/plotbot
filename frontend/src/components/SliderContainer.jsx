import React from "react"
import {
    Button, 
  Slider,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
  SliderMark,
} from "@chakra-ui/react"

export default function SliderContainer() {
return (
    <div className="App-row-container">
       <Slider aria-label='slider-ex-1' defaultValue={30}>
        <SliderTrack>
          <SliderFilledTrack />
        </SliderTrack>
        <SliderThumb />
      </Slider>    
     </div>

  );
}