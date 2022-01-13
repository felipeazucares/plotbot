import React, { useState, useContext } from "react"
import { UserContext } from '../App';
import {
    Input,
    Button,
    FormControl,
    FormLabel,
    FormErrorMessage,
    FormHelperText
} from "@chakra-ui/react"

  export default function Login() {
    const [password, setPassword] = useState("")
    const [username, setUsername] = useState("")
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const noUsernameError = username === ""
    const noPasswordError = password === ""
    //get user from context
    const {user,setUser} = useContext(UserContext)
    
    const handleUsernameChange = (inputValue) => setUsername(inputValue.target.value)
    const handlePasswordChange = (inputValue) => setPassword(inputValue.target.value)

    const tryLogin = async (event) => 
    {
        // don"t reload the page
        event.preventDefault()
        // now cook up the form
        let formData = new FormData()
        formData.append("grant_type","password")
        formData.append("scope","story:reader story:writer")
        formData.append("username",username)
        formData.append("password",password)
        try{            
            const response = await fetch("http://localhost:9000/login",{method:"POST", body: formData, credentials:"include"})
            if (response.status===200 && response.statusText==="OK"){
                console.log("logged in successfully")
                setIsLoggedIn(true)
                setUser(username)
                
            } else {
                console.error(`Login failed with status:${response.status} - ${response.statusText}`)
            }
        }
        catch(error){
            console.error(`Exception occured loggin in: ${error}`)
        }
    }


    const renderLoginForm =(
        <form onSubmit={tryLogin} className="form">
            <UserContext.Provider value = {user}>
                <FormControl isInvalid={noUsernameError||noPasswordError}>
                <FormLabel htmlFor="username">Username</FormLabel>
                    <Input
                        id="username"
                        type="text"
                        value={username}
                        onChange={handleUsernameChange}
                    />
                    {noUsernameError ? (
                        <FormErrorMessage>Username required</FormErrorMessage>
                    ):(
                        <FormHelperText>
                        </FormHelperText>
                    )}
                    <FormLabel htmlFor="password">Password</FormLabel>
                    <Input
                        id="password"
                        type="password"
                        value={password}
                        onChange={handlePasswordChange}
                    />
                    {noPasswordError ? (
                        <FormErrorMessage>Password required</FormErrorMessage>
                    ):(
                        <FormHelperText>
                        </FormHelperText>
                    )}
                    <Button type="submit" colorScheme="blue" size="lg">login
                    </Button>
                </FormControl>
            </UserContext.Provider>
        </form>
    )

    return (
        <div>
            {isLoggedIn ? null : renderLoginForm}
        </div>
  )
}