import React from "react"
import ButtonGetStoryTree from "./ButtonGetStoryTree";
import ButtonGetNewText from "./ButtonGetStoryTree";
import {
    Button
} from "@chakra-ui/react"

export default function ControlsContainer() {
return (
    <div className="App-row-container">
      <Button className="flex_button" colorScheme="blue">login</Button>  
      <Button className="flex_button" colorScheme="blue">logout</Button> 
      <ButtonGetNewText colorScheme="blue"></ButtonGetNewText>  
      <ButtonGetStoryTree colorScheme="blue"></ButtonGetStoryTree> 

     </div>

  );
}