import React, { useState, useContext } from "react"
import { UserContext } from '../App';
import {
    Button,
} from "@chakra-ui/react"
import { StoryTreeContext } from "../App"

  export default function getNewText() {
    // const [password, setPassword] = useState("")
    // const [username, setUsername] = useState("")
    // const [isLoggedIn, setIsLoggedIn] = useState(false);
    // const noUsernameError = username === ""
    // const noPasswordError = password === ""
    // //get user from context
    // const {user,setUser} = useContext(UserContext)
    
    // const handleUsernameChange = (inputValue) => setUsername(inputValue.target.value)
    // const handlePasswordChange = (inputValue) => setPassword(inputValue.target.value)
    const {storyTree, setStoryTree} = useContext(StoryTreeContext)

    const tryGetText = async (itemId) => 
    {
        // don"t reload the page
        // event.preventDefault()
        // now cook up the form
        // let formData = new FormData()
        // formData.append("grant_type","password")
        // formData.append("scope","story:reader story:writer")
        // formData.append("username",username)
        // formData.append("password",password)
        try{            
            const response = await fetch("http://localhost:9000/text",{method:"get", credentials:"include"})
            if (response.status===200 && response.statusText==="OK"){
                console.log("get text")
                setStoryTree(convertTree(result.data.story))
                // setUser(username)
                
            } else {
                console.error(`get text failed with status:${response.status} - ${response.statusText}`)
            }
        }
        catch(error){
            console.error(`Exception occured loggin in: ${error}`)
        }
    }


    const renderButtonGetStoryTree =(
        <StoryTreeContext.Provider value = {storyTree}>
        <Button colorScheme="blue" className="flex_button" onClick={tryGetText}>
            get tree
        </Button>
        </StoryTreeContext.Provider>
    )

    return (
        renderButtonGetStoryTree    
  )
}