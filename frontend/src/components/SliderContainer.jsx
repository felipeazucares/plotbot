import React, { useState, useContext } from "react"
import {
  Tooltip,
  Slider,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
  SliderMark
} from "@chakra-ui/react"
import { TemperatureContext } from "../App"



export default function SliderContainer() {
    const [sliderValue, setSliderValue] = useState(5)
    const [showTooltip, setShowTooltip] = useState(false)
    const {temperature, setTemperature} = useContext(TemperatureContext)
  
    const setTemp=(value)=>{
      setSliderValue(value)
      //convert and set temperature context
      setTemperature(0.7+((0.3/100) * value))
    }
return (
    <div className="App-controls-container">
    <Slider
      id='slider'
      defaultValue={1}
      min={1}
      max={100}
      colorScheme='blue'
      onChange={(v) => setTemp(v)}
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
      aria-label="Creativity"
    >
      <SliderMark value={1} mt='1' ml='-2.5' fontSize='sm'>
        Walter Cronkite
      </SliderMark>
      <SliderMark value={47} mt='1' ml='-2.5' fontSize='sm'>
        Ernest Hemmingway
      </SliderMark>
      <SliderMark value={94} mt='1' ml='-2.5' fontSize='sm'>
        Nic Cage
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