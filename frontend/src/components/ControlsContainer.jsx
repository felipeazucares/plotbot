import React from "react"
import {
    Button, Slider
} from "@chakra-ui/react"

export default function ControlsContainer() {
return (
    <div className="App-row-container">
      <Button className="flex_button" colorScheme="blue">login</Button>  
      <Button className="flex_button" colorScheme="blue">logout</Button> 
      <Button className="flex_button"colorScheme="blue">get texts</Button>  
      <Button className="flex_button" colorScheme="blue">get story</Button> 
      {/* <button type="button">logon</button>
      <button type="button">logoff</button>
      <button type="button">get story</button>
      <button type="button">get text</button> */}
     </div>
  );
}