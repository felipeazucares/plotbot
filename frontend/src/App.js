import React from "react";
// import logo from "./logo.svg";
import "./App.css";
import LoginForm from "./components/LoginForm";
import TreeContainer from "./components/TreeContainer";
import ControlsContainer from "./components/ControlsContainer";
import SliderContainer from "./components/SliderContainer";
import TextContainer from "./components/TextContainer";
import OrgChart from "./components/OrgChart";
import Header from "./components/Header";
import { Divider } from "@chakra-ui/react";

export const PlotbotContext = React.createContext();

const user = {
  name: "Philip Suggars",
  email: "psuggars@NodeStack.com",
};

function App() {
  return (
    <PlotbotContext.Provider value={user}>
      <div className="App">
        <div className="App-header">
          <Header />
        </div>
        <Divider></Divider>
        <div className="App-row-container">
          <div className="App-content-container-75">
            <div className="App-content-column">
              <TreeContainer className="App-content-element"></TreeContainer>
            </div>
          </div>
          <div className="App-content-container-25">
            <div className="App-content-column">
              <TextContainer className="App-content-element"></TextContainer>
              <LoginForm></LoginForm>
            </div>
          </div>
        </div>
        <Divider></Divider>
        <div>
          <ControlsContainer></ControlsContainer>
          <SliderContainer></SliderContainer>
        </div>
      </div>
    </PlotbotContext.Provider>
  );
}

export default App;
