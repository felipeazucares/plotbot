import React from "react"
import ButtonGetStoryTree from "./ButtonGetStoryTree";

import {
    Button
} from "@chakra-ui/react"
import GetNewTextButton from "./GetNewTextButton";

export default function ControlsContainer() {
return (
    <div className="App-row-container">
      <Button className="flex_button" colorScheme="blue">login</Button>  
      <Button className="flex_button" colorScheme="blue">logout</Button> 
      <ButtonGetStoryTree></ButtonGetStoryTree>
      <GetNewTextButton></GetNewTextButton>
     </div>

  );
}