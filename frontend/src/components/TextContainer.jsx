import React, { useContext, useState, useEffect} from "react"
import { StoryTreeContext,StoryTextContext,UserContext } from "../App"
import { Container } from '@chakra-ui/react'

export default function TextContainer() {
    const {storyText, setStoryText} = useContext(StoryTextContext)
    const {storyTree, setStoryTree} = useContext(StoryTreeContext)

    // go and get the story from the API
    
    // const [password, setPassword] = useState("")
    const [username, setUsername] = useState("")
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const {user,setUser} = useContext(UserContext)
    
    useEffect(() => {

    // const noUsernameError = username === ""
    // const noPasswordError = password === ""
    //get user from context
    
    // const handleUsernameChange = (inputValue) => setUsername(inputValue.target.value)
    // const handlePasswordChange = (inputValue) => setPassword(inputValue.target.value)

    const tryGetStoryText = async () => 
    {

        // now cook up the form
        let formData = new FormData()
        formData.append("grant_type","password")
        formData.append("scope","story:reader story:writer")
        formData.append("username","unittestuser")
        formData.append("password","don't look now")
        try{            
            const response = await fetch("http://localhost:8450/login",{method:"POST", body: formData, credentials:"include"})
            if (response.status===200 && response.statusText==="OK"){
                console.log("logged in successfully")
                setIsLoggedIn(true)
                setUser(username)
                
            } else {
                window.alert(`Login failed with status:${response.status} - ${response.statusText}`)
                console.error(`Login failed with status:${response.status} - ${response.statusText}`)
            }
        }
        catch(error){
            console.error(`Exception occured logging in: ${error}`)
            window.alert(`Exception occured logging in: ${error}`)
        }
        

        try{            
            const response = await fetch("http://localhost:8450/text",
                {
                    credentials:"include"
                 })
            if (response.status===200 && response.statusText==="OK"){
                const result = await response.json()
                console.log(`storyText:${JSON.stringify(result.data.text)}`)
                setStoryText(result.data.text)

            } else {
                console.error(`get /text failed with status:${response.status} - ${response.statusText}`)
            }
        }
        catch(error){
            console.error(`Exception occured getting story text: ${error}`)
        }
    }

    tryGetStoryText()},[setStoryText,storyTree,setUser,username]);    

return (
    <div style={{height: "40vh"}} >
        {storyText}
    </div>
  );
}