import React from "react";
// import logo from "./logo.svg";
import "./App.css";
import LoginForm from "./components/LoginForm";
import TreeContainer from "./components/TreeContainer";
import ControlsContainer from "./components/ControlsContainer";
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
          <article className="App-tree-container">
            <div className="App-tree-column">
              <TreeContainer className="App-tree-element"></TreeContainer>
            </div>
          </article>
          <aside className="App-text-container">
            <TextContainer></TextContainer>
          </aside>
        </div>
        <div>
          <ControlsContainer></ControlsContainer>
        </div>
      </div>
    </PlotbotContext.Provider>
  );
}

export default App;
