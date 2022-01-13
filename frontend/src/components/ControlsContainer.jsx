import React from "react"
import ButtonRestart from "./ButtonRestart"
import {
    Button, Container
} from "@chakra-ui/react"
// import GetNewTextButton from "./ButtonGetNewText";

export default function ControlsContainer() {
return (
    <div className="App-controls-container">
      <ButtonRestart></ButtonRestart>
     </div>
  );
}