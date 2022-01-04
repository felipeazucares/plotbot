import React, { useEffect, useState } from "react";
import {
    Input,
    Button,
    FormControl,
    FormLabel,
    FormErrorMessage,
    FormHelperText,
    ModalBody,

} from "@chakra-ui/react";

 
  export default function Login() {
    const [password, setPassword] = useState('')
    const [username, setUsername] = useState('')
    const noUsernameError = username === ''
    const noPasswordError = password === ''
    
    const handleUsernameChange = (inputValue) => setUsername(inputValue.target.value)
    const handlePasswordChange = (inputValue) => setPassword(inputValue.target.value)

    const tryLogin = async (event) => 
    {
        // don't reload the page
        event.preventDefault()
        // now cook up the form
        let data = new FormData()
        data.append("grant_type","password")
        data.append("scopes","story:reader story:writer")
        data.append("username",username)
        data.append("password",password)
        const response = await fetch("http://localhost:9000/login",{method:"POST", body: data});
        console.log(response);
    }

    useEffect(() => {
        tryLogin()
    }, [])


    return (
    <form onSubmit={tryLogin}>
        <FormControl isInvalid={(noUsernameError)||noPasswordError}>
        <FormLabel htmlFor='username'>username</FormLabel>
            <Input
                id='username'
                type='text'
                value={username}
                onChange={handleUsernameChange}
            />
            {noUsernameError ? (
                <FormErrorMessage>username required</FormErrorMessage>
            ):(
                <FormHelperText>
                Enter your username
                </FormHelperText>
            )}
            <FormLabel htmlFor='password'>password</FormLabel>
            <Input
                id='password'
                type='password'
                value={password}
                onChange={handlePasswordChange}
            />
            {noPasswordError ? (
                <FormErrorMessage>password required</FormErrorMessage>
            ):(
                <FormHelperText>
                Enter your password
                </FormHelperText>
            )}
            <Button type='submit' colorScheme='blue' size="lg">login
            </Button>
        </FormControl>
    </form>
  )
}