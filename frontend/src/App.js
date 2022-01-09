import React, { useState } from "react";
// import logo from "./logo.svg";
import "./App.css";
import LoginForm from "./components/LoginForm";
import TreeContainer from "./components/TreeContainer";
import ControlsContainer from "./components/ControlsContainer";
import SliderContainer from "./components/SliderContainer";
import TextContainer from "./components/TextContainer";
// import OrgChart from "./components/OrgChart";
import Header from "./components/Header";
import { Divider } from "@chakra-ui/react";

// const user = {
//   name: "Philip Suggars",
//   email: "psuggars@NodeStack.com",
// };

export const PlotbotContext = React.createContext({
  user: "",
  setUser: () => {},
});

function App() {
  const [user, setUser] = useState("not logged in");
  const value = { user, setUser };
  console.log(`app user:${user}`);
  return (
    <PlotbotContext.Provider value={value}>
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
