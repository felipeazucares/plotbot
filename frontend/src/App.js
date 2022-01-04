import React from "react";
// import logo from "./logo.svg";
import "./App.css";
import LoginForm from "./components/LoginForm";
import OrgChart from "./components/OrgChart";
import Header from "./components/Header";

export const PlotbotContext = React.createContext();

function App() {
  return (
    <PlotbotContext.Provider>
      <div className="App">
        <div>
          <Header />
        </div>
        <div>
          <LoginForm></LoginForm>
        </div>
        <div>
          <OrgChart></OrgChart>
        </div>
      </div>
    </PlotbotContext.Provider>
  );
}

export default App;
