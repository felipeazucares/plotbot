import React from "react"
import {
    Button, 
  Slider,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
  SliderMark,
} from "@chakra-ui/react"

export default function ControlsContainer() {
return (
    <div className="App-row-container">
      <Button className="flex_button" colorScheme="blue">login</Button>  
      <Button className="flex_button" colorScheme="blue">logout</Button> 
      <Button className="flex_button"colorScheme="blue">get texts</Button>  
      <Button className="flex_button" colorScheme="blue">get story</Button> 
       <Slider aria-label='slider-ex-1' defaultValue={30}>
        <SliderTrack>
          <SliderFilledTrack />
        </SliderTrack>
        <SliderThumb />
      </Slider>    
     </div>

  );
}