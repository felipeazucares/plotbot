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
  todos: [], fetchTodos: () => {}
})

export default function Todos() {
  const [todos, responseData] = useState([])
  const fetchTodos = async () => {
    const response = await fetch("http://localhost:9000/")
    const todos = await response.json()
    console.log(todos);
    responseData(todos.data)
  }
  useEffect(() => {
    fetchTodos()
  }, [])
  return (
    <TodosContext.Provider value={{todos, responseData}}>
      <Button size="lg" colorScheme="blue">login</Button>
      {/* <Stack spacing={5}>
        {todos.map((todo) => (
          <b>{todo.item}</b>
        ))}
      </Stack> */}
    </TodosContext.Provider>
  )
}