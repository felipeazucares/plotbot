import React, { useState } from "react"
import axios from "axios"
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
    
    const handleUsernameChange = (inputValue) => setUsername(inputValue.target.value)
    const handlePasswordChange = (inputValue) => setPassword(inputValue.target.value)

    const tryLogin = async (event) => 
    {
        // don"t reload the page
        event.preventDefault()
        // now cook up the form
        let formData = new FormData()
        formData.append("grant_type","password")
        formData.append("scopes","story:reader story:writer")
        formData.append("username",username)
        formData.append("password",password)
        console.log("data:"+formData);
        axios.defaults.withCredentials = true
        // const config = {
        //         headers: {
        //             'content-type': 'multipart/form-data'
        //         }
        //     }
        // const axiosConfig={
        //     method: "post",
        //     url: baseURL,
        //     withCredentials: true,
        //     data: data
        // }
        try{            
            const response = await axios.post("http://localhost:9000/login",formData)
            if (response.status===200 && response.statusText==="OK"){
                console.log("logged in successfully")
                console.log(response["headers"]);
                setIsLoggedIn(true)
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
        </form>
    )

    return (
        <div>
            {isLoggedIn ? <div>{username} successfully logged in</div> : renderLoginForm}
        </div>
  )
}