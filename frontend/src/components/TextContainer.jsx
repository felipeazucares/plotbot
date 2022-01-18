import React, { useContext, useState, useEffect} from "react"
import { StoryTreeContext,StoryTextContext,URLContext} from "../App"

export default function TextContainer() {
    const {storyText, setStoryText} = useContext(StoryTextContext)
    const {storyTree} = useContext(StoryTreeContext)
    const {baseAPIURL} = useContext(URLContext)

    // go and get the story from the API
    
    // const [password, setPassword] = useState("")
    const [username, setUsername] = useState("")
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const {user,setUser} = useContext(UserContext)

    // go and get the story from the API
    // const [password, setPassword] = useState("")
    const [username] = useState("")
    // const [isLoggedIn, setIsLoggedIn] = useState(false);
    // const {user,setUser} = useContext(UserContext)
    
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
            const response = await fetch(`${baseAPIURL}/login`,{method:"POST", body: formData, credentials:"include"})
            if (response.status===200){
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
            const response = await fetch({baseAPIURL},
                {
                    credentials:"include"
                 })
            if (response.status===200){
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

    tryGetStoryText()},[baseAPIURL,setStoryText,storyTree,username]);    

return (
    <div style={{height: "55vh"}} >
        {storyText}
    </div>
  );
}