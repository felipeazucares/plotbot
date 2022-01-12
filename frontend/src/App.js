import React, { useState } from "react";
// import logo from "./logo.svg";
import "./App.css";
import LoginForm from "./components/LoginForm";
import TreeContainer from "./components/TreeContainer";
import ControlsContainer from "./components/ControlsContainer";
import SliderContainer from "./components/SliderContainer";
import TextContainer from "./components/TextContainer";
// import OrgChart from "./components/OrgChart"
import Header from "./components/Header";
import { Divider } from "@chakra-ui/react";

export const UserContext = React.createContext({
  user: "",
  setUser: () => {},
});

export const StoryTreeContext = React.createContext({
  storyTree: {},
  setStoryTree: () => {},
});

export const StoryTextContext = React.createContext({
  storyTree: {},
  setStoryTree: () => {},
});
export const TemperatureContext = React.createContext({
  temperature: {},
  setTemperature: () => {},
});

function App() {
  const [user, setUser] = useState("not logged in");
  const value = { user, setUser };
  // this will contain the tree representation
  const [storyText, setStoryText] = useState("");
  const [temperature, setTemperature] = useState(0.7001);
  // this will set the text generated from the tree
  const [storyTree, setStoryTree] = useState({
    name: "Something broke!",
    attributes: { text: "Oops! Check you're logged in!" },
  });

  const tree = { storyTree, setStoryTree };
  const text = { storyText, setStoryText };
  const temp = { temperature, setTemperature };
  return (
    <UserContext.Provider value={value}>
      <StoryTreeContext.Provider value={tree}>
        <StoryTextContext.Provider value={text}>
          <TemperatureContext.Provider value={temp}>
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
                <SliderContainer></SliderContainer>
                <ControlsContainer></ControlsContainer>
              </div>
            </div>
          </TemperatureContext.Provider>
        </StoryTextContext.Provider>
      </StoryTreeContext.Provider>
    </UserContext.Provider>
  );
}

export default App;
