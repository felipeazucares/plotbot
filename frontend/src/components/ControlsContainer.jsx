import React from "react"
import ButtonGetStoryTree from "./ButtonGetStoryTree";
import {
    Button
} from "@chakra-ui/react"

export default function ControlsContainer() {
return (
    <div className="App-row-container">
      <Button className="flex_button" colorScheme="blue">login</Button>  
      <Button className="flex_button" colorScheme="blue">logout</Button> 
      <Button className="flex_button"colorScheme="blue">get texts</Button>  
      <ButtonGetStoryTree colorScheme="blue"></ButtonGetStoryTree> 

     </div>

  );
}