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

export const PlotbotContext = React.createContext();

function App() {
  return (
    <PlotbotContext.Provider>
      <div className="App">
        <div className="App-header">
          <Header />
        </div>
        <div className="App-row-container">
          <div className="App-content-container">
            <div className="App-content-column">
              <TreeContainer className="App-content-element"></TreeContainer>
            </div>
          </div>
          <div className="App-content-container">
            <div className="App-content-column">
              <TextContainer className="App-content-element"></TextContainer>
            </div>
          </div>
        </div>
        <div>
          <ControlsContainer></ControlsContainer>
          <SliderContainer></SliderContainer>
        </div>
      </div>
    </PlotbotContext.Provider>
  );
}

export default App;
