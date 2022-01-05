import React, { useState } from "react"
import {
  Tooltip,
  Slider,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
  SliderMark
} from "@chakra-ui/react"



export default function SliderContainer() {
    const [sliderValue, setSliderValue] = useState(5)
    const [showTooltip, setShowTooltip] = useState(false)
return (
    <div className="App-controls-container">
    <Slider
      id='slider'
      defaultValue={5}
      min={0}
      max={100}
      colorScheme='blue'
      onChange={(v) => setSliderValue(v)}
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
      aria-label="Creativity"
    >
      <SliderMark value={1} mt='1' ml='-2.5' fontSize='sm'>
        Walter Kronkite
      </SliderMark>
      <SliderMark value={50} mt='1' ml='-2.5' fontSize='sm'>
        Hemmingway
      </SliderMark>
      <SliderMark value={93.8} mt='1' ml='-2.5' fontSize='sm'>
        Nicholas Cage
      </SliderMark>
      <SliderTrack>
        <SliderFilledTrack />
      </SliderTrack>
      <Tooltip
        hasArrow
        bg='blue.500'
        color='white'
        placement='top'
        isOpen={showTooltip}
        label={`${sliderValue}%`}
      >
        <SliderThumb boxSize={7}/>
      </Tooltip>
    </Slider>   
     </div>

  );
}