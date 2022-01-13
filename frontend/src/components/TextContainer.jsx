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

    const tryLogin = async (event) => 
    {
        // don"t reload the page
        event.preventDefault()
        // now cook up the form
        let formData = new FormData()
        formData.append("grant_type","password")
        formData.append("scope","story:reader story:writer")
        formData.append("username","felipeazucares")
        formData.append("password","BlackM1lk")
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

    const tryGetStoryText = async () => 
    {
        try{            
            const response = await fetch("http://localhost:9000/text",
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

    // document.body.style.background = {background};
    tryGetStoryText()},[setStoryText,storyTree]);    

return (
    <div style={{height: "40vh"}} >
        {storyText}
    </div>
  );
}