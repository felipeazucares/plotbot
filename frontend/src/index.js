import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import OrgChart from "./components/OrgChart";
import { ChakraProvider } from "@chakra-ui/react";
import Header from "./components/Header";
import Login from "./components/Login";

ReactDOM.render(
  <React.StrictMode>
    {/* <App /> */}
    <ChakraProvider>
      <Header />
      <Login></Login>
      <OrgChart></OrgChart>
    </ChakraProvider>
  </React.StrictMode>,
  document.getElementById("root")
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
