import React from 'react'
import { Text, Heading } from '@chakra-ui/react'
import UserDeets from "./UserDeets"
const Header = () => {
  return (
    <span>
      <Heading fontSize='5xl'>PlotterBot</Heading>
      <Text fontSize='xs'>Interactive fiction powered by AiTextGen & Mongodb</Text>
      <UserDeets></UserDeets>
    </span>
  );
};


export default Header;