import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import { ChakraProvider } from "@chakra-ui/react";
import { extendTheme } from "@chakra-ui/react";

const theme = extendTheme({
  colors: {
    brand: {
      50: "#ffefe1",
      100: "#f4d5bd",
      200: "#e8bb97",
      300: "#dca06f",
      400: "#d18547",
      500: "#b86b2e",
      600: "#905323",
      700: "#673a17",
      800: "#3f230a",
      900: "#1b0a00",
    },
  },
});

ReactDOM.render(
  <React.StrictMode>
    {/* <App /> */}
    <ChakraProvider theme={theme}>
      <App></App>
    </ChakraProvider>
  </React.StrictMode>,
  document.getElementById("root")
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
