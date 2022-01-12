import React from 'react'
import { Text, Heading } from '@chakra-ui/react'
const Header = () => {
  return (
    <span>
      <Heading fontSize='5xl'>Hairy Plotter</Heading>
      <Text fontSize='xs'>Interactive fiction powered by AiTextGen & Mongodb</Text>
    </span>
  );
};


export default Header;