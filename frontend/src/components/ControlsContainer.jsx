import React from "react"
import ButtonRestart from "./ButtonRestart"
import {
    Button, Container
} from "@chakra-ui/react"
// import GetNewTextButton from "./ButtonGetNewText";

export default function ControlsContainer() {
return (
    <div className="App-controls-container">
      <Button className="flex_button" colorScheme="blue">login</Button>  
      <Button className="flex_button" colorScheme="blue">logout</Button> 
      <ButtonRestart></ButtonRestart>
     </div>
  );
}