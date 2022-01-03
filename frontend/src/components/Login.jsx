import React, { useEffect, useState } from "react";
import {
    Box,
    Button,
    Flex,
    Input,
    InputGroup,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
    Stack,
    Text,
    useDisclosure
} from "@chakra-ui/react";

const TodosContext = React.createContext({
  todos: [], tryLogin: () => {}
})

export default function Todos() {
  const [todos, responseData] = useState([])
  const tryLogin = async () => {
    const response = await fetch("http://localhost:9000/")
    const todos = await response.json()
    console.log(todos);
    responseData(todos.data)
  }
  useEffect(() => {
    tryLogin()
  }, [])
  return (
    <TodosContext.Provider value={{todos, responseData}}>
      <Button size="lg" onClick={tryLogin} colorScheme="blue">login</Button>
    </TodosContext.Provider>
  )
}