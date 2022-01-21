import React, { useState } from "react";
// import env from "react-dotenv";
// import logo from "./logo.svg";
import "./App.css";
import TreeContainer from "./components/TreeContainer";
import ControlsContainer from "./components/ControlsContainer";
import SliderContainer from "./components/SliderContainer";
import TextContainer from "./components/TextContainer";
// import OrgChart from "./components/OrgChart"
import Header from "./components/Header";

// export function MyComponent() {
//   return <div>env is: {env.REACT_APP_BASEAPIURL}</div>;
// }

export const URLContext = React.createContext({
  baseAPIURL: "",
  setURL: () => {},
});

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
  let baseurl = process.env.REACT_APP_BASEAPIURL;
  if (baseurl === undefined) {
    baseurl = "http://localhost:8450";
    console.log(`No BASEAPIURL env value found setting to: ${baseurl}`);
  }

  const [baseAPIURL, setURL] = useState(baseurl);
  const [user, setUser] = useState("not logged in");
  // this will contain the tree representation
  const [storyText, setStoryText] = useState("");
  const [temperature, setTemperature] = useState(parseFloat(0.7));
  // this will set the text generated from the tree
  const [storyTree, setStoryTree] = useState({
    name: "Something broke!",
    attributes: {
      text: "Oops! Check you're logged in by clicking the Start button!",
    },
  });

  const value = { user, setUser };
  const tree = { storyTree, setStoryTree };
  const text = { storyText, setStoryText };
  const temp = { temperature, setTemperature };
  const url = { baseAPIURL, setURL };
  return (
    <UserContext.Provider value={value}>
      <StoryTreeContext.Provider value={tree}>
        <StoryTextContext.Provider value={text}>
          <TemperatureContext.Provider value={temp}>
            <URLContext.Provider value={url}>
              <div className="App">
                <div className="App-header">
                  <Header />
                </div>
                {/* <Divider></Divider> */}
                <div className="App-row-container">
                  <div className="App-content-container-75">
                    <div className="App-content-column">
                      <TreeContainer className="App-content-element"></TreeContainer>
                    </div>
                  </div>
                  <div className="App-content-container-25">
                    <div className="App-content-column">
                      <TextContainer className="App-content-element"></TextContainer>
                    </div>
                  </div>
                </div>
                <div>
                  <SliderContainer></SliderContainer>
                  <ControlsContainer></ControlsContainer>
                </div>
              </div>
            </URLContext.Provider>
          </TemperatureContext.Provider>
        </StoryTextContext.Provider>
      </StoryTreeContext.Provider>
    </UserContext.Provider>
  );
}

export default App;
